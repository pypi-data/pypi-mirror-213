# Copyright 2018 The Open AI Team Authors and The HuggingFace Inc. team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Extracted from transformers/src/transformers/models/gpt2/tokenization_gpt2.py


def _byte_encode_dict():
  """
  Returns list of utf-8 byte and a mapping to unicode strings. We specifically avoids mapping to whitespace/control
  characters the bpe code barfs on.
  The reversible bpe codes work on unicode strings. This means you need a large # of unicode characters in your vocab
  if you want to avoid UNKs. When you're at something like a 10B token dataset you end up needing around 5K for
  decent coverage. This is a significant percentage of your normal, say, 32K bpe vocab. To avoid that, we want lookup
  tables between utf-8 bytes and unicode strings.
  """
  bs = (
    list(range(ord("!"),
               ord("~") + 1)) + list(range(ord("¡"),
                                           ord("¬") + 1)) +
    list(range(ord("®"),
               ord("ÿ") + 1))
  )
  cs = bs[:]
  n = 0
  for b in range(2**8):
    if b not in bs:
      bs.append(b)
      cs.append(2**8 + n)
      n += 1
  cs = [chr(n) for n in cs]
  return dict(zip(bs, cs))


BYTE_ENCODE_DICT = _byte_encode_dict()
BYTE_DECODE_DICT = {v: chr(k) for k, v in BYTE_ENCODE_DICT.items()}


def decode(s: str) -> str:
  rs = ""
  for c in s:
    rs += BYTE_DECODE_DICT.get(c, c)
  return rs
