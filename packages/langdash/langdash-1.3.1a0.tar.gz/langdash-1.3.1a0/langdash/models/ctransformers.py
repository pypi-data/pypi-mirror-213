from typing import Generator, List, Optional, Union, Dict, Any, Set
from math import inf
import weakref

import torch

from langdash.response import RespInfer
from langdash.llm import LLM
from langdash.llm_session import LLMGenerationSessionForRawText
from langdash.infer import InferArgs
import langdash.sampling as sampling
import langdash.models._bpe as bpe

import ctransformers # type: ignore
from ctransformers.llm import LLM as CTransformersLLM, LLMState as CTransformersState # type: ignore

class CTransformersWrapper:
  model: CTransformersLLM
  tokenizer: Optional[Any]
  buffered_token_head: Set[int]
  vocab: Dict[str, int]
  last_called_session: Optional[weakref.ref]

  def __init__(self, model_path: str, tokenizer: Optional[Any] = None, *args, **kwargs):
    self.model = ctransformers.AutoModelForCausalLM.from_pretrained(model_path, **kwargs)
    if tokenizer:
      self.tokenizer = tokenizer
      import transformers
      if isinstance(
        tokenizer, (transformers.GPT2Tokenizer, transformers.GPT2TokenizerFast)
      ):
        self.vocab = {
          bpe.decode(logits_tokstr): logits_tokid
          for logits_tokstr, logits_tokid in tokenizer.get_vocab().items()
        }
        self.buffered_token_head = set(
          v for k, v in tokenizer.get_vocab().items() if "\u0122" in k
        )
      else:
        self.vocab = tokenizer.get_vocab()
        self.buffered_token_head = set()
    else:
      self.tokenizer = tokenizer
      self.vocab = {}
      self.buffered_token_head = set()
    self.last_called_session = None

  def is_eot(self, tokid: int):
    return self.model.is_eos_token(tokid)

  def eval(self, tokens: List[int]) -> torch.Tensor:
    self.model.eval(tokens)
    return torch.tensor(self.model.logits)

  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    if self.tokenizer:
      return self.tokenizer.tokenize(text, add_special_tokens=add_special_tokens)
    else:
      return self.model.tokenize(text)

  def detokenize(self, tokens: List[int]) -> str:
    if self.tokenizer:
      return self.tokenizer.detokenize(tokens)
    else:
      return self.model.detokenize(tokens)

  def enter_session(self, session: "CTransformersSession"):
    if self.last_called_session is None:
      self.last_called_session = weakref.ref(session)
      return
    last_called_session = self.last_called_session()
    if session == last_called_session:
      return
    elif last_called_session is not None:
      last_called_session._logits = self.load_logits_from_model()
      last_called_session._state = self.model.save_state()
    if session._state is not None:
      self.model.set_state(session._state)
    self.last_called_session = weakref.ref(session)

  def load_logits_from_model(self) -> torch.Tensor:
    return torch.Tensor(self.model.eval_logits[-1])

  def clone_state(self, session: "CTransformersSession") -> CTransformersState:
    self.enter_session(session)
    return self.model.clone_state()

  def set_state(self, session: "CTransformersSession", state: Optional[CTransformersState]):
    self.enter_session(session)
    self.model.reset()
    if state is not None:
      self.model.set_state(state)


class CTransformersSession(
  LLMGenerationSessionForRawText["CTransformersModel", CTransformersState, torch.Tensor]
):
  """
  Session for llama.cpp model.
  """

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    def load_model(llm: CTransformersModel):
      return CTransformersWrapper(model_path=llm._model_path, **llm._model_kwargs)

    self._model = self._ld._get_model_internal(self._llm, load_model)

    self._logits = None
    self._state = None
    self._next_token = None

  def _eval(self, token: int):
    return self._model.eval([token])

  def _eval_mult(self, tokens: List[int]):
    return self._model.eval(tokens)

  def _next_token_logits_raw(self):
    self._model.enter_session(self)
    if self._next_token is None:
      if self._logits is None:
        raise ValueError("cannot predict next probability for empty input")
      logits = self._logits
    else:
      logits = self._eval(self._next_token[0])
    return logits

  def next_token_logits(self) -> List[float]:
    return self._next_token_logits_raw().tolist()

  def next_token_probs(self) -> List[float]:
    return sampling.logits_to_probs(self._next_token_logits_raw()).tolist()

  def set_state(self, state: Optional[CTransformersState]):
    self._model.set_state(self, state)
    if state == None:
      self._logits = None
    else:
      self._logits = self._model.load_logits_from_model()

  def clone_state(self) -> CTransformersState:
    return self._model.clone_state(self)

  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    return self._model.tokenize(text, add_special_tokens=add_special_tokens)

  def decode(self, tokens: List[int]) -> str:
    return self._model.detokenize(tokens)

  def _infer(self, end: Optional[Union[str, int]],
             args: InferArgs) -> Generator[RespInfer, None, None]:
    self._model.enter_session(self)

    generated = ""
    ctx: List[int] = []
    buffered_tokens: List[int] = []
    stops_at_eot = (
      (isinstance(end, str) and len(end) == 0) or
      (isinstance(end, int) and self._model.is_eot(end))
    )

    if self._logits is None:
      raise ValueError("no prompt provided for CTransformersModel")

    for i in range(args.max_new_tokens):
      strip_left = None

      if i == 0 and self._next_token is not None:
        tokid, tokstr = self._next_token

        for logits_tokstr, logits_tokid in self._model.vocab:
          if not logits_tokstr.startswith(tokstr):
            self._logits[logits_tokid] = -inf

        if self._logits.isinf().all():
          # we don't need to heal tokens because no token that begins with _next_token
          self._logits = self._eval(tokid)
        else:
          strip_left = tokstr

        self._next_token = None

      if not stops_at_eot:  # no early endoftext
        self._logits[0] = -inf

      tokid = sampling.sample(self._logits, args, ctx)
      ctx.append(tokid)

      if stops_at_eot and self._model.is_eot(tokid):
        break
      elif tokid in self._model.buffered_token_head:
        buffered_tokens.append(tokid)
      else:
        if buffered_tokens:
          tokstr = self._model.detokenize(buffered_tokens + [tokid])
          buffered_tokens = []
        else:
          tokstr = self._model.detokenize([tokid])

        if strip_left and tokstr.startswith(tokstr):
          tokstr = tokstr[len(strip_left):]

        self._next_token = (tokid, tokstr)

        generated += tokstr
        if isinstance(end, str) and end and generated.endswith(end):
          generated = generated[:-len(end)]
          break

        yield RespInfer(tokid=tokid, tokstr=tokstr, running_infer=generated)

      self._logits = self._eval(tokid)

    yield RespInfer(tokid=-1, tokstr="", running_infer=generated)

  # Wrapper for public functions to flush the old session states

  def inject(self, *a, **k):
    self._model.enter_session(self)
    return LLMGenerationSessionForRawText.inject(self, *a, **k)

  def flush_token(self, *a, **k):
    self._model.enter_session(self)
    return LLMGenerationSessionForRawText.inject(self, *a, **k)


class CTransformersModel(LLM[CTransformersSession]):
  """
  llama.cpp model.
  """

  Session = CTransformersSession

  def __init__(self, model_path: str, **model_kwargs):
    self._model_path = model_path
    self._model_kwargs = model_kwargs

  def session(self, **kwargs):
    return CTransformersSession(self, **kwargs)
