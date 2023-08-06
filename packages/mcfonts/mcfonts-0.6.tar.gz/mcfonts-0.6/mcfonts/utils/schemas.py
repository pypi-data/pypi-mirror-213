#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""JSON schemas for providers."""
from __future__ import annotations

import re

import unirange

PATTERN_RESOURCE_LOCATION = re.compile(r"^([0-9a-z_.]+:)?[0-9a-z_./-]+")
PATTERN_RESOURCE_LOCATION_TEMPLATED = re.compile(r"^([0-9a-z_.]+:)?[0-9a-z_./%-]+")

SCHEMA_PROVIDER_BITMAP = {
    "type": "object",
    "properties": {
        "type": {"const": "bitmap"},
        "file": {"type": "string", "minLength": 1, "pattern": PATTERN_RESOURCE_LOCATION.pattern + r"\.png$"},
        "height": {"type": "integer", "minimum": 1, "maximum": 512, "default": 8},
        "ascent": {"type": "integer", "minimum": -512, "maximum": 512},
        "chars": {"type": "array", "minItems": 1, "items": {"type": "string"}},
        "__comment": {"type": "string"},
    },
    "required": ["type", "file", "ascent", "chars"],
    "additionalProperties": True,
}
"""A schema to validate "bitmap" providers against."""

SCHEMA_PROVIDER_SPACE = {
    "type": "object",
    "properties": {
        "type": {"const": "space"},
        "advances": {
            "type": "object",
            "minLength": 1,
            "patternProperties": {unirange.UNIRANGE_FULL.pattern: {"type": "integer", "minimum": -256, "maximum": 256}},
        },
        "comment": {"type": "string"},
    },
    "required": ["type", "advances"],
    "additionalProperties": True,
}

"""A schema to validate "space" providers against."""

SCHEMA_PROVIDER_LEGACY_UNICODE = {
    "type": "object",
    "properties": {
        "type": {"const": "legacy_unicode"},
        "sizes": {"type": "string", "minLength": 1, "pattern": PATTERN_RESOURCE_LOCATION.pattern + r"\.bin$"},
        "template": {
            "type": "string",
            "minLength": 1,
            "pattern": PATTERN_RESOURCE_LOCATION_TEMPLATED.pattern + r"\.png$",
        },
        "comment": {"type": "string"},
    },
    "required": ["type", "sizes", "template"],
    "additionalProperties": True,
}
"""A schema to validate "legacy_unicode" providers against."""

SCHEMA_PROVIDER_TTF = {
    "type": "object",
    "properties": {
        "type": {"const": "ttf"},
        "file": {"type": "string", "minLength": 1, "pattern": PATTERN_RESOURCE_LOCATION.pattern + r"\.[ot]tf$"},
        "shift": {"type": "array", "items": {"type": "number"}, "minItems": 2, "maxItems": 2},
        "size": {"type": "number", "minimum": 1},
        "oversample": {"type": "number", "minimum": 1},
        "skip": {"type": ["string", "array"]},
        "comment": {"type": "string"},
    },
    "required": ["type", "file", "shift", "size", "oversample"],
    "additionalProperties": True,
}
"""A schema to validate "ttf" providers against."""

SCHEMA_PROVIDER_OPTIONS = {
    "type": "object",
    "properties": {
        "type": {"enum": ["options", "mcfonts:options"]},
        "fields": {
            "type": "object",
            "properties": {
                "fullwidth": {
                    "type": "object",
                    "patternProperties": {unirange.UNIRANGE_FULL.pattern: {"type": "boolean"}},
                },
                "shift": {
                    "type": "object",
                    "patternProperties": {
                        unirange.UNIRANGE_FULL.pattern: {
                            "type": "array",
                            "minItems": 2,
                            "maxItems": 2,
                            "items": {"type": "integer"},
                        }
                    },
                },
                "spacing": {
                    "type": "object",
                    "patternProperties": {unirange.UNIRANGE_FULL.pattern: {"type": "integer", "minimum": 0}},
                },
                "width": {
                    "type": "object",
                    "patternProperties": {unirange.UNIRANGE_FULL.pattern: {"type": "integer"}},
                },
            },
        },
        "comment": {"type": "string"},
    },
    "required": ["type"],
    "additionalProperties": True,
}
"""A schema to validate "options" providers against."""

SCHEMA_PROVIDER_UNIHEX = {
    "type": "object",
    "properties": {
        "type": {"const": "unihex"},
        "hex_file": {"type": "string", "minLength": 1, "pattern": PATTERN_RESOURCE_LOCATION.pattern + r"\.zip$"},
        "size_overrides": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "__ranges": {
                        # "__ranges" isn't part of the specification, but it's included in Vanilla files anyway.
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                    },
                    "from": {"type": "string", "minLength": 1, "maxLength": 1},
                    "to": {"type": "string", "minLength": 1, "maxLength": 1},
                    "left": {"type": "integer", "minimum": 0, "maximum": 256},
                    "right": {"type": "integer", "minimum": 0, "maximum": 256},
                },
                "required": ["from", "to", "left", "right"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["type", "hex_file", "size_overrides"],
    "additionalProperties": True,
}

SCHEMA_PROVIDER_REFERENCE = {
    "type": "object",
    "properties": {
        "type": {"const": "reference"},
        "id": {"type": "string", "minLength": 1, "pattern": PATTERN_RESOURCE_LOCATION.pattern},
    },
    "required": ["type", "id"],
    "additionalProperties": True,
}
