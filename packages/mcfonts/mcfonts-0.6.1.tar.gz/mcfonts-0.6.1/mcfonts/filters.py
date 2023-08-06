#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""A filter is a class used to control what characters and providers are included or not included when exporting."""
from __future__ import annotations

import enum

import unirange

import mcfonts.providers.options
import mcfonts.providers.utils


@enum.unique
class OptionPolicy(enum.Enum):
    # TODO Deprecated, remove soon
    """How to handle special options attached to characters."""

    INCLUDE = 0
    """Include characters that have options declared."""
    DISREGARD_OPTIONS = 1
    """Disregard the options for a char, even if declared (but still include the char)."""
    INCLUDE_ONLY = 2
    """Only include characters that have any options declared."""
    EXCLUDE = 3
    """Do not include characters that have any options declared.."""


@enum.unique
class CharPolicy(enum.Enum):
    """How to handle filtered characters."""

    INCLUDE = 0
    """Include only the characters in this filter."""
    EXCLUDE = 1
    """Do not include any of the characters in this filter."""


@enum.unique
class ProviderPolicy(enum.Enum):
    """How to handle filtered providers."""

    INCLUDE = 0
    """Include only these providers."""
    EXCLUDE = 1
    """Do not include these providers."""


class FilterResult(enum.Enum):
    """The result of a filter query."""

    CONTINUE = 0
    """No special treatment needed; this character is not filtered."""
    SKIP_CHAR = 1
    """Skip this character."""
    SKIP_PROVIDER = 2
    """Skip this provider."""
    DISCARD_CHAR_OPTIONS = 3
    """Character is allowed, but special options must not be considered."""


class Filter:
    """
    A filter used in exporting.

    Can filter characters based on their codepoint, and if they have options.
    Can filter providers based on their type.
    """

    def __init__(
        self,
        filtered_chars: set[str] | str | None = None,
        filtered_providers: set[type[mcfonts.providers.utils.AnyProvider]] | None = None,
        char_policy: CharPolicy = CharPolicy.EXCLUDE,
        provider_policy: ProviderPolicy = ProviderPolicy.EXCLUDE,
        option_policy: OptionPolicy = OptionPolicy.INCLUDE,
    ) -> None:
        if filtered_chars is None:
            filtered_chars = set()
        elif isinstance(filtered_chars, str):
            filtered_chars = unirange.unirange_to_characters(filtered_chars)
        if filtered_providers is None:
            filtered_providers = set()
        self.filtered_chars: set[str] = filtered_chars
        self.char_policy: CharPolicy = char_policy
        self.filtered_providers: set[type[mcfonts.providers.utils.AnyProvider]] = filtered_providers
        self.provider_policy: ProviderPolicy = provider_policy
        self.option_policy: OptionPolicy = option_policy  # TODO Deprecated, remove soon

    def filter_char(self, character: str) -> bool:
        """
        Add `character` to the character filter.

        :param character: A string of 1 character.
        :returns: Boolean of success; True if character was added, False if it was already present.
        """
        if character in self.filtered_chars:
            return False
        self.filtered_chars.add(character)
        return True

    def unfilter_char(self, character: str) -> bool:
        """
        Remove `character` from the character filter.

        :param character: A string of 1 character.
        :returns: Boolean of success; True if character was removed, False if it wasn't present.
        """
        if character not in self.filtered_chars:
            return False
        self.filtered_chars.remove(character)
        return True

    def filter_provider(self, provider: type[mcfonts.providers.utils.AnyProvider]) -> bool:
        """
        Add `provider` to the provider filter.

        :param provider: A type of :data:`~mcfonts.providers.utils.AnyProvider`.
        :returns: Boolean of success; True if the provider was added, False if it was already present.
        """
        if provider in self.filtered_providers:
            return False
        self.filtered_providers.add(provider)
        return True

    def unfilter_provider(self, provider: type[mcfonts.providers.utils.AnyProvider]) -> bool:
        """
        Remove `provider` from the provider filter.

        :param provider: A type of :data:`~mcfonts.providers.utils.AnyProvider`.
        :returns: Boolean of success; True if provider was removed, False if it was never present.
        """
        if provider not in self.filtered_providers:
            return False
        self.filtered_providers.remove(provider)
        return True

    def set_char_policy(self, new_char_policy: CharPolicy) -> None:
        """
        Set the character policy for how to handle filtering characters.

        :param new_char_policy: A value from the :class:`CharPolicy` enum.
        """
        self.char_policy = new_char_policy

    def set_provider_policy(self, new_provider_policy: ProviderPolicy) -> None:
        """
        Set the provider policy for how to handle filtering providers.

        :param new_provider_policy: A value from the :class:`ProviderPolicy` enum.
        """
        self.provider_policy = new_provider_policy

    def set_option_policy(self, new_option_policy: OptionPolicy) -> None:
        """
        Set the option policy for how to handle filtering characters with options.

        :param new_option_policy: A value from the :class:`OptionPolicy` enum.
        """
        self.option_policy = new_option_policy  # TODO Deprecated, remove soon

    def should_ignore_char(
        self, character: str, options: mcfonts.providers.options.OptionsProvider | None = None
    ) -> FilterResult:
        """
        Determine how `character` should be handled, working off of the current Filter instance.

        - If filtered characters are declared:
            - If character is **IN** filtered characters **AND** character policy is EXCLUDE
            - OR
            - If character is **NOT IN** filtered characters **AND** character policy is INCLUDE:
                - *Skip character*
        - If options exist:
            - If options **DO EXIST** for character:
                - If option policy is INCLUDE or INCLUDE_ONLY:
                    - *Continue*
                - If option policy is DISREGARD_OPTIONS:
                    - *Ignore character options, continue*
                - If option policy is EXCLUDE:
                    - *Skip character*
            - If options **DO EXIST** for character **AND** option policy is INCLUDE_ONLY:
                - *Skip character*
        - Else:
            - *Continue*

        :param character: A string of a character to determine filtering for.
        :param options:
            An optional instance of :class:`~mcfonts.providers.options.OptionsProvider`.
            If this is None, :data:`self.char_policy` will be ignored.
        :returns: A value from the :class:`FilterResult` enum.
        """

        if self.filtered_chars and (
            (self.char_policy == CharPolicy.EXCLUDE and character in self.filtered_chars)
            or (self.char_policy == CharPolicy.INCLUDE and character not in self.filtered_chars)
        ):
            return FilterResult.SKIP_CHAR

        if options is not None:
            if options.has_options(character):
                if self.option_policy in {
                    OptionPolicy.INCLUDE,
                    OptionPolicy.INCLUDE_ONLY,
                }:
                    return FilterResult.CONTINUE
                if self.option_policy == OptionPolicy.DISREGARD_OPTIONS:
                    return FilterResult.DISCARD_CHAR_OPTIONS
                if self.option_policy == OptionPolicy.EXCLUDE:
                    return FilterResult.SKIP_CHAR
            if self.option_policy == OptionPolicy.INCLUDE_ONLY:
                return FilterResult.SKIP_CHAR
        return FilterResult.CONTINUE

    def should_ignore_provider(self, provider: type[mcfonts.providers.utils.AnyProvider]) -> FilterResult:
        """
        Determine how `provider` should be handled, working off of the current Filter instance.

        - If filtered providers are declared:
            - If provider is **IN** filtered providers **AND** provider policy is EXCLUDE:
            - OR
            - If provider is **NOT IN** filtered providers **AND** provider policy is INCLUDE:
                - *Skip provider*
        - Else:
            - *Continue*

        :param provider: The type of the provider to determine filtering for; this is not an instance.
        :returns: A value from the :class:`FilterResult` enum.
        """
        if self.filtered_providers and (
            (provider in self.filtered_providers and self.provider_policy == ProviderPolicy.EXCLUDE)
            or (provider not in self.filtered_providers and self.provider_policy == ProviderPolicy.INCLUDE)
        ):
            return FilterResult.SKIP_PROVIDER
        return FilterResult.CONTINUE
