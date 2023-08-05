from dataclasses import dataclass
import warnings


@dataclass
class InferArgs:
  """
  Data class for inference arguments.
  
  Attributes:
    min_new_tokens: Minimum number of new tokens to generate
    max_new_tokens: Maximum number of new tokens to generate
    temperature: Temperature
    top_p: Top-P. If typical sampling isn't used, generation defaults to top-p sampling
    typical_mass: Mass parameter. If set, generation will use typical sampling
    max_rep_ctx: Maximum number of tokens to look back for repetition penalty
    rep_penalty: Repetition penalty, applied to logits for every token
  """
  min_new_tokens: int = 0
  max_new_tokens: int = 512
  temperature: float = 1.0
  top_p: float = 0.
  typical_mass: float = 0.
  max_rep_ctx: int = 64
  rep_penalty: float = 1.0
