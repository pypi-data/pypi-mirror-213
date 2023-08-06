#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""A ttf provider, including already-made TTF and OTF fonts."""
import collections.abc
import os

import jsonschema

import mcfonts.glyphs
import mcfonts.providers.base
import mcfonts.utils.schemas


class TTFProvider(mcfonts.providers.base.BaseProvider):
    """
    The ``ttf`` provider embeds already-compiled TrueType and OpenType fonts.

    mcfonts does not handle TTF providers by default, and they cannot be :doc:`exported <exporting>`.
    """

    minimum_pack_format = 9
    icon = "𝑇"

    def __init__(self, provider: dict, origin: os.PathLike[str] | str, resource: bytes | None = None):
        super().__init__("ttf", provider, origin)
        if "skip" in self.contents:
            chars = []
            if isinstance(skip := self.contents.get("skip"), list):
                for line in skip:
                    chars.append(line)
            # Flatten into a string
            self.contents["skip"] = "".join(chars)
        self.validate()
        self.resource = resource

    def validate(self) -> None:
        jsonschema.validate(self.contents, mcfonts.utils.schemas.SCHEMA_PROVIDER_TTF)

    def pretty_print(self) -> str:
        return f"{self.icon} ttf: {self.contents.get('file', 'no file')}"

    def print_info(self) -> None:
        super().print_info()
        # TODO finish thsi

    def construct_glyphs(
        self, ignore_empty: bool = True
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.AnyGlyph]]:
        yield from []

    def yield_glyphs(self, ignore_empty: bool = True) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.AnyGlyph]]:
        yield from []

    def yield_characters(self, ignore_padding: bool = True) -> collections.abc.Iterable[str]:
        yield from []
