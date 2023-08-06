from typing import Generator, Dict, Any
from langdash.response import RespInfer
from langdash.llm import LLM
from langdash.llm_session import LLMSession


class MockSession(LLMSession):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def inject(self, text: str) -> int:
    return 0

  def _infer(self, end: str,
             args: Dict[str, Any]) -> Generator[RespInfer, None, None]:
    yield RespInfer(tokid=0, tokstr="", running_infer=self._llm._mockret)


class MockModel(LLM[MockSession]):
  Session = MockSession

  def __init__(self, mockret: str):
    self._mockret = mockret

  def session(self, **kwargs):
    return MockSession(self, **kwargs)
