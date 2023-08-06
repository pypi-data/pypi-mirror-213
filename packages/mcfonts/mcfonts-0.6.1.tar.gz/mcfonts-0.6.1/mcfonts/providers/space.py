#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""A space provider, defining simple widths for characters."""
import collections.abc
import os

import jsonschema
import unirange

import mcfonts.constants
import mcfonts.glyphs
import mcfonts.providers.base
import mcfonts.utils.schemas
import mcfonts.utils.unicode


class SpaceProvider(mcfonts.providers.base.BaseProvider):
    """
    The ``space`` provider defines only the width of a character.

    It's the simplest provider: it only contains the ``"advances"`` map.

    The keys of the advances are the characters as 1-length strings, and the values are the widths as integers.

    In mcfonts only, uniranges can also be used as the keys.
    They will be expanded as they're for the :doc:`options`.

    The default width for U+0020 SPACE is 4.
    """

    minimum_pack_format = 9
    icon = "␣"

    def __init__(self, provider: dict, origin: os.PathLike[str] | str):
        # Expand the uniranges, copy over fields
        self.contents = provider
        self.glyphs: dict[str, mcfonts.glyphs.SpaceGlyph] = dict(self.construct_glyphs())
        for key, value in provider.get("advances", {}).items():
            for newchar in unirange.unirange_to_characters(key):
                self.contents["advances"][newchar] = value
        super().__init__("space", provider, origin, set(provider["advances"].keys()))
        self.validate()

    def pretty_print(self) -> str:
        return f"{self.icon} space: {len(self.contents.get('advances', [])):,} widths"

    def validate(self) -> None:
        jsonschema.validate(self.contents, mcfonts.utils.schemas.SCHEMA_PROVIDER_SPACE)

    def print_info(self) -> None:
        super().print_info()

        if len(self.contents["advances"]) < 1:
            # There's no "advances" dictionary.
            print("No advances.")
        else:
            advances = self.contents["advances"]
            print(f"Advances: ({len(advances):,})")
            for spacechar, width in advances.items():
                print(f"\tCharacter {mcfonts.utils.unicode.pretty_print_char(spacechar)}: {width}")

    def construct_glyphs(
        self, ignore_empty: bool = True
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.AnyGlyph]]:
        for character, width in self.contents["advances"].items():
            yield character, mcfonts.glyphs.SpaceGlyph(width)

    def yield_characters(self, ignore_padding: bool = False) -> collections.abc.Iterable[str]:
        for char in self.contents["advances"]:
            if not ignore_padding or char not in mcfonts.constants.PADDING_CHARS:
                yield char

    def yield_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.SpaceGlyph]]:
        yield from self.glyphs.items()


def to_glyph_sizes(advances: dict[str, int], default_width: tuple[int, int] = (0, 14)) -> bytearray:
    """
    Create a glyph_sizes.bin bytearray from a template of characters and their starting and ending positions.

    >>> to_glyph_sizes({"\\0": 15}, (0, 0))
    bytearray(b'\\x0e\\x00\\x00\\x00...')

    :param advances: A dictionary of ``{character: width}``.
    :param default_width:
        The width to fall back to if `advances` doesn't define one for a character.
    :returns: Bytearray of glyph_sizes.bin.
    """
    glyphsizes = bytearray((default_width[0] * 16 + default_width[1]).to_bytes(1, "big") * 65536)
    for character, width in advances.items():
        if (codepoint := ord(character)) > 0xFFFF:
            # Can't pack characters higher than the BMP.
            mcfonts.logger.warning(f"Cannot include character {character} in glyph_sizes; codepoint is above U+FFFF.")
            continue
        # Ensure the high and low bits are in the correct 0-F range.
        if 0 > width < 15:
            raise ValueError("Width must be within 0 to 15")
        glyphsizes[codepoint] = width
    return glyphsizes
