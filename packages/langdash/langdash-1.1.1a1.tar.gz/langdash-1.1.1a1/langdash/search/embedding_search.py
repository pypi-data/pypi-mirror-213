import faiss
from typing import Generator, Tuple, List, Union

from langdash.llm_session import LLMEmbeddingSession
from langdash.search.engine import Engine


class EmbeddingSearch(Engine):
  """ A search engine that uses vector embeddings from a language model. """

  def __init__(
    self,
    embd_session: LLMEmbeddingSession,
  ):
    super().__init__()
    self._embd_session = embd_session
    self._embds = faiss.IndexFlatIP(self._embd_session.embedding_size())

  def add(self, texts: Union[str, List[str]]):
    if isinstance(texts, str):
      self._documents.append(texts)
      self._embds.add(self._embd_session.embed([texts]))
    else:
      self._documents += texts
      self._embds.add(self._embd_session.embed(texts))

  def search(
    self,
    text: str,
    max_documents: int = 1
  ) -> Generator[Tuple[str, float], None, None]:
    embd = self._embd_session.embed([text])
    if max_documents == -1:
      max_documents = len(self._documents)
    D, I = self._embds.search(embd, max_documents)
    for d, i in zip(D[0], I[0]):
      yield i, self._documents[i], d
