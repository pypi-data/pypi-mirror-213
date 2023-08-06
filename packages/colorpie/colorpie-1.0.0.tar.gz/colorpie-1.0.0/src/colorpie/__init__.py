# -*- coding: UTF-8 -*-

from os import system

from .constants import ATTRIBUTES, COLORS, HIGHLIGHTS
from .handlers import Style4Bit

system("color")

__all__ = [
    "Style4Bit",
    "ATTRIBUTES",
    "COLORS",
    "HIGHLIGHTS",
]
