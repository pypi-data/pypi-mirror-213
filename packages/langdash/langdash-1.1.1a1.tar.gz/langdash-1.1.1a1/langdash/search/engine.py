from typing import Generator, Tuple, Union, List


class Engine:
  """
  Base class representing a search engine that can search for texts in a collection of documents.
  """

  _documents: List[str]

  def __init__(self):
    self._documents = []

  def __len__(self) -> int:
    return len(self._documents)

  def add(self, texts: Union[str, List[str]]):
    """
    Add one or more documents to the search engine.

    Arg:
      texts (Union[str, List[str]]):
        a document or a list of documents to add to the search engine.
    """
    raise NotImplementedError("add")

  def search(
    self,
    text: str,
    max_documents: int = 1
  ) -> Generator[Tuple[int, str, float], None, None]:
    """
    Search for documents relating to text in the engine.

    Args:
      text (str): The text to search for in the documents.
      max_documents (int): The maximum number of documents to search through. Default is 1.

    Returns:
      A generator of tuples containing the index of the document, its content
      and its relevance score to the search text.
    """
    raise NotImplementedError("search")
