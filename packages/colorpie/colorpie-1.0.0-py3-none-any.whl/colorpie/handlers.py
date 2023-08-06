# -*- coding: UTF-8 -*-

from os import environ
from string import Template
from typing import Union, Tuple, List, Any

from .constants import ESCAPE, RESET

__all__ = ["Style4Bit"]


class Style4Bit(object):
    """
    Colorise text (16-color mode).
    https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit

    Available colours:
        - black: 30
        - red: 31
        - green: 32
        - yellow: 33
        - blue: 34
        - magenta: 35
        - cyan: 36
        - white: 37
        - bright black: 90
        - bright red: 91
        - bright green: 92
        - bright yellow: 93
        - bright blue: 94
        - bright magenta: 95
        - bright cyan: 96
        - bright white: 97

    Available highlights:
        - black: 40
        - red: 41
        - green: 42
        - yellow: 43
        - blue: 44
        - magenta: 45
        - cyan: 46
        - white: 47
        - bright black: 100
        - bright red: 101
        - bright green: 102
        - bright yellow: 103
        - bright blue: 104
        - bright magenta: 105
        - bright cyan: 106
        - bright white: 107

    Available attributes:
        - reset: 0
        - bold: 1 (or increased intensity)
        - dark: 2
        - italic: 3 (not widely supported)
        - underline: 4
        - slow blink: 5 (not widely supported)
        - rapid blink: 6 (not widely supported)
        - reverse: 7 (swap foreground and background colors)
        - concealed: 8 (not widely supported.)

    Example:

        from colorpie import Style4Bit \n
        from colorpie.constants COLORS, HIGHLIGHTS, ATTRIBUTES as ATTRS \n

        style = Style4Bit(
            color=COLORS.RED,
            highlight=HIGHLIGHTS.BLACK,
            attributes=[ATTRS.BOLD, ATTRS.SLOW_BLINK]
        )

        print(style.format('Hello, World!'))
    """

    @staticmethod
    def _type_name(value: Any) -> str:
        return type(value).__name__

    @staticmethod
    def _join(style: int, text: str) -> str:
        return f"{ESCAPE}{style}m{text}"

    def __init__(self, color: int = None, highlight: int = None, attributes: Union[int, Tuple[int], List[int]] = None):
        self._template: Template = self._as_template(color, highlight, attributes)

    def _as_template(self, color: int, highlight: int, attributes: Union[int, Tuple[int], List[int]]) -> Template:
        text: str = "${text}"

        if color is not None:
            self._check_color(color)
            text = self._join(color, text)

        if highlight is not None:
            self._check_highlight(highlight)
            text = self._join(highlight, text)

        if attributes is not None:
            attributes: Tuple[int] = self._check_attributes(attributes)
            for attr in attributes:
                text = self._join(attr, text)

        if text.startswith(ESCAPE):
            return Template(f"{text}{RESET}")

        return Template(text)

    def _check_color(self, value: int) -> int:
        if not isinstance(value, int):
            self._raise_for_error("color", value)
        return value

    def _check_highlight(self, value: int) -> int:
        if not isinstance(value, int):
            self._raise_for_error("highlight", value)
        return value

    def _check_attributes(self, args: Union[int, Tuple[int], List[int]]) -> Tuple[int]:
        if isinstance(args, int):
            return (args,)

        if isinstance(args, (tuple, list)):
            return tuple(set(self._check_attribute(item) for item in args))

        raise TypeError(
            f"Formatting 'attributes' must be of type 'int', 'list[int]' or "
            f"'tuple[int]' not '{self._type_name(args)}'!"
        )

    def _check_attribute(self, value: int) -> int:
        if not isinstance(value, int):
            self._raise_for_error("attribute", value)
        return value

    def _raise_for_error(self, name: str, value: Any):
        raise TypeError(
            f"Formatting '{name}' code must be of "
            f"type 'int' not '{self._type_name(value)}'!"
        )

    def format(self, text: str) -> str:
        if ("NO_COLOR" in environ) or ("ANSI_COLORS_DISABLED" in environ):
            return text
        return self._template.substitute(text=text)
