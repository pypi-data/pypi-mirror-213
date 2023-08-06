from typing import List, Optional, Tuple
from dataclasses import dataclass
import copy
import os
import sys
import torch
import tokenizers  # type: ignore

from langdash.llm import LLM
from langdash.llm_session import LLMGenerationSessionForRawText, LLMState
import langdash.sampling as sampling
import langdash.models._bpe as bpe
from ._tokenizer.rwkv_20b_tokenizer import Rwkv20BTokenizer
from ._mixins.tensor_based_infer_mixin import TensorBasedInferMixin

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
          git, "clone", "--recursive",
          "https://github.com/saharNooby/rwkv.cpp", _rwkv_cpp_folder
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

  def eval(self, tokid, state) -> Tuple[torch.Tensor, torch.Tensor]:
    return self.model.eval(tokid, state)


class RwkvCppSession(
  TensorBasedInferMixin,
  LLMGenerationSessionForRawText["RwkvCppModel", RwkvCppState, torch.Tensor]
):
  """
  Session for rwkv.cpp model.
  """

  _logits: Optional[torch.Tensor]
  _state: Optional[torch.Tensor]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    def load_model(llm: RwkvCppModel):
      return RwkvCppWrapper(llm)

    self._model = self._ld._get_model_internal(self._llm, load_model)
    self._logits, self._state = None, None
    self._next_token = None

  def _eval(self, tokid: int) -> torch.Tensor:
    self._logits, self._state = self._model.eval(tokid, self._state)
    # FIXME: mypy does not infer self._logits to not be None
    return self._logits  # type: ignore

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
      assert _rwkv_cpp_folder is not None
      self._tokenizer_path = os.path.join(
        _rwkv_cpp_folder, builtin_tokenizer_paths[self._tokenizer_type]
      )
    else:
      self._tokenizer_path = tokenizer_path
