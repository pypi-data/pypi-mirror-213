#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""Contains the basic parent provider that all functional providers subclass and inherit from."""
from __future__ import annotations

import abc
import collections.abc
import os

import mcfonts.constants
import mcfonts.glyphs


class BaseProvider(abc.ABC):
    """The base provider class. All providers subclass this."""

    minimum_pack_format: int = 0
    # This means nothing, but it's fun.
    icon: str = "?"

    def __init__(
        self,
        provider_type: str,
        contents: dict,
        origin: os.PathLike[str] | str,
        chars_covered: set[str] | None = None,
    ):
        """
        :param provider_type: A string of the value in the JSON "type" field.
        :param contents: The provider's contents.
        :param origin: The absolute path to the provider's JSON file.
        :param chars_covered: A set of the individual characters covered by this provider.
        """
        if chars_covered is None:
            chars_covered = set()
        self.provider_type = provider_type
        self.chars_covered: set[str] = chars_covered
        self.contents: dict = contents
        self.origin = origin

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}("{self.provider_type}", {self.contents}, {self.minimum_pack_format},'
            f" {self.chars_covered})"
        )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({len(self.chars_covered):,} chars)"

    @abc.abstractmethod
    def validate(self) -> None:
        """
        Specific tests for validating a provider.

        This function checks values to ensure that they're correct and in an acceptable range.

        If applicable, textures are checked to ensure all characters have a defined glyph,
        and that the dimensions are correct.

        Warnings are printed through :func:`mcfonts.logger.warning`.

        :returns: Nothing; problems are either raised or warned.
        """

    @abc.abstractmethod
    def print_info(self) -> None:
        """Print information about this provider."""
        print(f"Provider type: {mcfonts.constants.UNKNOWN_FIELD}")
        print(f"Characters covered: {len(self.chars_covered):,}")

    @abc.abstractmethod
    def pretty_print(self) -> str:
        """
        Return a short one line description of the provider.

        :returns: A string of the provider's info, normally ``<icon> <type>: <info,...>``.
        """
        return f"{self.icon} {self.provider_type}"

    @abc.abstractmethod
    def construct_glyphs(
        self, ignore_empty: bool = True
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.AnyGlyph]]:
        """
        Yield a tuple of (character, glyph) for every glyph available in the provider's resource.

        :param ignore_empty: Whether to ignore or include None for codepoints that don't have glyphs.
        :returns: A yield of ``(character, AnyGlyph)``.
        """

    @abc.abstractmethod
    def yield_characters(self, ignore_padding: bool = True) -> collections.abc.Iterable[str]:
        """
        Yield strings of the individual characters this provider supports.

        :returns: A yield of strings of length 1.
        """

    @abc.abstractmethod
    def yield_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.AnyGlyph]]:
        """
        Yield a tuple of (character, glyph) for every glyph available in the provider's resource.

        This is different from :meth:`construct_glyphs`
        because it yields glyphs that have already been constructed and stored.

        :returns: A yield of ``(character, AnyGlyph)``.
        """
