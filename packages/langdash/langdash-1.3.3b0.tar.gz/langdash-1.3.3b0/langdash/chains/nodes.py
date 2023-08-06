from dataclasses import dataclass
from typing import List, Union, Optional, Tuple, TYPE_CHECKING
import random
from weakref import WeakKeyDictionary
from math import inf

from langdash.response import RespInfer, RespInject, RespReturns
from langdash.infer import InferArgs

if TYPE_CHECKING:
  from langdash.core import Langdash
  from langdash.llm_session import LLMGenerationSession
  from .chains import LDChain, LDNodeGenerator, LDNodeArgs


class LDNode:
  """ Base class for langdash nodes. """

  def __init__(self, ld: "Langdash"):
    self._ld = ld

  def __call__(
    self, session: "LLMGenerationSession", args: "LDNodeArgs"
  ) -> "LDNodeGenerator":
    raise NotImplementedError("__call__")


class LDText(LDNode):
  """ Constant text node """

  def __init__(
    self, ld: "Langdash", text: str, add_special_tokens: bool = False
  ):
    super().__init__(ld)
    self._text = text
    self._add_special_tokens = add_special_tokens

  def __repr__(self):
    return f"<Text>\n{self._text}\n</Text>"

  def __call__(
    self, session: "LLMGenerationSession", args: "LDNodeArgs"
  ) -> "LDNodeGenerator":
    tokens_counter = session.inject(
      self._text, add_special_tokens=self._add_special_tokens
    )
    yield RespInject(tokens_counter=tokens_counter)


class LDFormatArg(LDNode):
  """ Format argument node """

  def __init__(self, ld: "Langdash", text: str):
    super().__init__(ld)
    self._text = text

  def __repr__(self):
    return f"<FormatArgs>\n{self._text}\n</FormatArgs>"

  def __call__(
    self, session: "LLMGenerationSession", args: "LDNodeArgs"
  ) -> "LDNodeGenerator":
    tokens_counter = session.inject(
      self._text.format(globals=session.global_args, **args)
    )
    yield RespInject(tokens_counter=tokens_counter)


class LDArg(LDNode):
  """ Argument node """

  def __init__(
    self, ld: "Langdash", arg: str, padleft: str = "", padright: str = ""
  ):
    super().__init__(ld)
    self._arg = arg
    self._padleft = padleft
    self._padright = padright

  def __repr__(self):
    return f"<Arg arg={self._arg}>"

  def __call__(
    self, session: "LLMGenerationSession", args: "LDNodeArgs"
  ) -> "LDNodeGenerator":
    s = ""
    s += self._padleft
    if self._arg in args:
      s += str(args[self._arg])
    else:
      s += str(session.global_args[self._arg])
    s += self._padright
    tokens_counter = session.inject(s)
    yield RespInject(tokens_counter=tokens_counter)


class LDReturns(LDNode):
  """ Return node """

  def __init__(
    self,
    ld: "Langdash",
    returns: str,
    end: Optional[Union[str, int]],
    padleft: str = "",
    infer_args: Optional[InferArgs] = None
  ):
    super().__init__(ld)
    self._returns = returns
    self._end = end
    self._padleft = padleft
    self._infer_args = infer_args

  def __repr__(self):
    return f"<Returns arg={self._returns}>"

  def __call__(
    self, session: "LLMGenerationSession", args: "LDNodeArgs"
  ) -> "LDNodeGenerator":
    for i, respinfer in enumerate(
      session.infer(end=self._end, args=self._infer_args)
    ):
      if i == 0:
        if self._padleft and respinfer.tokstr.startswith(self._padleft):
          respinfer.tokstr = respinfer.tokstr[len(self._padleft):]
      elif respinfer.tokid == -1:  # end
        if self._padleft and respinfer.running_infer.startswith(self._padleft):
          respinfer.running_infer = respinfer.running_infer[len(self
                                                                ._padleft):]
      yield respinfer


@dataclass(frozen=True)
class _LDChoiceTokensCache:
  choices_tokens: List[List[int]]
  heal_prefix: str


class LDChoice(LDNode):
  """ Choice node """

  def __init__(
    self,
    ld: "Langdash",
    returns: str,
    choices: List[str],
    padleft: str = "",
    padright: str = "",
    argmax: bool = False
  ):
    super().__init__(ld)
    self._returns = returns
    self._choices = choices
    self._padleft = padleft
    self._padright = padright
    self._argmax = argmax

    self._choices_preprocessed = [
      f"{self._padleft}{choice}{self._padright}" for choice in self._choices
    ]
    self._token_cache: WeakKeyDictionary[
      "LLMGenerationSession", _LDChoiceTokensCache] = WeakKeyDictionary()

  def __repr__(self):
    return f"<Choices {self._returns}>"

  def _get_token_cache(
    self, session: "LLMGenerationSession", heal_prefix: str
  ) -> _LDChoiceTokensCache:
    try:
      cache = self._token_cache[session]
      if cache.heal_prefix == heal_prefix:
        return cache
    except KeyError:
      pass
    cache = _LDChoiceTokensCache(
      choices_tokens=[
        session.tokenize(heal_prefix + text)
        for text in self._choices_preprocessed
      ],
      heal_prefix=heal_prefix
    )
    self._token_cache[session] = cache
    return cache

  def __call__(
    self, session: "LLMGenerationSession", args: "LDNodeArgs"
  ) -> "LDNodeGenerator":
    from langdash.llm_session import LLMGenerationSessionForRawText

    heal_prefix: str = ""
    if session.token_healing and \
      isinstance(session, LLMGenerationSessionForRawText) and \
      session._next_token is not None:
      heal_prefix = session._next_token[1]
      session._next_token = None

    cache = self._get_token_cache(session, heal_prefix)
    choices_tokens: List[Tuple[int, List[int]]] = [
      (i, list(reversed(tokens)))
      for i, tokens in enumerate(cache.choices_tokens)
    ]

    while len(choices_tokens) > 1:
      probs = session.next_token_probs()

      if self._argmax:
        tokid = -1
        tokid_prob = -inf
        for _, tokens in choices_tokens:
          cur_tokid = tokens[-1]
          if probs[cur_tokid] > tokid_prob:
            tokid = cur_tokid
            tokid_prob = probs[cur_tokid]
      else:
        cur_choice_tokens = []
        cur_choice_weights = []
        for _, tokens in choices_tokens:
          tokid = tokens[-1]
          cur_choice_tokens.append(tokid)
          cur_choice_weights.append(probs[tokid])
        tokid = random.choices(
          cur_choice_tokens, weights=cur_choice_weights
        )[0]

      session.inject(tokid)

      old_choices_tokens = choices_tokens
      choices_tokens = []
      for i, tokens in old_choices_tokens:
        if tokens[-1] == tokid:
          tokens.pop()
          choices_tokens.append((i, tokens))

    choice, remaining = choices_tokens.pop()
    for tokid in reversed(remaining):
      session.inject(tokid)
    yield RespInfer(-1, "", self._choices[choice])
    yield RespInject(tokens_counter=len(cache.choices_tokens[choice]))


class LDRepeat(LDNode):
  """ Repeat node """

  def __init__(
    self,
    ld: "Langdash",
    subchain: "LDChain",
    append_source: str,
    append_target: str,
    end: str = "",
    max_len: int = -1,
    end_threshold: float = 0.5
  ):
    super().__init__(ld)
    assert subchain._ld == ld
    self._subchain = subchain
    self._append_source = append_source
    self._append_target = append_target
    self._end = end
    self._max_len = max_len
    self._end_threshold = end_threshold

  def __call__(
    self, session: "LLMGenerationSession", args: "LDNodeArgs"
  ) -> "LDNodeGenerator":
    if self._end:
      end_toks = session.tokenize(self._end)
      assert len(end_toks) == 1, "only supports 1 end token"
      end_tok = end_toks[0]
    else:
      end_tok = 0
    append_resp = RespReturns(key=self._append_target)

    i = 0
    while True:
      in_append_source = False
      for resp in self._subchain.stream(session, args=args):
        if isinstance(resp, RespReturns):
          if resp.key == self._append_source:
            in_append_source = True
            yield append_resp
          else:
            in_append_source = False
            yield resp
        elif isinstance(resp, RespInfer):
          if resp.tokid == -1:
            yield resp
            if in_append_source:
              in_append_source = False
        else:
          yield resp
          in_append_source = False

      prob_dist = session.next_token_probs()
      if prob_dist[end_tok] > self._end_threshold:
        break

      i += 1
      if i == self._max_len:
        break
