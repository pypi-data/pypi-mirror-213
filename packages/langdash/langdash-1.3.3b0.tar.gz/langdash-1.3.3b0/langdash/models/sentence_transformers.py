from typing import List
import torch
from langdash.llm import EmbeddingLLM
from langdash.llm_session import LLMEmbeddingSession
from sentence_transformers import SentenceTransformer  # type: ignore


class SentenceTransformersSession(
  LLMEmbeddingSession["SentenceTransformersModel", torch.Tensor]
):
  """
  Session for sentence_transformers embedding model.
  """

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self._model = self._ld._get_model_internal(
      self._llm, lambda llm: SentenceTransformer(llm._model_name)
    )

  def embedding_size(self) -> int:
    return self._model.get_sentence_embedding_dimension()

  def embed(self, documents: List[str]) -> torch.Tensor:
    return self._model.encode(documents)


class SentenceTransformersModel(EmbeddingLLM[SentenceTransformersSession]):
  """
  sentence_transformers embedding model.
  """
  Session = SentenceTransformersSession

  def __init__(self, model_name: str):
    self._model_name = model_name
