
from dataclasses import dataclass
from jsonmathpy.core.types import TokenType


@dataclass
class Token:
    type: TokenType = None
    value: any      = None