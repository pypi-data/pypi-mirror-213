from typing import List, Union, Optional, Generator
from .tokenizer import Tokenizer, BufferedToken
from ._bpe import decode as bpe_decode


class HFTokenizer(Tokenizer):
  vocab: List[str]

  def __init__(self, tokenizer):
    self.tokenizer = tokenizer
    assert not self.tokenizer.is_fast
    assert self.tokenizer.errors == "strict"
    if hasattr(self.tokenizer, "bpe"):
      self.vocab = [
        bpe_decode(token) for token in
        self.tokenizer.convert_ids_to_tokens(range(self.tokenizer.vocab_size))
      ]
    else:
      self.vocab = self.tokenizer.convert_ids_to_tokens(
        range(self.tokenizer.vocab_size)
      )

  def encode(self, text: str, add_special_tokens: bool = False) -> List[int]:
    return self.tokenizer.encode(text, add_special_tokens=add_special_tokens)

  def decode(self, tokens: List[int]) -> str:
    return self.tokenizer.decode(tokens)

  def decode_once(self, token: int) -> Union[str, BufferedToken]:
    try:
      return self.tokenizer.decode(token)
    except UnicodeDecodeError:
      return HFBufferedToken(self, token)

  def tokens_starting_with(self, token_id: int) -> Generator[int, None, None]:
    try:
      tokstr = self.tokenizer.decode(token_id)
      for logits_tokid, logits_tokstr in enumerate(self.vocab):
        if not logits_tokstr.startswith(tokstr):
          yield logits_tokid
    except UnicodeDecodeError:
      return


class HFBufferedToken(BufferedToken):

  def __init__(self, tokenizer: HFTokenizer, token_id: int):
    self.tokenizer = tokenizer
    self.tokens: List[int] = [token_id]

  def add_token_id(self, token_id: int) -> Optional[str]:
    self.tokens.append(token_id)
    try:
      return self.tokenizer.decode(self.tokens)
    except UnicodeDecodeError:
      return None

  def flush(self) -> str:
    return ""
