"""
This module contains utilities.
"""

from enum import Enum

from .array import Array


class Directions(Enum):
    up = Array(0, 1)
    down = Array(0, -1)
    left = Array(-1, 0)
    right = Array(1, 0)
