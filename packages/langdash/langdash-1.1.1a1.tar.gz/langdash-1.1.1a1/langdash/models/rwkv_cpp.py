from typing import Generator, List, Optional, Tuple, Union, Dict
from math import inf
from dataclasses import dataclass
import copy

from langdash.response import RespInfer
from langdash.llm import LLM
from langdash.llm_session import LLMGenerationSessionForRawText, LLMState
from langdash.infer import InferArgs
import langdash.sampling as sampling
import langdash.models._bpe as bpe

import os
import sys
import torch
import pathlib

_rwkv_lib: Optional[str] = None

RWKV_CPP_COMMIT = "9e2a0de8436a956c5ef80fbd5f4184311a7a568d"


def _load_rwkv_import():
  global _rwkv_lib

  import subprocess
  import shutil

  import langdash
  rwkv_cpp_folder = os.path.join(
    os.path.dirname(langdash.__file__), "extern/rwkv.cpp"
  )

  if not os.path.isdir(rwkv_cpp_folder):
    print("rwkv.cpp isn't installed, clone and install? (requires git, cmake)")
    do_install = input("Type 'y' (without quotes) to install: ") == "y"
    if not do_install:
      raise ImportError("rwkv.cpp is not installed")

    os.makedirs(rwkv_cpp_folder, exist_ok=True)
    git = shutil.which("git")
    if git is None:
      raise ImportError("git is needed for compiling rwkv.cpp")
    subprocess.check_call(
      [
        git, "clone", "--recursive", "https://github.com/saharNooby/rwkv.cpp",
        rwkv_cpp_folder
      ]
    )
    subprocess.check_call(
      [git, "checkout", RWKV_CPP_COMMIT], cwd=rwkv_cpp_folder
    )
    subprocess.check_call([git, "submodule", "update"], cwd=rwkv_cpp_folder)

  if "win32" in sys.platform or "cygwin" in sys.platform:
    file_name = "rwkv.dll"
  elif "darwin" in sys.platform:
    file_name = "librwkv.dylib"
  else:
    file_name = "librwkv.so"

  _rwkv_lib = os.path.join(rwkv_cpp_folder, file_name)

  if not os.path.isfile(_rwkv_lib):
    cmake = shutil.which("cmake")
    if cmake is None:
      raise ImportError("cmake is needed for compiling rwkv.cpp")
    subprocess.check_call([cmake, "."], cwd=rwkv_cpp_folder)
    subprocess.check_call(
      [cmake, "--build", ".", "--config", "Release"], cwd=rwkv_cpp_folder
    )
  sys.path.append(os.path.join(rwkv_cpp_folder, "rwkv"))


_load_rwkv_import()

import tokenizers  # type: ignore
import rwkv_cpp_model  # type: ignore
import rwkv_cpp_shared_library  # type: ignore


@dataclass
class RwkvCppState(LLMState):
  _logits: Optional[torch.Tensor] = None
  _state: Optional[torch.Tensor] = None
  _next_token: Optional[Tuple[int, str]] = None


@dataclass
class RwkvCppExtras:
  tokenizer: tokenizers.Tokenizer
  vocab: Dict[str, int]


class RwkvCppSession(
  LLMGenerationSessionForRawText["RwkvCppModel", RwkvCppState, torch.Tensor]
):
  """
  Session for rwkv.cpp model.
  """

  _rwkv: rwkv_cpp_model.RWKVModel
  _tokenizer: tokenizers.Tokenizer

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    def load_model(llm: RwkvCppModel):
      assert _rwkv_lib is not None
      model = rwkv_cpp_model.RWKVModel(
        rwkv_cpp_shared_library.RWKVSharedLibrary(_rwkv_lib), llm._model_path
      )
      tokenizer = tokenizers.Tokenizer.from_file(llm._tokenizer_path)
      extras = RwkvCppExtras(
        tokenizer=tokenizer,
        vocab={
          bpe.decode(logits_tokstr): logits_tokid
          for logits_tokstr, logits_tokid in tokenizer.get_vocab().items()
        }
      )
      return model, extras

    self._rwkv, self._extras = self._ld._get_model_internal(
      self._llm, load_model
    )
    self._logits, self._state = None, None
    self._next_token = None

  def _eval(self, tokid: int) -> torch.Tensor:
    self._logits, self._state = self._rwkv.eval(tokid, self._state)
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
    return self._extras.tokenizer.encode(
      text, add_special_tokens=add_special_tokens
    ).ids

  def decode(self, tokids: List[int]) -> str:
    return self._extras.tokenizer.decode(tokids)

  def next_token_probs(self) -> List[float]:
    if self._next_token is None:
      if self._logits is None:
        raise ValueError("cannot predict next probability for empty input")
      logits = self._logits
    else:
      logits, _ = self._rwkv.eval(self._next_token[0], self._state)
    return sampling.logits_to_probs(logits).tolist()

  def _infer(self, end: Optional[Union[str, int]],
             args: InferArgs) -> Generator[RespInfer, None, None]:
    generated = ""
    ctx: List[int] = []
    buffered_tokens: List[int] = []

    assert args.min_new_tokens >= 0, "min_new_tokens must be at least 0"

    if isinstance(end, str):
      if len(end) == 0:
        end = 0
      elif args.min_new_tokens > 0:
        endtoks = self.tokenize(end)
        assert len(endtoks) == 1
        end = endtoks[0]

    if self._logits is None:
      raise ValueError("no prompt provided for RwkvCppModel")

    for i in range(args.max_new_tokens):
      strip_left = None

      if i == 0 and self._next_token is not None:
        tokid, tokstr = self._next_token

        for logits_tokstr, logits_tokid in self._extras.vocab.items():
          if not logits_tokstr.startswith(tokstr):
            self._logits[logits_tokid] = -inf

        if self._logits.isinf().all():
          # we don't need to heal tokens because no token that begins with _next_token
          self._logits, self._state = self._rwkv.eval(tokid, self._state)
        else:
          strip_left = tokstr

        self._next_token = None

      if end != 0:  # no early endoftext
        self._logits[0] = -inf
      elif args.min_new_tokens > 0 and i < args.min_new_tokens:
        self._logits[end] = -inf

      tokid = sampling.sample(self._logits, args, ctx)
      ctx.append(tokid)

      if tokid == end:  # implies end is int
        break

      tokstr = self._extras.tokenizer.decode([tokid])

      if "\ufffd" in tokstr:
        buffered_tokens.append(tokid)
        self._next_token = (tokid, "")
      else:
        if buffered_tokens:
          tokstr = self._extras.tokenizer.decode(buffered_tokens)
          tokstr += self._extras.tokenizer.decode([tokid])
          buffered_tokens.clear()
        else:
          if strip_left and tokstr.startswith(strip_left):
            tokstr = tokstr[len(strip_left):]

        self._next_token = (tokid, tokstr)

        generated += tokstr
        if isinstance(end, str) and end and generated.endswith(end):
          generated = generated[:-len(end)]
          break

        yield RespInfer(tokid=tokid, tokstr=tokstr, running_infer=generated)

      self._logits, self._state = self._rwkv.eval(tokid, self._state)

    if buffered_tokens:
      generated += self._extras.tokenizer.decode(buffered_tokens)
    yield RespInfer(tokid=-1, tokstr="", running_infer=generated)


class RwkvCppModel(LLM[RwkvCppSession]):
  """
  rwkv.cpp model
  """

  Session = RwkvCppSession

  def __init__(self, model_path: str, tokenizer_path: Optional[str] = None):
    """
    Creates a template for the RWKV language model (using the rwkv.cpp library).
    
    Args:
      model_path (str): Path to the model file.
      tokenizer_path (Optional[str]):
        Path to the tokenizer file.
        If None is given, the tokenizer is assumed to be the model_path / '20B_tokenizer.json'.
    """
    self._model_path = model_path
    if tokenizer_path is None:
      self._tokenizer_path = str(
        pathlib.Path(os.path.abspath(model_path)).parent / "20B_tokenizer.json"
      )
    else:
      self._tokenizer_path = tokenizer_path
