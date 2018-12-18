from enum import Enum


class Color(Enum):
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)
    DARK_GRAY = (50, 50, 50)
    WHITE = (240, 240, 240)
    RED = (240, 10, 10)
    DARK_RED = (200, 10, 10)
    GREEN = (10, 240, 100)


class ColorRole(Enum):
    Background = 0
    Foreground = 1
    Text = 2