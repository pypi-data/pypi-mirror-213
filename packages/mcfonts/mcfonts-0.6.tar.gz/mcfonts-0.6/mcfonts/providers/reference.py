#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""A reference provider, including other fonts."""
import collections.abc
import os
import typing

import jsonschema

import mcfonts.exceptions
import mcfonts.glyphs
import mcfonts.providers.base
import mcfonts.providers.bitmap
import mcfonts.providers.legacy_unicode
import mcfonts.providers.space
import mcfonts.providers.ttf
import mcfonts.providers.unihex
import mcfonts.providers.utils
import mcfonts.utils.schemas

AnyProviderNotReference = (
    mcfonts.providers.bitmap.BitmapProvider
    | mcfonts.providers.space.SpaceProvider
    | mcfonts.providers.legacy_unicode.LegacyUnicodeProvider
    | mcfonts.providers.ttf.TTFProvider
    | mcfonts.providers.unihex.UnihexProvider
)
"""
A UnionType similar to :class:`mcfonts.providers.utils.AnyProvider`,
except that it does not include :class:`ReferenceProvider`."""

PROVIDER_SHORTCUT_MAP: dict[typing.Type[AnyProviderNotReference], str] = {
    mcfonts.providers.bitmap.BitmapProvider: "bt",
    mcfonts.providers.space.SpaceProvider: "sp",
    mcfonts.providers.legacy_unicode.LegacyUnicodeProvider: "lu",
    mcfonts.providers.ttf.TTFProvider: "ttf",
    mcfonts.providers.unihex.UnihexProvider: "uh",
}


class ReferenceProvider(mcfonts.providers.base.BaseProvider):
    """
    The ``reference`` provider is used to include and load another font only once.

    It has one field, ``id``, which points to a font JSON to include.
    If more than 1 reference provider points to the same font JSON, it will be ignored.
    """

    minimum_pack_format = 15
    icon = "↩"

    def __init__(self, provider: dict, origin: os.PathLike[str] | str, children: list[AnyProviderNotReference]):
        if isinstance(children, self.__class__):
            raise mcfonts.exceptions.ReferenceChildError("a child provider cannot be another reference provider")
        self.children: list[AnyProviderNotReference] = children

        super().__init__("reference", provider, origin, set(self.yield_characters()))
        self.validate()

    def validate(self) -> None:
        jsonschema.validate(self.contents, mcfonts.utils.schemas.SCHEMA_PROVIDER_REFERENCE)

    def print_info(self) -> None:
        super().print_info()
        n_children: int = len(self.children)
        print(f"Children: ({n_children})")
        provider: mcfonts.providers.utils.AnyProvider
        for provider in self.children:
            print(f"\t- {str(provider.__class__)}, {len(provider.chars_covered):,} chars")

    def construct_glyphs(
        self, ignore_empty: bool = True
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.AnyGlyph]]:
        # TODO add this stuff I guess
        yield from []

    def yield_children(self) -> collections.abc.Iterable[AnyProviderNotReference]:
        """
        Yield all the providers that this reference provider is referring to.

        :returns: A yield of the contained providers.
        """
        yield from self.children

    def pretty_print(self) -> str:
        children_formatted: list[str] = [
            PROVIDER_SHORTCUT_MAP.get(child.__class__, mcfonts.constants.UNKNOWN_FIELD) for child in self.children
        ]
        return f"{self.icon} reference: {len(self.children):,} children: [{', '.join(children_formatted)}]"

    def yield_glyphs(self) -> collections.abc.Iterable[mcfonts.glyphs.BitmapGlyph | None]:
        raise NotImplementedError()

    def yield_characters(self, ignore_padding: bool = True) -> collections.abc.Iterable[str]:
        for child in self.children:
            for char in child.yield_characters(ignore_padding):
                yield char
