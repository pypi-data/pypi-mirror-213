#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""General exceptions."""
from __future__ import annotations


class ExportError(Exception):
    """Base parent class for all exceptions that may be raised when exporting a provider's characters."""


class GlyphLimitError(Exception):
    """Raised when a font has 65,535 characters allocated and that no more can be added."""


class ProviderError(Exception):
    """Raised when a :class:`mcfonts.providers.AnyProvider` is expected but not found."""


class ReferenceChildError(Exception):
    """Raised when another reference provider is given as the child provider for a reference provider."""


class ResourceError(ExportError):
    """Raised when a resource is expected but does not exist."""


class CharacterPaddingError(ExportError):
    """Raised when a requested character is in :data:`mcfonts.constants.PADDING_CHARS`."""
