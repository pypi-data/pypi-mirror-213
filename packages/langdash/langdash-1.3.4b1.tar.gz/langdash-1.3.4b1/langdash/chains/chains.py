from dataclasses import dataclass
from collections import OrderedDict
from typing import Generator, Dict, Any, List, Union, Optional, Tuple, FrozenSet, TYPE_CHECKING, cast
import re
import copy
import warnings

from langdash.response import Response, RespInfer, RespInject, RespReturns
from .nodes import LDNode, LDText, LDFormatArg, LDArg, LDReturns, LDChoice, LDRepeat
from .typing import Type, TypeDict

if TYPE_CHECKING:
  from langdash.core import Langdash
  from langdash.llm_session import LLMGenerationSession, LLMState

RE_FIRST_CONST = re.compile(r"^((?:[^{]|{{)+)")
RE_IDENT = re.compile(r"^({[a-zA-Z_][a-zA-Z0-9_]*})")
RE_FORMAT_ARG = re.compile(r"^({[^}]+})")

LDNodeGenerator = Generator[Response, None, None]
LDNodeArgs = Dict[str, Any]
LDNodeArgsFrozen = FrozenSet[Tuple[str, Any]]


@dataclass(frozen=True)
class CalledChain:
  """
  Data class used to store info about nodes previously called.
  
  Attributes:
    node: Node object
    args: Arguments passed to the node (for LDFormatArg)
    tokens_used: Number of tokens the node used (either number of tokens injected, or generated)
  """
  node: "LDNode"
  args: LDNodeArgs
  tokens_used: int


class LDChain:
  """ Class used to represent language chains """

  def __init__(
    self,
    ld: "Langdash",
    nodes: List[Union["LDNode", str]],
    args: TypeDict = {},
    returns: TypeDict = {},
  ):
    self._ld = ld
    self._args = args
    self._returns = returns
    assert len(nodes) > 0, "at least one node must be given to chain"
    self._nodes = self._preprocess_nodes(nodes)

  def cached(self, model: str, **model_kwargs) -> "LDChainCached":
    """
    Cache the chain for a specific model
    
    Args:
      model (str): The model name
      
    Returns:
      The cached chain
    """
    return LDChainCached(
      model=model,
      model_kwargs=model_kwargs,
      _ld=self._ld,
      _args=self._args,
      _returns=self._returns,
      _nodes=self._nodes,
    )

  def argtype(self, name: str) -> Optional[Type]:
    """
    Return the type of the argument.
    """
    try:
      return self._args[name]
    except KeyError:
      return None

  def _preprocess_nodes(self, nodes: List[Union["LDNode",
                                                str]]) -> List["LDNode"]:
    pp_nodes: List[Optional[LDNode]] = []

    def _preprocess_format_arg(node: LDFormatArg):
      text = node._text
      while text:
        matches = RE_FIRST_CONST.match(text)
        skip = 0
        if matches:
          skip = len(matches.group(0))
          pp_nodes.append(self._ld.text(matches.group(0)))
        else:
          matches = RE_IDENT.match(text)
          if matches:
            ident = matches.group(0)[1:-1]
            skip = len(matches.group(0))
            pp_nodes.append(self._ld.arg(ident))
          else:
            matches = RE_FORMAT_ARG.match(text)
            if matches:
              fmt = matches.group(0)
              skip = len(matches.group(0))
              pp_nodes.append(self._ld.format_args(fmt))
            else:
              pp_nodes.append(self._ld.format_args(text))
              break
        text = text[skip:]

    # create pp_nodes
    for node in nodes:
      if isinstance(node, str):
        pp_nodes.append(self._ld.text(node))
      elif isinstance(node, LDFormatArg):
        _preprocess_format_arg(node)
      else:
        pp_nodes.append(node)

    # fuse text nodes
    for i in range(len(pp_nodes)):
      pp_node_i = pp_nodes[i]
      if isinstance(pp_node_i, LDText):
        for j in range(i + 1, len(pp_nodes)):
          pp_node_j = pp_nodes[j]
          if not isinstance(pp_node_j, LDText):
            break
          pp_node_i._text += pp_node_j._text
          pp_node_j = None

    # filter
    pp_nodes = [node for node in pp_nodes if node is not None]

    return cast(List[LDNode], pp_nodes)

  def _node_pass(self, session: "LLMGenerationSession", args: LDNodeArgs):
    for node in self._nodes:
      session.tokens_counter = 0
      yield node
      session._append_called_chain(node, args, session.tokens_counter)

  def _load_session(
    self, ctx: Union[str, "LLMGenerationSession"]
  ) -> "LLMGenerationSession":
    from langdash.llm_session import LLMGenerationSession
    if isinstance(ctx, LLMGenerationSession):
      return cast(LLMGenerationSession, ctx)
    else:
      session = self._ld.session_for_model(ctx)
      assert isinstance(
        session, LLMGenerationSession
      ), "context must be LLMGenerationSession"
      return session

  def _stream(self, session: "LLMGenerationSession", args: LDNodeArgs) \
    -> Generator[Response, None, None]:
    for node in self._node_pass(session, args):
      if isinstance(node, (LDReturns, LDChoice)):
        yield RespReturns(key=node._returns)
      yield from node(session, args)

  def stream(self, ctx: Union[str, "LLMGenerationSession"], **kwargs) \
    -> Generator[Response, None, None]:
    """
    Stream data generated from the LLM within the specified session.
    
    Args:
      session (Union[str, "LLMGenerationSession"]):
        The name of the model, or an existing LLM generation session.
      args (LDNodeArgs):
        Arguments to pass to the chain. This will be used by any argument or format nodes.
    """
    return self._stream(session=self._load_session(ctx), **kwargs)

  def _call(
    self,
    session: "LLMGenerationSession",
    args: LDNodeArgs = {},
    return_session: bool = False,
    set_global_args: bool = False,
  ) -> Union["LDResult", Tuple["LDResult", "LLMGenerationSession"]]:
    result = LDResult()

    for node in self._node_pass(session, args):
      generator = node(session, args)

      if isinstance(node, LDReturns):
        text = ""
        for resp in generator:
          assert isinstance(resp, RespInfer)
          text = resp.running_infer
        result.returns[node._returns] = text

      elif isinstance(node, LDChoice):
        resp = next(generator)
        assert isinstance(resp, RespInfer)
        result.returns[node._returns] = resp.running_infer

        resp = next(generator)
        assert isinstance(resp, RespInject)
        result.completion_tokens += resp.tokens_counter

      elif isinstance(node, LDRepeat):
        text = ""
        for resp in generator:
          assert isinstance(resp, RespInfer)
          text = resp.running_infer
          if resp.tokid != -1:
            result.completion_tokens += 1
          else:
            result.returns[node._append_target].append(text)
            text = ""

      else:
        for resp in generator:
          if isinstance(resp, RespInject):
            result.prompt_tokens += resp.tokens_counter
          else:
            raise NotImplementedError(resp.__class__.__name__)

    if return_session:
      if set_global_args:
        session.global_args = args
      return result, session
    return result

  def call(self, ctx: Union[str, "LLMGenerationSession"], **kwargs):
    """
    Returns data generated from the LLM within the specified session.
    
    Args:
      ctx (Union[str, "LLMGenerationSession"]):
        The name of the model, or an existing LLM generation session.
      args (LDNodeArgs):
        Arguments to pass to the chain. This will be used by any argument or format nodes.
      return_session (bool):
        Whether or not to return the generation session after generation.
      set_global_args (bool):
        Whether or not to set current arguments as global arguments.
    
    Returns:
      (LDResult) The result, or a tuple with (result, session).
    """
    return self._call(session=self._load_session(ctx), **kwargs)


@dataclass
class _LDChainCacheState:
  state: "LLMState"
  skip_nodes: int


_LDChainCacheStoreDict = OrderedDict[FrozenSet[Tuple[str, Any]],
                                     _LDChainCacheState]


@dataclass(frozen=True)
class LDChainCacheStore:
  _dict: _LDChainCacheStoreDict
  _model: str
  _model_kwargs: dict


class LDChainCached(LDChain):

  def __init__(self, model: str, model_kwargs: dict, **kwargs):
    for k, v in kwargs.items():
      setattr(self, k, v)

    self._model = model
    self._model_kwargs = model_kwargs

    # track the first index where the argument is first used
    _arg_first_used_at = {k: -1 for k in self._args.keys()}
    # track the first index where any argument is used
    self._any_arg_first_use = 0
    for idx, node in enumerate(self._nodes):
      if isinstance(node, LDArg) and _arg_first_used_at[node._arg] == -1:
        _arg_first_used_at[node._arg] = idx
      if isinstance(
        node, (LDArg, LDFormatArg)
      ) and self._any_arg_first_use == 0:
        self._any_arg_first_use = idx
    # set min(_arg_first_used_at.values) == self._any_arg_first_use
    for k, v in _arg_first_used_at.items():
      if v == -1:
        _arg_first_used_at[k] = self._any_arg_first_use

    self._arg_first_used_at: Dict[str, int] = _arg_first_used_at
    self._arg_first_used_at_ordered: List[str] = list(
      _arg_first_used_at.keys()
    )
    self._arg_first_used_at_ordered.sort(key=lambda k: _arg_first_used_at[k])

    # cache session per argument use
    self._state_cache: _LDChainCacheStoreDict = OrderedDict()
    if len(self._args) == 0:
      self.max_states_to_cache = 1
    else:
      self.max_states_to_cache = min(len(self._args) + 2, 8)
    self._skip_nodes = 0

  # State cache functions

  def load_cache_store(self, cache_store: LDChainCacheStore):
    """
    Loads the cache store from previous inference time.
    Raises `ValueError` if the model names mismatch.
    This function expects that the model data of the parent Langdash instance does not change across session. If it does, a `UserWarning` is raised.
    
    Args:
      cache_store (LDChainCacheStore): The cache store.
    """
    if self._model != cache_store._model:
      raise ValueError("model mismatch for LDChainCacheStore")
    if self._model_kwargs != cache_store._model_kwargs:
      warnings.warn(
        "model kwargs does not match LDChainCacheStore, unexpected behavior might occur"
      )
    self._state_cache = cache_store._dict

  def save_cache_store(self) -> LDChainCacheStore:
    """ Saves the cache store into an object. """
    return LDChainCacheStore(
      _dict=copy.deepcopy(self._state_cache),
      _model=self._model,
      _model_kwargs=copy.deepcopy(self._model_kwargs)
    )

  def _set_state_cache(
    self, key: FrozenSet[Tuple[str, Any]], value: _LDChainCacheState
  ):
    self._state_cache[key] = value
    self._update_state_cache(key)
    if len(self._state_cache) > self.max_states_to_cache:
      self._state_cache.popitem(last=True)

  def _update_state_cache(self, key: FrozenSet[Tuple[str, Any]]):
    self._state_cache.move_to_end(key, last=False)

  def _get_state_cache(
    self, key: FrozenSet[Tuple[str, Any]]
  ) -> _LDChainCacheState:
    self._update_state_cache(key)
    return self._state_cache[key]

  def _arg_subset_sorted_by_idx(self, args: LDNodeArgs):
    current_subset: LDNodeArgs = {}
    yield current_subset
    for arg in self._arg_first_used_at_ordered:
      current_subset[arg] = args[arg]
      yield current_subset

  # Inference functions

  def _node_pass(self, session: "LLMGenerationSession", args: LDNodeArgs):
    last_state_key: Optional[_LDChainCacheState] = None
    for i in range(self._skip_nodes, len(self._nodes)):
      node = self._nodes[i]
      session.tokens_counter = 0
      yield node
      if isinstance(node, LDText) and last_state_key is not None:
        last_state_key.state = session.clone_state()
        last_state_key.skip_nodes = (i + 1)
      elif isinstance(node, LDArg) and self.max_states_to_cache > 0:
        # TODO: there might be a faster way of doing this
        # if the frozenset from _arg_subset_sorted_by_idx is used
        cached_idx = self._arg_first_used_at[node._arg]
        if i > cached_idx:
          last_state_key = None
          continue
        current_keys = frozenset(
          (k, v)
          for k, v in args.items()
          if self._arg_first_used_at[k] <= cached_idx
        )
        if current_keys not in self._state_cache:
          self._set_state_cache(
            current_keys,
            _LDChainCacheState(
              state=session.clone_state(), skip_nodes=(cached_idx + 1)
            )
          )
        else:
          self._update_state_cache(current_keys)
        last_state_key = self._state_cache[current_keys]
      else:
        last_state_key = None
      session._append_called_chain(node, args, session.tokens_counter)

  def _create_new_session(self) -> "LLMGenerationSession":
    ctx = self._ld.session_for_model(self._model, **self._model_kwargs)
    from langdash.llm_session import LLMGenerationSession
    assert isinstance(
      ctx, LLMGenerationSession
    ), "context must be LLMGenerationSession"
    return ctx

  def _load_gen_session(
    self, args: Optional[LDNodeArgs] = None
  ) -> "LLMGenerationSession":
    session = self._create_new_session()

    if frozenset() not in self._state_cache:
      text_node = self._nodes[0]

      if isinstance(text_node, LDText):
        session.inject(text_node._text)
        self._set_state_cache(
          frozenset(),
          _LDChainCacheState(state=session.clone_state(), skip_nodes=1)
        )
        self._skip_nodes = 1

      return session

    if args is None:
      old_state_cache = self._get_state_cache(frozenset())
      self._skip_nodes = old_state_cache.skip_nodes
      session.set_state(old_state_cache.state)
      return session
    else:
      for subset in self._arg_subset_sorted_by_idx(args):
        subset_frozen = frozenset(subset.items())
        if subset_frozen not in self._state_cache:
          break
        old_state_cache = self._get_state_cache(subset_frozen)

      session.set_state(old_state_cache.state)
      self._skip_nodes = old_state_cache.skip_nodes
      return session

  def stream(self, **kwargs):
    return super()._stream(
      session=self._load_gen_session(args=kwargs.get("args")), **kwargs
    )

  def call(self, **kwargs):
    return super()._call(
      session=self._load_gen_session(args=kwargs.get("args")), **kwargs
    )


@dataclass
class LDResult:
  """
  Class for storing the results of inference.
  
  Attributes:
    returns: Mapping of return keys to return values
    prompt_tokens: Number of tokens injected to the language model
    completion_tokens: Number of tokens generated by the language model
  """

  returns: Dict[str, Any]
  prompt_tokens: int
  completion_tokens: int

  def __init__(self):
    self.returns = {}
    self.prompt_tokens = 0
    self.completion_tokens = 0
