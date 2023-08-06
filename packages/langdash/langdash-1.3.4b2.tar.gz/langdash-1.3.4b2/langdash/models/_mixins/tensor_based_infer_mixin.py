from typing import Generator, Optional, Union, Any, Tuple, List
from math import inf
from torch import Tensor

from langdash.response import RespInfer
from langdash.infer import InferArgs
import langdash.sampling as sampling
from .._tokenizer.tokenizer import BufferedToken


class TensorBasedInferMixin:
  _model: Any
  _logits: Optional[Tensor]
  _next_token: Optional[Tuple[int, str]]

  def _eval(self, token: int) -> Tensor:
    raise NotImplementedError("_eval")

  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    raise NotImplementedError("tokenize")

  def decode(self, tokids: List[int]) -> str:
    raise NotImplementedError("decode")

  def _infer(self, end: Optional[Union[str, int]],
             args: InferArgs) -> Generator[RespInfer, None, None]:
    generated = ""
    buffered_tokens: Optional[BufferedToken] = None
    ctx: List[int] = []

    if isinstance(end, str):
      if len(end) == 0:
        end = self._model.eos_token
      elif args.min_new_tokens > 0:
        endtoks = self.tokenize(end)
        assert len(endtoks) == 1
        end = endtoks[0]

    if self._logits is None:
      raise ValueError("no prompt provided")

    for i in range(args.max_new_tokens):
      strip_left: Optional[str] = None

      if i == 0 and self._next_token is not None:
        for logits_tokid in self._model.tokenizer.tokens_starting_with(
          self._next_token[0]
        ):
          self._logits[logits_tokid] = -inf

        if self._logits.isinf().all():
          # we don't need to heal tokens because no token that begins with _next_token
          self._logits = self._eval(self._next_token[0])
        else:
          strip_left = self._next_token[1]

        self._next_token = None

      if end != self._model.eos_token:  # no early endoftext
        self._logits[self._model.eos_token] = -inf
      elif args.min_new_tokens > 0 and i < args.min_new_tokens:
        self._logits[end] = -inf

      tokid = sampling.sample(self._logits, args, ctx)
      ctx.append(tokid)

      if tokid == self._model.eos_token:  # implies end is int
        break

      tokstr: Optional[str] = None

      if buffered_tokens is None:
        tokstr_or_buffered = self._model.tokenizer.decode_once(tokid)

        if isinstance(tokstr_or_buffered, str):
          tokstr = tokstr_or_buffered
        else:
          buffered_tokens = tokstr_or_buffered
      else:
        tokstr = buffered_tokens.add_token_id(tokid)

      if tokstr is not None:
        if strip_left and tokstr.startswith(strip_left):
          tokstr = tokstr[len(strip_left):]

        self._next_token = (tokid, tokstr)

        generated += tokstr
        if isinstance(end, str) and end and generated.endswith(end):
          generated = generated[:-len(end)]
          break

        yield RespInfer(tokid=tokid, tokstr=tokstr, running_infer=generated)

        buffered_tokens = None

      self._logits = self._eval(tokid)

    if buffered_tokens:
      tokstr = buffered_tokens.flush()
      generated += tokstr
      yield RespInfer(tokid=tokid, tokstr=tokstr, running_infer=generated)
    yield RespInfer(tokid=-1, tokstr="", running_infer=generated)


class TensorBasedInferWithSessionMixin:

  def _infer(self, *a, **k):
    self._model.enter_session(self)
    yield from TensorBasedInferMixin._infer(self, *a, **k)
