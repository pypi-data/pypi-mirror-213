from typing import List, Optional, Tuple, Union, Any
from dataclasses import dataclass
import copy

from langdash.llm import LLM
from langdash.llm_session import LLMGenerationSessionForRawText, LLMState
import langdash.sampling as sampling
from ._tokenizer.hf_tokenizer import HFTokenizer
from ._mixins.tensor_based_infer_mixin import TensorBasedInferMixin

import transformers  # type: ignore
import torch

try:
  from transformers import RwkvForCausalLM as t_RwkvForCausalLM

  def model_is_rwkv(model):
    return isinstance(model, t_RwkvForCausalLM)
except ImportError:

  def model_is_rwkv(model):
    return False


def _deep_clone_tensor_tup(val):
  if isinstance(val, tuple):
    return tuple(_deep_clone_tensor_tup(inner) for inner in val)
  elif isinstance(val, torch.Tensor):
    return torch.tensor(val)
  else:
    raise NotImplementedError(f"{val.__class__.__name__}")


@dataclass
class TransformersState(LLMState):
  _logits: Optional[torch.Tensor] = None
  _state: Any = None
  _next_token: Optional[Tuple[int, str]] = None


class TransformersWrapper:
  model: Any
  tokenizer: HFTokenizer
  eos_token: int

  def __init__(self, llm: "TransformersModel"):
    if isinstance(llm._model, str):
      self.model = transformers.AutoModelForCausalLM.from_pretrained(
        llm._model, **llm._model_kwargs
      )
    else:
      self.model = llm._model

    if isinstance(llm._tokenizer, str):
      hf_tokenizer = transformers.AutoTokenizer.from_pretrained(
        llm._tokenizer, errors="strict", use_fast=False
      )
    else:
      hf_tokenizer = llm._tokenizer
    self.tokenizer = HFTokenizer(hf_tokenizer)
    self.eos_token = hf_tokenizer.eos_token_id

  def forward(self, *a, **k):
    return self.model.forward(*a, **k)


class TransformersSession(
  TensorBasedInferMixin,
  LLMGenerationSessionForRawText["TransformersModel", TransformersState,
                                 torch.Tensor]
):
  """
  Session for transformers model.
  """

  _logits: Optional[torch.Tensor]
  _next_token: Optional[Tuple[int, str]]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    def load_model(llm: TransformersModel):
      return TransformersWrapper(llm)

    self._model = self._ld._get_model_internal(self._llm, load_model)
    self._logits = None
    self._state = None
    self._next_token = None

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
      self._state = _deep_clone_tensor_tup(outputs.state)
    else:
      outputs = self._model.forward(
        torch.IntTensor([tokid]), past_key_values=self._state, use_cache=True
      )
      self._state = _deep_clone_tensor_tup(outputs.past_key_values)
    return torch.tensor(outputs.logits[-1])

  def decode(self, tokids: List[int]) -> str:
    return self._model.tokenizer.decode(tokids)

  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    return self._model.tokenizer.encode(
      text, add_special_tokens=add_special_tokens
    )

  def _next_token_logits_raw(self):
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
    return logits

  def next_token_logits(self) -> List[float]:
    return self._next_token_logits_raw().tolist()

  def next_token_probs(self) -> List[float]:
    return sampling.logits_to_probs(self._next_token_logits_raw()).tolist()


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
        Defaults to `None`. If not set, the name of the model will be used to load the tokenizer.
    """
    if tokenizer is None:
      assert isinstance(
        model, str
      ), "model must be string if tokenizer is None"
      tokenizer = model
    self._model = model
    self._tokenizer = tokenizer
    self._model_kwargs = model_kwargs
