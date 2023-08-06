#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Utilities for dealing with .hex glyphs.

This is often used in conjunction with :class:`mcfonts.providers.unihex.UnihexProvider`.
"""
from __future__ import annotations
import collections.abc

import PIL.Image
import PIL.ImageOps


def get_codepoint(hex_glyph: str) -> str:
    """
    Return the character that a .hex glyph is associated with.

    :param hex_glyph: The entire .hex glyph.
    :returns: The character portion of a .hex glyph.
    """
    return chr(int(hex_glyph.split(":", 1)[0], 16))


def get_width(bit_string: str) -> int:
    """
    Return how wide a .hex glyph's bit string is.

    Width is equivalent to ``len(bit_string) // 4``, which can be shortened to ``len(bit_string) >> 2``.

    :param bit_string: The bit string portion of a .hex glyph.
    :returns: The width of the bit string. A power of 2 above or equal to 8.
    """
    return len(bit_string) >> 2


def get_bit_string(hex_glyph: str) -> str:
    """
    Return the "bit string" portion of a .hex glyph. This is the part after the ``:``.

    >>> get_bit_string("0041:0000000018242442427E424242420000")
    '0000000018242442427E424242420000'

    :param hex_glyph: A single .hex glyph.
    :returns: The bit string portion.
    """
    return hex_glyph.split(":", 1)[1]


def bit_string_to_bytes(bit_string: str) -> bytes:
    r"""
    Return `bit_string` but with each set of "bytes" as real bytes.
    For example, "00EA" returns "\\x00\\xEA".

    This is useful for iterating over the pixels of a bit string, or converting to an image.

    >>> bit_string_to_bytes("0000000018242442427E424242420000")
    b'\x00\x00\x00\x00\x18$$BB~BBBB\x00\x00'

    :param bit_string: The bit string.
    :returns: Bytes of the bit string, with each two-character portion translated to their byte representation.
    """
    r = []
    for i in range(0, len(bit_string), 2):
        r.append(int(bit_string[i : i + 2], 16))
    return bytes(r)


def bit_string_to_image(bit_string: str) -> PIL.Image.Image:
    """
    Given `bit_string`, return a :class:`~PIL.Image.Image` that is a 1:1 representation of the glyph.

    :param bit_string: A bit string.
    :returns: An :class:`~PIL.Image.Image` of the bit string.
    """
    return PIL.Image.frombuffer("1", (get_width(bit_string), 16), bit_string_to_bytes(bit_string))


def bit_string_to_rows(bit_string: str, reverse: bool = True) -> collections.abc.Iterable[str]:
    """
    Convert `bit_string` into a yield of strings, with each character in the string being either "1" or "0".

    If `reverse` (the default), the rows will be flipped vertically.

    >>> list(bit_string_to_rows("0000000018242442427E424242420000"))
    [
        '00000000',
        '00000000',
        '01000010',
        '01000010',
        '01000010',
        '01000010',
        '01111110',
        '01000010',
        '01000010',
        '00100100',
        '00100100',
        '00011000',
        '00000000',
        '00000000',
        '00000000',
        '00000000'
    ]


    :param bit_string: The bit string.
    :param reverse:
        Whether to flip the image along the Y-axis.
        This is to match the normal behavior of iterating over the pixels of a :class:`PIL.Image.Image`,
        from the bottom-left to the top-right, row first.
    :return:
    """
    row_width_hex = len(bit_string) >> 4  # len // 16
    row_width_bin = len(bit_string) >> 2  # len // 4
    if reverse:
        for i in reversed(range(0, len(bit_string), row_width_hex)):
            yield bin(int(bit_string[i : i + row_width_hex], 16))[2:].zfill(row_width_bin)
    else:
        for i in range(0, len(bit_string), row_width_hex):
            yield bin(int(bit_string[i : i + row_width_hex], 16))[2:].zfill(row_width_bin)


def get_unihex_bearings(bit_string: str) -> tuple[int, int]:
    """
    Return the two integers of the bearings of an .hex glyph's bit string.

    Bearings are a "padding" from the edge of the canvas to image pixels.
    Left bearing is the distance from the left edge of the canvas to the most-left pixel data.
    Right bearing is the distance from the right edge of the canvas to the most-right pixel data.

    If return is (0, 0), there's no pixel data, the glyph is all spaces.

    This function is similar to :func:`mcfonts.utils.image.get_image_bearings`.

    >>> get_unihex_bearings("0000000018242442427E424242420000")
    (1, 7)

    :param bit_string: The bit string of a .hex glyph.
    :returns:
        Left bearing and right bearing.
        Returns (0, 0) if there's no pixel data.
    """
    glyph_width = get_width(bit_string)
    grid = [list(row) for row in bit_string_to_rows(bit_string)]

    left_bearing = 0
    right_bearing = glyph_width

    for x in range(glyph_width):
        if all(grid[y][x] == "0" for y in range(16)):
            left_bearing += 1
        else:
            break

    if left_bearing == glyph_width:
        # The left bearing is the whole glyph, so there's no data here anyway.
        return 0, 0

    for x_reversed in reversed(range(glyph_width)):
        if all(grid[y][x_reversed] == "0" for y in range(16)):
            right_bearing -= 1
        else:
            break

    return left_bearing, right_bearing
