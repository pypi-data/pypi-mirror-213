#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
The Options provider.

.. warning::
    This is deprecated and will be removed in v0.7.
"""
import os
import warnings

import jsonschema
import unirange

import mcfonts.utils.schemas

ACCEPTED_OPTIONS_TYPES: set[str] = {"mcfonts:options", "options"}

warnings.warn("The options provider is deprecated.", DeprecationWarning, stacklevel=2)


class OptionsProvider:
    """
    A mcfonts-specific provider that only is used when exporting.

    This does not extend :class:`mcfonts.providers.base.BaseProvider`.

    .. warning::
        This is deprecated and will be removed in v0.7.
    """

    # TODO Deprecated, removing in v0.7.

    icon = "⚙"

    def __init__(self, provider: dict, origin: os.PathLike[str] | str):
        warnings.warn("The options provider is deprecated.", DeprecationWarning, stacklevel=2)
        self.contents = provider
        self.origin = origin
        self.contents["fields"] = {}

        # Expand the uniranges, copy over fields
        for field in OPTION_FIELDS:
            if field not in self.contents["fields"]:
                self.contents["fields"][field] = {}
            for key, value in provider.get("fields", {}).get(field, {}).items():
                for newchar in unirange.unirange_to_characters(key):
                    self.contents["fields"][field][newchar] = value
        self.chars_covered: set[str] = set()
        for field in OPTION_FIELDS:
            self.chars_covered.update(self.contents["fields"].get(field, {}).keys())
        self.validate()

    def validate(self) -> None:
        """
        Validate this provider, ensuring its structure is correct and that all values are acceptable.

        This function **does** validate textures.
        """
        jsonschema.validate(self.contents, mcfonts.utils.schemas.SCHEMA_PROVIDER_OPTIONS)
        for char in self.chars_covered:
            if self.contents.get("fullwidth", {}).get(char) and self.contents.get("spacing", {}).get(char):
                mcfonts.logger.warning(
                    f"Provider has conflicting options, fullwidth and spacing are present for character {char}."
                )
            if self.contents.get("fullwidth", {}).get(char) and self.contents.get("width", {}).get(char):
                mcfonts.logger.warning(
                    f"Provider has conflicting options, fullwidth and width are present for character {char}."
                )
            if self.contents.get("width", {}).get(char) and self.contents.get("spacing", {}).get(char):
                mcfonts.logger.warning(
                    f"Provider has conflicting options, width and spacing are present for character {char}."
                )

    def get_options_for_char(self, char: str) -> dict[str, int | bool | list[int]] | None:
        """
        Given `char`, a character, return a dictionary of all the options for that character.

        For example, if :attr:`self.contents` is:
            {"width": {"a": 4}, "spacing": {"a": 0}}
        Then `self.get_options_for_char("a")` should return:
            {"width": 4, "spacing": 0}

        :param char: A single character.
        :returns: A flat dictionary containing a value for each field that `char` has declared.
        """
        if char in mcfonts.constants.PADDING_CHARS:
            return None
        result = {}
        for field in OPTION_FIELDS:
            if (char_options := self.contents["fields"].get(field, {}).get(char)) is not None:
                result[field] = char_options
        if result:
            return result
        return None

    def has_options(self, char: str, field_names: str | set[str] | None = None) -> bool:
        """
        Given `char`, a character, return if any options are defined for it.

        If `field_names` is not None, only return True if the character has an option for that field.

        :param char:
            A single character.
        :param field_names:
            Either a string, list of strings, or None.
            * If str, check for this field name only.
            * If list[str], check for *any* of these field names.
            * If None, no special field check.
        :returns: If `char` has an option declared for it.
        """
        if isinstance(field_names, str):
            fields = {field_names}
        elif isinstance(field_names, set):
            fields = field_names
        else:
            fields = OPTION_FIELDS
        for field in fields:
            if (self.contents["fields"].get(field, {}).get(char)) is not None:
                return True
        return False

    def pretty_print(self) -> str:
        """Pretty print this provider."""
        return f"{self.icon} options: {len(self.chars_covered):,} chars"


OPTION_FIELDS: set[str] = {
    "width",
    "fullwidth",
    "shift",
    "spacing",
}
