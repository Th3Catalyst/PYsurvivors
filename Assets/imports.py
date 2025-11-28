from typing import Tuple, Iterable
import pygame
import math
from enum import Enum
class globs(Enum):
    Number = int|float
    playerObj = None
    def __or__(self, other) -> Enum | None:
        if isinstance(other, globs):
            return globs
