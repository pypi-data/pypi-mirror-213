# -*- coding: UTF-8 -*-

from sys import version_info

from .mapping import Attributes, Color, Colors

__all__ = [
    "ATTRIBUTES",
    "COLORS",
    "HIGHLIGHTS",
    "ESCAPE",
    "RESET",
]

ATTRIBUTES: Attributes = Attributes(
    RESET=0,
    BOLD=1,  # or increased intensity
    DARK=2,
    ITALIC=3,  # not widely supported
    UNDERLINE=4,
    SLOW_BLINK=5,  # not widely supported
    RAPID_BLINK=6,  # not widely supported
    REVERSE=7,  # swap foreground and background colors
    CONCEALED=8,  # not widely supported.
)

COLORS: Colors = Colors(
    BLACK=30,
    RED=31,
    GREEN=32,
    YELLOW=33,
    BLUE=34,
    MAGENTA=35,
    CYAN=36,
    WHITE=37,
    BRIGHT=Color(
        BLACK=90,
        RED=91,
        GREEN=92,
        YELLOW=93,
        BLUE=94,
        MAGENTA=95,
        CYAN=96,
        WHITE=97,
    )
)

HIGHLIGHTS: Colors = Colors(
    BLACK=40,
    RED=41,
    GREEN=42,
    YELLOW=43,
    BLUE=44,
    MAGENTA=45,
    CYAN=46,
    WHITE=47,
    BRIGHT=Color(
        BLACK=100,
        RED=101,
        GREEN=102,
        YELLOW=103,
        BLUE=104,
        MAGENTA=105,
        CYAN=106,
        WHITE=107,
    )
)

ESCAPE: str = "\x1b[" if version_info.major > 2 else "\033["

RESET: str = f"{ESCAPE}{ATTRIBUTES.RESET}m"
