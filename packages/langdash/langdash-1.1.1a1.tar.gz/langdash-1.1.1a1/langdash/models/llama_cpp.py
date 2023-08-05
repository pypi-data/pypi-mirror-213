from typing import Generator, List, Optional, Union
from math import inf
import weakref

import torch
from llama_cpp import Llama, LlamaState, llama_token_to_str  #type: ignore

from langdash.response import RespInfer
from langdash.llm import LLM
from langdash.llm_session import LLMGenerationSessionForRawText
from langdash.infer import InferArgs
import langdash.sampling as sampling


class LlamaWrapper:
  model: Llama
  vocab: List[bytes]
  last_called_session: Optional[weakref.ref]

  def __init__(self, *args, **kwargs):
    self.model = Llama(*args, **kwargs)
    self.vocab = [
      llama_token_to_str(self.model.ctx, tokid)
      for tokid in range(self.model.n_vocab())
    ]
    self.last_called_session = None

  def eval(self, tokens: List[int]) -> torch.Tensor:
    self.model.eval(tokens)
    return torch.from_numpy(self.model._scores[-1, :])

  def tokenize(self, text: bytes, add_bos: bool = True) -> List[int]:
    return self.model.tokenize(text=text, add_bos=add_bos)

  def detokenize(self, tokens: List[int]) -> bytes:
    return self.model.detokenize(tokens=tokens)

  def enter_session(self, session: "LlamaCppSession"):
    if self.last_called_session is None:
      self.last_called_session = weakref.ref(session)
      return
    last_called_session = self.last_called_session()
    if session == last_called_session:
      return
    elif last_called_session is not None:
      last_called_session._logits = self.load_logits_from_llama()
      last_called_session._state = self.model.save_state()
    if session._state is not None:
      self.model.load_state(session._state)
    self.last_called_session = weakref.ref(session)

  def load_logits_from_llama(self) -> torch.Tensor:
    return torch.Tensor(self.model.eval_logits[-1])

  def clone_state(self, session: "LlamaCppSession") -> LlamaState:
    self.enter_session(session)
    return self.model.save_state()

  def set_state(self, session: "LlamaCppSession", state: Optional[LlamaState]):
    self.enter_session(session)
    self.model.reset()
    if state is not None:
      self.model.load_state(state)


class LlamaCppSession(
  LLMGenerationSessionForRawText["LlamaCppModel", LlamaState, torch.Tensor]
):
  """
  Session for llama.cpp model.
  """

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    def load_model(llm: LlamaCppModel):
      return LlamaWrapper(model_path=llm._model_path, **llm._model_kwargs)

    self._llama = self._ld._get_model_internal(self._llm, load_model)
    self._eos_token = Llama.token_eos()
    self._bos_token = Llama.token_bos()

    self._logits = None
    self._state = None
    self._next_token = None

  def _eval(self, token: int):
    return self._llama.eval([token])

  def _eval_mult(self, tokens: List[int]):
    return self._llama.eval(tokens)

  def next_token_probs(self):
    self._llama.enter_session(self)
    if self._next_token is None:
      if self._logits is None:
        raise ValueError("cannot predict next probability for empty input")
      logits = self._logits
    else:
      logits = self._eval(self._next_token[0])
    return sampling.logits_to_probs(logits).tolist()

  def set_state(self, state: Optional[LlamaState]):
    self._llama.set_state(self, state)
    if state == None:
      self._logits = None
    else:
      self._logits = self._llama.load_logits_from_llama()

  def clone_state(self) -> LlamaState:
    return self._llama.clone_state(self)

  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    return self._llama.tokenize(text.encode("utf-8"), add_bos=False)

  def decode(self, tokens: List[int]) -> str:
    return self._llama.detokenize(tokens).decode("utf-8", errors="ignore")

  def _on_first_inject(self):
    self._llama.model.reset()
    self._eval(self._bos_token)

  def _infer(self, end: Optional[Union[str, int]],
             args: InferArgs) -> Generator[RespInfer, None, None]:
    self._llama.enter_session(self)

    generated = ""
    buffered_tokens = b""

    if isinstance(end, str):
      if len(end) == 0:
        end = self._eos_token
      elif args.min_new_tokens > 0:
        endtoks = self.tokenize(end)
        assert len(endtoks) == 1
        end = endtoks[0]

    if self._logits is None:
      raise ValueError("no prompt provided for LlamaCppModel")

    for i in range(args.max_new_tokens):
      strip_left = None

      if i == 0 and self._next_token is not None:
        tokstr_b = self._next_token[1].encode("utf-8")

        for logits_tokid, logits_tokstr in enumerate(self._llama.vocab):
          if not logits_tokstr.startswith(tokstr_b):
            self._logits[logits_tokid] = -inf

        if self._logits.isinf().all():
          # we don't need to heal tokens because no token that begins with _next_token
          self._logits = self._eval(self._next_token[0])
        else:
          strip_left = tokstr_b

        self._next_token = None

      if end != self._eos_token:  # no early endoftext
        self._logits[self._eos_token] = -inf
      elif args.min_new_tokens > 0 and i < args.min_new_tokens:
        self._logits[end] = -inf

      tokid = sampling.sample(self._logits, args, self._llama.model.eval_tokens)

      if tokid == end:  # implies end is int
        break

      tokstr_b = self._llama.vocab[tokid]

      try:
        if buffered_tokens:
          tokstr = (buffered_tokens + tokstr_b).decode("utf-8")
          buffered_tokens = b""
        else:
          if strip_left and tokstr_b.startswith(strip_left):
            tokstr_b = tokstr_b[len(strip_left):]
          tokstr = tokstr_b.decode("utf-8")

        self._next_token = (tokid, tokstr)

        generated += tokstr
        if isinstance(end, str) and end and generated.endswith(end):
          generated = generated[:-len(end)]
          break

        yield RespInfer(tokid=tokid, tokstr=tokstr, running_infer=generated)

      except UnicodeDecodeError:
        buffered_tokens += tokstr_b

      self._logits = self._eval(tokid)

    if buffered_tokens:
      tokstr = buffered_tokens.decode("utf-8", errors="ignore")
      generated += tokstr
      yield RespInfer(tokid=tokid, tokstr=tokstr, running_infer=generated)
    yield RespInfer(tokid=-1, tokstr="", running_infer=generated)

  # Wrapper for public functions to flush the old session states

  def inject(self, *a, **k):
    self._llama.enter_session(self)
    return LLMGenerationSessionForRawText.inject(self, *a, **k)

  def flush_token(self, *a, **k):
    self._llama.enter_session(self)
    return LLMGenerationSessionForRawText.inject(self, *a, **k)


class LlamaCppModel(LLM[LlamaCppSession]):
  """
  llama.cpp model.
  """

  Session = LlamaCppSession

  def __init__(self, model_path: str, **model_kwargs):
    self._model_path = model_path
    self._model_kwargs = model_kwargs

  def session(self, **kwargs):
    return LlamaCppSession(self, **kwargs)
