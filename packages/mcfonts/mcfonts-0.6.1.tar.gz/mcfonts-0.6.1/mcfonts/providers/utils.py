#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""Utilities and types for the providers."""
from __future__ import annotations

import collections.abc
import json
import os

import PIL

import mcfonts.exceptions
import mcfonts.providers.bitmap
import mcfonts.providers.legacy_unicode
import mcfonts.providers.options
import mcfonts.providers.reference
import mcfonts.providers.space
import mcfonts.providers.ttf
import mcfonts.providers.unihex
import mcfonts.utils.resources


AnyProvider = (
    mcfonts.providers.bitmap.BitmapProvider
    | mcfonts.providers.space.SpaceProvider
    | mcfonts.providers.legacy_unicode.LegacyUnicodeProvider
    | mcfonts.providers.ttf.TTFProvider
    | mcfonts.providers.unihex.UnihexProvider
    | mcfonts.providers.reference.ReferenceProvider
)
"""
A UnionType for any kind of Provider subclass that the Vanilla game accepts.
This does not include :class:`OptionsProvider`.
"""


def format_provider_message(
    provider: AnyProvider | mcfonts.providers.options.OptionsProvider | dict, message: str
) -> str:
    """
    Format a provider warning message properly, following Provider <type>: <message>.

    Calls :func:`mcfonts.utils.pretty_print_provider()`.

    :param provider:
        The provider, either as a dictionary or instance of :data:`mcfonts.providers.AnyProvider`.
    :param message: The message to append at the end.
    :returns: The formatted warning message.
    """
    if isinstance(provider, dict):
        return f"Provider {pretty_print_provider_dictionary(provider)} {message}"
    return f"Provider {provider.pretty_print()} {message}"


def pretty_print_provider_dictionary(provider: dict) -> str:
    """
    Format a provider information message properly, following ``<type><provider specific>``.

    Provider specific info:

     * ``bitmap``: ``<file> h <height> a <ascent>``
     * ``space``: nothing
     * ``legacy_unicode``: ``<template>``
     * ``ttf``: ``<file> s <shift0, 1>, sz <size>, o <oversample>, sk <skip>``

    :param provider:
        The provider as a dictionary, **not** an instance of :data:`mcfonts.providers.AnyProvider`.
    :returns: The pretty provider information.
    """
    if (provider_type := provider.get("type", "")).lower() == "bitmap":
        return f'"bitmap": {provider.get("file", "no resource")}'
    if provider_type == "space":
        return '"space"'
    if provider_type == "legacy_unicode":
        return f'"legacy_unicode": {provider.get("template", "no template")}'
    if provider_type == "ttf":
        return (
            f'"ttf": {provider.get("file", "no file")}, s '
            f'{provider.get("shift", "[?, ?]")}, sz '
            f'{provider.get("size", "?")}, o '
            f'{provider.get("oversample", "?")}, sk '
            f'{provider.get("skip", "none")}'
        )
    if provider_type == "options":
        return '"options"'
    return f'provider "{provider_type}": ?'


def load_all(
    providers: list[dict],
    json_path: os.PathLike[str] | str,
    strict: bool = False,
    mode: str = "LA",
) -> collections.abc.Iterable[mcfonts.providers.utils.AnyProvider | mcfonts.providers.options.OptionsProvider]:
    """
    Load every provider in the list `providers`.

    :param providers:
        A list of dictionaries of providers.
        This should be the value of the "providers" key in the JSON file.
    :param json_path: The path to the JSON file at which this provider JSON is from.
    :param strict: Whether to raise or warn (and continue) on exceptions.
    :param mode:
        What "mode" to load bitmap resources in.

        * ``"LA"`` - Grayscale
        * ``"RGBA"`` - Color

    :returns: A yield of AnyProvider | OptionsProvider.
    """
    # TODO on deprecation, remove | OptionsProvider.
    for provider in providers:
        yield load_provider(provider, json_path, strict, mode)


def load_provider(
    provider: dict,
    json_path: os.PathLike[str] | str,
    strict: bool = False,
    mode: str = "LA",
) -> mcfonts.providers.utils.AnyProvider | mcfonts.providers.options.OptionsProvider:
    """
    Load a specific provider dictionary and return the equivalent Provider class.

    :param provider: A dictionary of a provider.
    :param json_path: The path to the JSON file at which this provider JSON is from.
    :param strict: Whether to raise or warn (and continue) on exceptions.
    :param mode:
        What "mode" to load bitmap resources in.

        * ``"LA"`` - Grayscale
        * ``"RGBA"`` - Color

    :returns: A Provider instance.
    """
    provider_type = provider.get("type", "").lower().strip()
    try:
        if provider_type == "bitmap":
            return mcfonts.providers.bitmap.BitmapProvider(
                provider,
                json_path,
                mcfonts.utils.resources.load_bitmap(
                    provider["file"], mcfonts.utils.resources.traverse_to_assets(json_path)
                ),
            )
        elif provider_type == "legacy_unicode":
            return mcfonts.providers.legacy_unicode.LegacyUnicodeProvider(
                provider,
                json_path,
                dict(
                    mcfonts.utils.resources.load_resources_legacy_unicode(
                        provider["template"], mcfonts.utils.resources.traverse_to_assets(json_path), provider["sizes"]
                    )
                ),
            )
        elif provider_type == "space":
            return mcfonts.providers.space.SpaceProvider(provider, json_path)
        elif provider_type == "ttf":
            with open(
                mcfonts.utils.resources.resolve_path(
                    provider["file"], mcfonts.utils.resources.traverse_to_assets(json_path), "font"
                ),
                "rb",
            ) as open_tempfile:
                ttf = open_tempfile.read()
            return mcfonts.providers.ttf.TTFProvider(provider, json_path, ttf)
        elif provider_type == "unihex":
            return mcfonts.providers.unihex.UnihexProvider(
                provider,
                json_path,
                dict(
                    mcfonts.utils.resources.load_resources_unihex(
                        provider["hex_file"], mcfonts.utils.resources.traverse_to_assets(json_path)
                    )
                ),
            )
        elif provider_type == "reference":
            # Create any child providers first
            with open(
                temp_recursive_path := mcfonts.utils.resources.resolve_path(
                    provider["id"] + ".json", mcfonts.utils.resources.traverse_to_assets(json_path), "font"
                ),
                encoding="utf-8",
            ) as temp_recursive_file:
                data = json.load(temp_recursive_file, strict=strict)
            # This is recursive
            children = list(load_all(data.get("providers", {}), temp_recursive_path, strict, mode))
            if any(isinstance(child, mcfonts.providers.reference.ReferenceProvider) for child in children):
                raise mcfonts.exceptions.ReferenceChildError()
            return mcfonts.providers.reference.ReferenceProvider(provider, json_path, children)
        elif provider_type in mcfonts.providers.options.ACCEPTED_OPTIONS_TYPES:
            return mcfonts.providers.options.OptionsProvider(provider, json_path)
    except PIL.UnidentifiedImageError as exception:
        if not strict:
            mcfonts.logger.warning(
                mcfonts.providers.utils.format_provider_message(provider, "has invalid file; must be PNG.")
            )
        else:
            raise exception
    except FileNotFoundError as exception:
        if not strict:
            # Missing files are ignored
            mcfonts.logger.warning(
                mcfonts.providers.utils.format_provider_message(
                    provider, f'file "{exception.filename}" does not exist, skipping.'
                )
            )
        else:
            # Missing files not allowed, raising exception
            raise exception
    raise mcfonts.exceptions.ProviderError(f'Unknown provider "{provider_type}".')
