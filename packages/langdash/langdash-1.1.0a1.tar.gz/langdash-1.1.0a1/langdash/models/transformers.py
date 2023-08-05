from typing import Generator, List, Optional, Tuple, Union, Any, Dict, Set
from math import inf
from dataclasses import dataclass
import copy

from langdash.response import RespInfer
from langdash.llm import LLM
from langdash.llm_session import LLMGenerationSessionForRawText, LLMState
from langdash.infer import InferArgs
import langdash.sampling as sampling
import langdash.models._bpe as bpe

import transformers  # type: ignore
import torch

try:
  from transformers import RwkvForCausalLM as t_RwkvForCausalLM

  def model_is_rwkv(model):
    return isinstance(model, t_RwkvForCausalLM)
except ImportError:

  def model_is_rwkv(model):
    return False


@dataclass
class TransformersState(LLMState):
  _logits: Optional[torch.Tensor] = None
  _state: Any = None
  _next_token: Optional[Tuple[int, str]] = None


@dataclass
class TransformersExtras:
  tokenizer: Any
  vocab: Dict[str, int]
  buffered_token_head: Set[int]


class TransformersSession(
  LLMGenerationSessionForRawText["TransformersModel", TransformersState,
                                 torch.Tensor]
):
  """
  Session for transformers model.
  """

  _next_token: Optional[Tuple[int, str]]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    def load_model(llm: TransformersModel):
      if isinstance(llm._model, str):
        model = transformers.AutoModelForCausalLM.from_pretrained(
          llm._model, **llm._model_kwargs
        )
      else:
        model = llm._model

      if isinstance(llm._tokenizer, str):
        tokenizer = transformers.AutoTokenizer.from_pretrained(llm._tokenizer)
      else:
        tokenizer = llm._tokenizer

      if isinstance(
        tokenizer, (transformers.GPT2Tokenizer, transformers.GPT2TokenizerFast)
      ):
        buffered_token_head = set(
          v for k, v in tokenizer.get_vocab().items() if "\u0122" in k
        )
      else:
        buffered_token_head = set()

      extras = TransformersExtras(
        tokenizer=tokenizer,
        vocab={
          bpe.decode(logits_tokstr): logits_tokid
          for logits_tokstr, logits_tokid in tokenizer.get_vocab().items()
        },
        buffered_token_head=buffered_token_head
      )
      return model, extras

    self._model, self._extras = self._ld._get_model_internal(
      self._llm, load_model
    )
    self._logits = None
    self._state = None
    self._next_token = None

  def _heal_token(self, tok_a: int, tok_b: int) -> str:
    return self._extras.tokenizer.decode([tok_a, tok_b])

  def set_state(self, state: Optional[TransformersState]):
    if state is None:
      self._logits = None
      self._state = None
      self._next_token = None
    else:
      self._logits = copy.deepcopy(state._logits)
      self._state = copy.deepcopy(state._state)
      self._next_token = state._next_token

  def clone_state(self) -> TransformersState:
    return TransformersState(
      _logits=copy.deepcopy(self._logits),
      _state=copy.deepcopy(self._state),
      _next_token=self._next_token,
    )

  def _eval(self, tokid: int):
    if model_is_rwkv(self._model):
      outputs = self._model.forward(
        torch.IntTensor([tokid]), state=self._state, use_cache=True
      )
      self._state = outputs.state
    else:
      outputs = self._model.forward(
        torch.IntTensor([tokid]), past_key_values=self._state, use_cache=True
      )
      self._state = outputs.past_key_values
    return outputs.logits[-1]

  def decode(self, tokids: List[int]) -> str:
    return self._extras.tokenizer.decode(tokids)

  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    return self._extras.tokenizer.encode(
      text, add_special_tokens=add_special_tokens
    ).tolist()

  def next_token_probs(self):
    if self._next_token is None:
      if self._logits is None:
        raise ValueError("cannot predict next probability for empty input")
      logits = self._logits
    else:
      if model_is_rwkv(self._model):
        logits = self._model.forward(
          torch.IntTensor([self._next_token[0]]),
          state=self._state,
          use_cache=True
        )._logits[-1]
      else:
        logits = self._model.forward(
          torch.IntTensor([self._next_token[0]]),
          past_key_values=self._state,
          use_cache=True
        )._logits[-1]
    return sampling.logits_to_probs(logits).tolist()

  def _infer(self, end: Optional[Union[str, int]],
             args: InferArgs) -> Generator[RespInfer, None, None]:
    generated = ""
    ctx: List[int] = []
    buffered_tokens: List[int] = []
    stops_at_eot = (
      (isinstance(end, str) and len(end) == 0) or
      (isinstance(end, int) and end == self._extras.tokenizer.eos_token_id)
    )
    eot_tok = self._extras.tokenizer.eos_token_id

    if self._logits is None:
      raise ValueError("no prompt provided for TransformersModel")

    for i in range(args.max_new_tokens):
      strip_left = None

      if i == 0 and self._next_token is not None:
        tokid, tokstr = self._next_token

        for logits_tokstr, logits_tokid in self._extras.vocab:
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

      if stops_at_eot and tokid == eot_tok:
        break
      elif tokid in self._extras.buffered_token_head:
        buffered_tokens.append(tokid)
      else:
        if buffered_tokens:
          tokstr = self._extras.tokenizer.decode(buffered_tokens + [tokid])
          buffered_tokens = []
        else:
          tokstr = self._extras.tokenizer.decode([tokid])

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


class TransformersModel(LLM[TransformersSession]):
  """
  transformers model.
  """
  Session = TransformersSession

  def __init__(
    self,
    model: Union[str, transformers.PreTrainedModel],
    tokenizer: Optional[Union[str, transformers.PreTrainedTokenizer]] = None,
    **model_kwargs
  ):
    """
    Creates a template for a language model powered by the transformers library.
    
    Args:
      model (Union[str, transformers.PreTrainedModel]):
        The name of the model, or the model class itself.
      tokenizer (Optional[Union[str, transformers.PreTrainedTokenizer]]):
        The name of the tokenizer, or the tokenizer class itself.
        Defaults to `None`. If not set, the name of the model will be used to detect the tokenizer.
    """
    if tokenizer is None:
      assert isinstance(model, str), "model must be string if tokenizer is None"
      tokenizer = model
    self._model = model
    self._tokenizer = tokenizer
    self._model_kwargs = model_kwargs
