#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""Functions for working with Unicode characters, codepoints, and surrogate pairs."""

from __future__ import annotations
import unicodedata

INVISIBLE_CHARS: set[str] = {
    "\u034F",
    "\u115F",
    "\u1160",
    "\u17B4",
    "\u17B5",
    "\u2800",
    "\u3164",
    "\uFFA0",
    "\U0001D159",
    "\U0001d173",
    "\U0001d174",
    "\U0001d175",
    "\U0001d176",
    "\U0001d177",
    "\U0001d178",
    "\U0001d179",
    "\U0001d17a",
}
"""A set of characters that normally do not appear under most fonts."""


def char_to_surrogates(char: str) -> tuple[int, int]:
    r"""
    Convert one character into 2 integers of its UTF-16 surrogate codepoints.

    A surrogate pair are two characters that represent another character.
    Since UTF-16 only stores characters from 0 to 0xFFFF,
    chars past 0xFFFF need to be split into two codepoints below 0xFFFF.

    This is useful even in plaintext Unicode notation, because ``\u1D105`` is not a single
    character, it's two (``ᴐ5``, not ``𝄅``).

    :param char:
        A single character.
    :returns:
        A surrogate pair, in codepoints of the surrogates.
    """
    codepoint = ord(char)
    codepoint -= 0x10000
    return 0xD800 + (codepoint >> 10), 0xDC00 + (codepoint & 0x3FF)


def surrogates_to_char(surrogates: tuple[int, int]) -> str:
    """
    Given a tuple of surrogate chars, return the single codepoint they combine to.

    :param surrogates:
        A tuple of two surrogate codepoints.
    :returns:
        A single character of the resulting surrogates.
    """
    return chr((surrogates[0] - 0xD800) * 0x400 + (surrogates[1] - 0xDC00) + 0x10000)


def is_char_invisible(char: str) -> bool:
    """
    Return if `char` would be invisible (might not have glyph info).

    A character is "invisible" if it:

    * Is in these categories: ``Cf, Cc, Zl, Zs, Zp``.
    * | Is equal to these codepoints:
      | ``2800, 034F, 115F, 1160, 17B4, 17B5, 3164, FFA0, 1D159, 1D174, 1D176, 1D177, 1D178, 1D17A``.
    * Is private use.

    You can visit `<https://invisible-characters.com/>`_ if you would like to see the list.

    .. warning::
        "Invisibility" is not a valid Unicode standard property.
        Do use utilize it outside this application for standardization purposes.

    :param char:
        A single character.
    :returns:
        If `char` is a spacing character.
    """
    return (
        unicodedata.category(char) in ("Cf", "Cc", "Zl", "Zs", "Zp")
        or char in INVISIBLE_CHARS
        or is_char_private_use(char)
    )


def is_char_private_use(char: str) -> bool:
    """
    Return if `char` is in a Private Use Area (PUA).

    A PUA is one of these codepoint ranges:

    * U+E000 to U+F8FF
    * U+F0000 to U+FFFFD
    * U+100000 to U+10FFFD

    :param char:
        A single character.
    :returns:
        If `char` is in a Private Use Area.
    """
    codepoint = ord(char)
    return (0xE000 <= codepoint <= 0xF8FF) or (0xF0000 <= codepoint <= 0xFFFFD) or (0x100000 <= codepoint <= 0x10FFFD)


def str_to_tags(string: str) -> str:
    """
    | Given `string`, which should have only ASCII characters, turn it into that
    | same string but every character is a Tag of itself, instead.

    See https://en.wikipedia.org/wiki/Tags_(Unicode_block).

    :param string: Any string; it should have ASCII characters.
    :returns: `string` but with ASCII characters replaced with their Tag equivalents.
    """
    return "".join(chr(ord(ch) + 0xE0000) for ch in string if ord(ch) < 0x7F)


def pretty_print_char(char: str) -> str:
    r"""
    Return relevant info about a character into a string, following ``U+<codepoint> <name> <character>``.

    >>> pretty_print_char('\u2601')
    'U+2601: CLOUD ☁'
    >>> pretty_print_char('\ue000')
    'U+E000: <PRIVATE USE> \ue000'
    >>> pretty_print_char('\U0001f400')
    'U+1F400: RAT 🐀'
    >>> pretty_print_char('\b')
    'U+0008: BACKSPACE ␈'
    >>> pretty_print_char('\b')
    'U+0008: BACKSPACE ␈'

    :param char: A single character.
    :returns: The pretty character string.
    """
    codepoint = ord(char)
    try:
        if unicodedata.category(char) == "Cc":
            return (
                f"U+{codepoint:04X}: "
                f"{unicodedata.name(chr(ord(char) + 0x2400)).split('SYMBOL FOR ')[1]} "
                f"{chr(ord(char) + 0x2400)}"
            )
        return f"U+{codepoint:04X}: {unicodedata.name(char)} {char}"
    except (ValueError, IndexError):
        if is_char_private_use(char):
            return f"U+{codepoint:04X}: <PRIVATE USE> {char}"
        return f"U+{codepoint:04X}: {char}"
