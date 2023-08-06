from typing import Generator, List, Optional, Tuple, Union, Dict, Any
from math import inf
from dataclasses import dataclass
import copy
import os
import sys
import torch
import tokenizers

from langdash.response import RespInfer
from langdash.llm import LLM
from langdash.llm_session import LLMGenerationSessionForRawText, LLMState
from langdash.infer import InferArgs
import langdash.sampling as sampling
import langdash.models._bpe as bpe
from ._tokenizer.tokenizer import Tokenizer, BufferedToken
from ._tokenizer.rwkv_20b_tokenizer import Rwkv20BTokenizer

_rwkv_lib: Optional[str] = None
_rwkv_cpp_folder: Optional[str] = None

RWKV_CPP_COMMIT_DEFAULT = "82c4ac78f4d10ef1af87104fc051ea2119eaaddf"
RWKV_CPP_COMMIT = os.environ.get(
  "LANGDASH_RWKV_CPP_COMMIT", RWKV_CPP_COMMIT_DEFAULT
)
RWKV_CPP_FORCE_RECOMPILE = os.environ.get(
  "LANGDASH_RWKV_FORCE_RECOMPILE", ""
) == "1"


def _load_rwkv_import():
  global _rwkv_lib, _rwkv_cpp_folder

  import subprocess
  import shutil

  import langdash
  _rwkv_cpp_folder = os.path.join(
    os.path.dirname(langdash.__file__), "extern/rwkv.cpp"
  )

  force_recompile = RWKV_CPP_FORCE_RECOMPILE

  git = shutil.which("git")

  if not os.path.isdir(_rwkv_cpp_folder):
    print("rwkv.cpp isn't installed, clone and install? (requires git, cmake)")
    do_install = input("Type 'y' (without quotes) to install: ") == "y"
    if not do_install:
      raise ImportError("rwkv.cpp is not installed")
    if git is None:
      raise ImportError("git is needed for compiling rwkv.cpp")

    os.makedirs(_rwkv_cpp_folder, exist_ok=True)

    if not os.path.isdir(_rwkv_cpp_folder):
      subprocess.check_call(
        [
          git, "clone", "--recursive", "https://github.com/saharNooby/rwkv.cpp",
          _rwkv_cpp_folder
        ]
      )
    subprocess.check_call(
      [git, "checkout", RWKV_CPP_COMMIT], cwd=_rwkv_cpp_folder
    )
    subprocess.check_call([git, "submodule", "update"], cwd=_rwkv_cpp_folder)

  elif git is not None:
    current_commit = subprocess.check_output(
      [git, "rev-parse", "HEAD"], cwd=_rwkv_cpp_folder, encoding="utf-8"
    ).strip()
    if current_commit != RWKV_CPP_COMMIT:
      subprocess.check_call(
        [git, "pull", "origin", "master"], cwd=_rwkv_cpp_folder
      )
      subprocess.check_call(
        [git, "checkout", RWKV_CPP_COMMIT], cwd=_rwkv_cpp_folder
      )
      subprocess.check_call([git, "submodule", "update"], cwd=_rwkv_cpp_folder)
      force_recompile = True

  if force_recompile:
    try:
      os.unlink(os.path.join(_rwkv_cpp_folder, "CMakeCache.txt"))
    except FileNotFoundError:
      pass

  if "win32" in sys.platform or "cygwin" in sys.platform:
    file_name = "rwkv.dll"
  elif "darwin" in sys.platform:
    file_name = "librwkv.dylib"
  else:
    file_name = "librwkv.so"

  _rwkv_lib = os.path.join(_rwkv_cpp_folder, file_name)

  if force_recompile or not os.path.isfile(_rwkv_lib):
    cmake = shutil.which("cmake")
    if cmake is None:
      raise ImportError("cmake is needed for compiling rwkv.cpp")
    subprocess.check_call([cmake, "."], cwd=_rwkv_cpp_folder)
    subprocess.check_call(
      [cmake, "--build", ".", "--config", "Release"], cwd=_rwkv_cpp_folder
    )

  sys.path.insert(0, os.path.join(_rwkv_cpp_folder, "rwkv"))


_load_rwkv_import()

import rwkv_cpp_model  # type: ignore
import rwkv_cpp_shared_library  # type: ignore

try:
  import rwkv_tokenizer  # type: ignore
  _rwkv_tokenizer_available = True
except ModuleNotFoundError:
  _rwkv_tokenizer_available = False

sys.path.pop(0)


@dataclass
class RwkvCppState(LLMState):
  _logits: Optional[torch.Tensor] = None
  _state: Optional[torch.Tensor] = None
  _next_token: Optional[Tuple[int, str]] = None


class RwkvCppWrapper:

  def __init__(self, llm: "RwkvCppModel"):
    assert _rwkv_lib is not None
    self.model = rwkv_cpp_model.RWKVModel(
      rwkv_cpp_shared_library.RWKVSharedLibrary(_rwkv_lib), llm._model_path
    )
    if llm._tokenizer_type == "20B":
      tokenizer = tokenizers.Tokenizer.from_file(llm._tokenizer_path)
    elif llm._tokenizer_type == "world":
      tokenizer = rwkv_tokenizer.TRIE_TOKENIZER(llm._tokenizer_path)
    else:
      raise ValueError(f"unknown tokenizer type {llm._tokenizer_type}")
    vocab = {
      bpe.decode(logits_tokstr): logits_tokid
      for logits_tokstr, logits_tokid in tokenizer.get_vocab().items()
    }
    self.tokenizer = Rwkv20BTokenizer(tokenizer, vocab)
    self.eos_token = 0

  def eval(self, tokid, state):
    return self.model.eval(tokid, state)


class RwkvCppSession(
  LLMGenerationSessionForRawText["RwkvCppModel", RwkvCppState, torch.Tensor]
):
  """
  Session for rwkv.cpp model.
  """

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    def load_model(llm: RwkvCppModel):
      return RwkvCppWrapper(llm)

    self._model = self._ld._get_model_internal(self._llm, load_model)
    self._logits, self._state = None, None
    self._next_token = None

  def _eval(self, tokid: int) -> torch.Tensor:
    self._logits, self._state = self._model.eval(tokid, self._state)
    return self._logits

  def set_state(self, state: Optional[RwkvCppState]):
    if state is None:
      self._logits, self._state = None, None
      self._next_token = None
    else:
      self._logits = copy.deepcopy(state._logits)
      self._state = copy.deepcopy(state._state)
      self._next_token = state._next_token

  def clone_state(self) -> RwkvCppState:
    return RwkvCppState(
      _logits=copy.deepcopy(self._logits),
      _state=copy.deepcopy(self._state),
      _next_token=self._next_token,
    )

  def tokenize(self, text: str, add_special_tokens: bool = False) -> List[int]:
    return self._model.tokenizer.encode(
      text, add_special_tokens=add_special_tokens
    )

  def decode(self, tokids: List[int]) -> str:
    return self._model.tokenizer.decode(tokids)

  def _next_token_logits_raw(self):
    if self._next_token is None:
      if self._logits is None:
        raise ValueError("cannot predict next probability for empty input")
      logits = self._logits
    else:
      logits, _ = self._model.eval(self._next_token[0], self._state)
    return logits

  def next_token_logits(self) -> List[float]:
    return self._next_token_logits_raw().tolist()

  def next_token_probs(self) -> List[float]:
    return sampling.logits_to_probs(self._next_token_logits_raw()).tolist()

  def _infer(self, end: Optional[Union[str, int]],
             args: InferArgs) -> Generator[RespInfer, None, None]:
    generated = ""
    buffered_tokens: Optional[BytesDictBufferedToken] = None
    ctx = []

    if isinstance(end, str):
      if len(end) == 0:
        end = self._model.eos_token
      elif args.min_new_tokens > 0:
        endtoks = self.tokenize(end)
        assert len(endtoks) == 1
        end = endtoks[0]

    if self._logits is None:
      raise ValueError("no prompt provided for LlamaCppModel")

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

      if tokid == end:  # implies end is int
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


class RwkvCppModel(LLM[RwkvCppSession]):
  """
  rwkv.cpp model
  """

  Session = RwkvCppSession

  def __init__(
    self,
    model_path: str,
    tokenizer_path: Optional[str] = None,
    tokenizer_type: str = "20B"
  ):
    """
    Creates a template for the RWKV language model (using the rwkv.cpp library).
    
    Args:
      model_path (str): Path to the model file.
      tokenizer_path (Optional[str]):
        Path to the tokenizer file.
        Defaults to `None`. If not set, the built-in tokenizer will be used.
      tokenizer_type (str):
        The type of tokenizer to use. Either `"world"` for world models or `"20B"` for anything else.
    """
    self._model_path = model_path
    self._tokenizer_type = tokenizer_type
    if not _rwkv_tokenizer_available and self._tokenizer_type != "20B":
      raise ValueError("old RWKV tokenizer only supports 20B")
    if tokenizer_path is None:
      builtin_tokenizer_paths = {
        "world": "rwkv/rwkv_vocab_v20230424.txt",
        "20B": "rwkv/20B_tokenizer.json",
      }
      self._tokenizer_path = str(
        os.path.join(
          _rwkv_cpp_folder, builtin_tokenizer_paths[self._tokenizer_type]
        )
      )
    else:
      self._tokenizer_path = tokenizer_path
