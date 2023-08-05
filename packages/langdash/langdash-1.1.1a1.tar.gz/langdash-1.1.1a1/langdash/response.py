from dataclasses import dataclass


class Response:
  """ Base class for responses from language model """
  pass


@dataclass
class RespReturns(Response):
  """
  Returns response. Acts as a header for return values.
  
  Attributes:
    key: Return key
  """
  key: str


@dataclass
class RespInfer(Response):
  """
  Inference response. Will be emitted on every token generated.
  
  Attributes:
    tokid: Token ID, or -1 if last inference
    tokstr: Token string representation, or empty string if last inference
    running_infer: Current generated string
  """
  tokid: int
  tokstr: str
  running_infer: str


@dataclass
class RespInject(Response):
  """
  Injected response. Will be emitted every time new context is injected.
  
  Attributes:
    tokens_counter: Number of tokens injected to model
  """
  tokens_counter: int
