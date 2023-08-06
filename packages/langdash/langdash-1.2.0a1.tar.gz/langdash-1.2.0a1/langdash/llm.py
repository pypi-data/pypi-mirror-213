from typing import TypeVar, Generic, Type, TYPE_CHECKING
from enum import Flag, auto


class LLMCapability(Flag):
  """
  Capability of language models.
  """
  Generative = auto()
  Embedding = auto()


if TYPE_CHECKING:
  from langdash.llm_session import LLMSession, LLMEmbeddingSession
  T_LLMSession = TypeVar("T_LLMSession", bound=LLMSession)
  T_LLMEmbeddingSession = TypeVar(
    "T_LLMEmbeddingSession", bound=LLMEmbeddingSession
  )
else:
  T_LLMSession = TypeVar("T_LLMSession")
  T_LLMEmbeddingSession = TypeVar("T_LLMEmbeddingSession")


class LLM(Generic[T_LLMSession]):
  """
  A language model class for inference.
  """
  Session: Type["T_LLMSession"]

  def session(self, *args, **kwargs) -> "T_LLMSession":
    """
    Create a new session for the given model.
    
    Args:
      default_infer_args (dict):
        Default arguments for the default inference engine.
      track_called_chains (bool):
        Whether to track called chains.
      token_healing (bool):
        Whether to tokenize the input text.
      global_args (dict):
        Global arguments for the session.

    Returns:
      A new session object.
    """
    return self.__class__.Session(llm=self, *args, **kwargs)

  def get_capability(self) -> LLMCapability:
    """
    Returns the capability of the language model.
    """
    return LLMCapability.Generative


class EmbeddingLLM(LLM[T_LLMEmbeddingSession]):
  """
  A language model class for generating embeddings.
  """

  def get_capability(self) -> LLMCapability:
    return LLMCapability.Embedding
