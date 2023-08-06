from typing import List, Optional, Any
import weakref
import torch

from langdash.llm import LLM
from langdash.llm_session import LLMGenerationSessionForRawText
import langdash.sampling as sampling
from ._tokenizer.tokenizer import Tokenizer
from ._tokenizer.bytes_dict_tokenizer import BytesDictTokenizer
from ._tokenizer.hf_tokenizer import HFTokenizer
from ._mixins.tensor_based_infer_mixin import TensorBasedInferWithSessionMixin

import ctransformers  # type: ignore
from ctransformers.llm import LLM as CTransformersLLM, LLMState as CTransformersState  # type: ignore


class CTransformersWrapper:
  model: CTransformersLLM
  tokenizer: Tokenizer
  vocab: List[bytes]
  last_called_session: Optional[weakref.ref]
  eos_token: int

  def __init__(
    self,
    model_path: str,
    transformers_tokenizer: Optional[Any] = None,
    *args,
    **kwargs
  ):
    self.model = ctransformers.AutoModelForCausalLM.from_pretrained(
      model_path, **kwargs
    )
    if transformers_tokenizer is not None:
      self.tokenizer = HFTokenizer(transformers_tokenizer)
    else:
      mapping = [
        self.model.token_id_to_str(tokid)
        for tokid in range(self.model.vocab_size)
      ]
      self.tokenizer = BytesDictTokenizer(
        lambda text, **_k: self.model.tokenize(text),
        lambda tokens: self.model.detokenize(tokens), mapping
      )
    self.eos_token = self.model.eos_token_id
    self.last_called_session = None

  def eval(self, tokens: List[int]) -> torch.Tensor:
    self.model.eval(tokens)
    return torch.tensor(self.model.logits)

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

  def set_state(
    self, session: "CTransformersSession", state: Optional[CTransformersState]
  ):
    self.enter_session(session)
    self.model.reset()
    if state is not None:
      self.model.set_state(state)


class CTransformersSession(
  TensorBasedInferWithSessionMixin,
  LLMGenerationSessionForRawText["CTransformersModel", CTransformersState,
                                 torch.Tensor]
):
  """
  Session for llama.cpp model.
  """

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    def load_model(llm: CTransformersModel):
      return CTransformersWrapper(
        model_path=llm._model_path, **llm._model_kwargs
      )

    self._model = self._ld._get_model_internal(self._llm, load_model)

    self._logits = None
    self._state = None
    self._next_token = None

  def _eval(self, token: int):
    return self._model.eval([token])

  def _eval_mult(self, tokens: List[int]):
    return self._model.eval(tokens)

  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    return self._model.tokenizer.encode(
      text, add_special_tokens=add_special_tokens
    )

  def decode(self, tokids: List[int]) -> str:
    return self._model.tokenizer.decode(tokids)

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
    if state is None:
      self._logits = None
    else:
      self._logits = self._model.load_logits_from_model()

  def clone_state(self) -> CTransformersState:
    return self._model.clone_state(self)

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
