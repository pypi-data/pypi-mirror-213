from typing import List, Union, Dict, Optional, Generator
from .tokenizer import Tokenizer, BufferedToken


class Rwkv20BTokenizer(Tokenizer):

  def __init__(self, tokenizer, vocab: Dict[str, int]):
    self.tokenizer = tokenizer
    self.vocab = vocab

  def encode(self, text: str, add_special_tokens: bool = False) -> List[int]:
    return self.tokenizer.encode(
      text, add_special_tokens=add_special_tokens
    ).ids

  def decode(self, tokens: List[int]) -> str:
    return self.tokenizer.decode(tokens)

  def decode_once(self, token_id: int) -> Union[str, BufferedToken]:
    s = self.decode([token_id])
    if "\ufffd" not in s:
      return s
    else:
      return Rwkv20BBufferedToken(self, token_id)

  def tokens_starting_with(self, token_id: int) -> Generator[int, None, None]:
    tokstr = self.decode([token_id])
    for logits_tokstr, logits_tokid in self.vocab.items():
      if not logits_tokstr.startswith(tokstr):
        yield logits_tokid


class Rwkv20BBufferedToken(BufferedToken):

  def __init__(self, tokenizer: Rwkv20BTokenizer, token_id: int):
    self.tokenizer = tokenizer
    self.token_ids = [token_id]

  def add_token_id(self, token_id: int) -> Optional[str]:
    self.token_ids.append(token_id)
    s = self.tokenizer.decode(self.token_ids)
    if "\ufffd" not in s:
      return s
    else:
      return None

  def flush(self) -> str:
    return self.tokenizer.decode(self.token_ids)
