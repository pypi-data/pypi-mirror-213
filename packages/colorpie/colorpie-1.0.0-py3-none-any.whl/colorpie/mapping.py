# -*- coding: UTF-8 -*-

from dataclasses import dataclass, field

__all__ = [
    "Attributes",
    "Color",
    "Colors",
]


@dataclass
class Attributes(object):
    RESET: int = field(default=0)
    BOLD: int = field(default=0)
    DARK: int = field(default=0)
    ITALIC: int = field(default=0)
    UNDERLINE: int = field(default=0)
    SLOW_BLINK: int = field(default=0)
    RAPID_BLINK: int = field(default=0)
    REVERSE: int = field(default=0)
    CONCEALED: int = field(default=0)


@dataclass
class Color(object):
    BLACK: int = field(default=0)
    RED: int = field(default=0)
    GREEN: int = field(default=0)
    YELLOW: int = field(default=0)
    BLUE: int = field(default=0)
    MAGENTA: int = field(default=0)
    CYAN: int = field(default=0)
    WHITE: int = field(default=0)


@dataclass
class Colors(Color):
    BRIGHT: Color = field(default_factory=Color)
