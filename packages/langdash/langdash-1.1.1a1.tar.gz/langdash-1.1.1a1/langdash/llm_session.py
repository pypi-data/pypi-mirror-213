from typing import TypeVar, Generic, Optional, List, Generator, Union, Tuple, TYPE_CHECKING
import copy

from langdash.response import RespInfer
from langdash.chains import CalledChain, LDNodeArgs, LDNode
from langdash.infer import InferArgs
from langdash.llm import LLM

if TYPE_CHECKING:
  from langdash.core import Langdash

T_LLM = TypeVar("T_LLM", bound=LLM)


class LLMSession(Generic[T_LLM]):
  """
  Base class for a session for a language model.
  """

  def __init__(self, llm: T_LLM, ld: "Langdash"):
    self._ld = ld
    self._llm = llm

  def clone(self) -> "LLMSession":
    """
    Clone the current session.
    """
    raise NotImplementedError("clone")


class LLMState:
  """
  A state class for a language model.
  """
  pass


T_LLMState = TypeVar("T_LLMState", bound=LLMState)


class LLMGenerationSession(LLMSession, Generic[T_LLM, T_LLMState]):
  """ Generation session for a language model. """

  def __init__(
    self,
    llm: T_LLM,
    ld: "Langdash",
    default_infer_args: InferArgs = InferArgs(),
    track_called_chains: bool = True,
    token_healing: bool = True,
    global_args: LDNodeArgs = {}
  ):
    super().__init__(llm, ld)
    self.default_infer_args = default_infer_args
    self.called_chains: Optional[List[CalledChain]
                                ] = ([] if track_called_chains else None)
    self.token_healing = token_healing
    self.global_args = global_args
    self.tokens_counter = 0

  def set_state(self, state: Optional[T_LLMState]):
    """
    Set the state of the language model.

    Args:
      state (Optional[T_LLMState]):
        The state of the language model, or None to clear the state.
    """
    raise NotImplementedError("set_state")

  def clone_state(self) -> T_LLMState:
    """
    Clone the current state of the language model.
    """
    raise NotImplementedError("clone_state")

  def clone(self) -> "LLMGenerationSession":
    session = self.__class__(
      llm=self._llm,
      ld=self._ld,
      default_infer_args=self.default_infer_args,
      track_called_chains=False,
      token_healing=self.token_healing,
      global_args=copy.copy(self.global_args)
    )
    session.set_state(self.clone_state())
    if self.called_chains is not None:
      session.called_chains = copy.copy(self.called_chains)
    return session

  def _append_called_chain(
    self, node: LDNode, args: LDNodeArgs, tokens_used: int
  ):
    if self.called_chains is None:
      pass
    else:
      self.called_chains.append(
        CalledChain(node=node, args=args, tokens_used=tokens_used)
      )

  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    """
    Tokenize the given text into a list of tokens.

    Args:
      text (str): The text to tokenize.
      add_special_tokens (bool): Whether to add special tokens to the output.

    Returns:
      (List[int]) The list of tokens.
    """
    raise NotImplementedError("tokenize")

  def decode(self, tokids: List[int]) -> str:
    raise NotImplementedError("decode")

  def next_token_probs(self) -> List[float]:
    """
    Returns the probabilities for next token.
    """
    raise NotImplementedError("next_token_probs")

  def flush_token(self):
    raise NotImplementedError("flush_token")

  def _infer(self, end: Optional[Union[str, int]],
             args: InferArgs) -> Generator[RespInfer, None, None]:
    raise NotImplementedError("_infer")

  def infer(
    self,
    end: Optional[Union[str, int]],
    args: Optional[InferArgs] = None
  ) -> Generator[RespInfer, None, None]:
    """
    Infer the next token from the input sequence.

    Args:
      end (Optional[Union[str, int]]):
        The end of the output sequence.
        If set to None, the output sequence will be generated until the maximum number of tokens is reached.
      args (Optional[InferArgs]):
        Optionak inference parameters.
        
    Returns:
      Inference response
    """
    if not args:
      args = self.default_infer_args
    yield from self._infer(end, args)

  def inject(
    self, text: Union[str, int], add_special_tokens: bool = False
  ) -> int:
    raise NotImplementedError("inject")


T_Tensor = TypeVar("T_Tensor")


class LLMGenerationSessionForRawText(
  LLMGenerationSession, Generic[T_LLM, T_LLMState, T_Tensor]
):
  """ Generation session for a language model that processes raw text. """

  _logits: Optional[T_Tensor]
  _next_token: Optional[Tuple[int, str]]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._logits = None
    self._next_token = None

  def _eval(self, tokid: int) -> T_Tensor:
    raise NotImplementedError("_eval")

  def _eval_mult(self, tokens: List[int]):
    assert tokens, "tokens must not be empty"
    for tokid in tokens:
      logits = self._eval(tokid)
    return logits

  def flush_token(self):
    """
    Flushes the previous token into the language model if healing is enabled.
    
    **Warning:** unexpected behavior if the previous token is a "boundary" token
    like spaces.
    """
    if self._next_token is None:
      return
    self.inject(self._next_token[0])
    self._next_token = None

  def next_token_probs(self, *args, **kwargs) -> List[float]:
    raise NotImplementedError("next_token_probs")

  def _on_first_inject(self):
    return

  def inject(
    self, text: Union[str, int], add_special_tokens: bool = False
  ) -> int:
    if isinstance(text, str):
      tokens = self.tokenize(text, add_special_tokens=add_special_tokens)
    else:
      tokens = [text]
    if not tokens:
      return 0

    if self._logits is None:
      self._on_first_inject()

    num_toks = 0

    if self.token_healing:
      if self._next_token is not None:
        tokid, _ = self._next_token
        tokens = self.tokenize(
          self.decode([tokid, *tokens]), add_special_tokens=add_special_tokens
        )
      if len(tokens) > 1:
        self._logits = self._eval_mult(tokens[:-1])
        num_toks += len(tokens) - 1
      self._next_token = (tokens[-1], self.decode([tokens[-1]]))
    else:
      if self._next_token is not None:
        tokid, tokstr = self._next_token
        self._eval(tokid)
        num_toks += 1
      self._logits = self._eval_mult(tokens)
      num_toks += len(tokens)

    return num_toks


T_Embedding = TypeVar("T_Embedding")


class LLMEmbeddingSession(LLMSession, Generic[T_LLM, T_Embedding]):
  """ Session for a language model that outputs an embedding for raw text. """

  def __init__(self, llm: T_LLM, ld: "Langdash"):
    self._ld = ld
    self._llm = llm

  def embedding_size(self) -> int:
    """
    Returns the embedding size of the model.
    """
    raise NotImplementedError("embedding_size")

  def embed(self, documents: List[str]) -> T_Embedding:
    """
    Infer the embedding of a list of text.
    
    Args:
      documents (List[str]): The text to be embedded.
      
    Returns:
      The embedding vector of the text.
    """
    raise NotImplementedError("infer")
