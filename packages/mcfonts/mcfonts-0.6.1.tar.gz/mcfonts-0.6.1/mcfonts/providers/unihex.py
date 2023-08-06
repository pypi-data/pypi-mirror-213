#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""A unihex provider, handling .hex glyphs."""
import collections.abc
import os

import jsonschema

import mcfonts.glyphs
import mcfonts.providers.base
import mcfonts.utils.schemas
import mcfonts.utils.unihex


class UnihexProvider(mcfonts.providers.base.BaseProvider):
    """
    The ``unihex`` provider loads glyphs from text files in the ".hex" format.

    It has two required fields, ``hex_file`` and ``size_overrides``.

    * ``hex_file`` is a resource location to a .ZIP file containing any number of ".hex" files at its root.
    * ``size_overrides`` is a list of maps stating the beginning and end of a character range, and the starting and
      ending columns of the glyphs that match that range.

    Each ".hex" file is a text document with each line containing a hex glyph.
    A hex glyph is a string of text in the format of ``<codepoint>:<bit string>``.
    The bit string is a string of hexadecimal numbers.
    The numbers, when converted to binary, describe the glyph's pixels.
    A 1 bit is an "on" pixel, and a 0 bit is an "off" pixel.
    When exporting, the empty left and right columns are trimmed unless ``size_overrides`` explicitly overrides this.
    """

    minimum_pack_format = 15
    icon = "⬣"

    def __init__(self, provider: dict, origin: os.PathLike[str] | str, resources: dict[str, str] | None):
        self.contents = provider
        self.resources = resources
        self.size_overrides: dict[str, tuple[int, int]] = dict(self.yield_size_overrides())
        self.glyphs: dict[str, mcfonts.glyphs.UnihexGlyph] | None = dict(self.construct_glyphs())
        super().__init__("unihex", provider, origin, set(self.glyphs.keys()))
        self.validate()

    def construct_glyphs(
        self, ignore_empty: bool = True
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.UnihexGlyph]] | None:
        if not self.resources:
            return
        for name, hex_contents in self.resources.items():
            for hex_glyph in hex_contents.splitlines():
                yield mcfonts.utils.unihex.get_codepoint(hex_glyph), mcfonts.glyphs.UnihexGlyph(
                    mcfonts.utils.unihex.get_bit_string(hex_glyph), None, None, None, None
                )

    def yield_size_overrides(self) -> collections.abc.Iterable[tuple[str, tuple[int, int]]]:
        """
        Yield all the size overrides for every character.

        Overrides are given as ``tuple[int, int]``.

        :returns: A yield of (character, (left, right))
        """
        override: dict
        for override in self.contents.get("size_overrides", {}):
            left: int = override.get("left", -1)
            right: int = override.get("right", -1)
            for codepoint in range(ord(override.get("from", 0)), ord(override.get("to", 0))):
                yield chr(codepoint), (left, right)

    def get_size_override(self, character: str) -> tuple[int, int] | None:
        """
        The size overrides are a tuple of two integers of the starting and ending columns to cut off when exporting.
        """
        return self.size_overrides.get(character)

    def validate(self) -> None:
        jsonschema.validate(self.contents, mcfonts.utils.schemas.SCHEMA_PROVIDER_UNIHEX)

    def pretty_print(self) -> str:
        return (
            f"{self.icon} unihex: {len(self.resources or []):,} .hex files, {len(self.size_overrides):,} size overrides"
        )

    def print_info(self) -> None:
        pass

    def yield_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.UnihexGlyph]]:
        yield from self.glyphs.items()

    def yield_characters(self, ignore_padding: bool = True) -> collections.abc.Iterable[str]:
        for key in self.glyphs:
            yield key
