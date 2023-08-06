#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""A legacy unicode provider, handling bitmap glyphs in a 16px x 16px grid."""
import collections.abc
import os
import re
import unicodedata

import PIL.Image
import jsonschema

import mcfonts.constants
import mcfonts.glyphs
import mcfonts.providers.base
import mcfonts.utils.resources
import mcfonts.utils.schemas


class LegacyUnicodeProvider(mcfonts.providers.base.BaseProvider):
    """
    The ``legacy_unicode`` provider is a "fallback" provider intended to be used as a last-resort.

    It is similar to the :class:`bitmap provider<mcfonts.providers.bitmap.BitmapProvider>`
    in that its glyphs are bitmaps.

    It uses a system of templates to create and add 16px x 16px tables of "fallback" characters.
    Each glyph is 16px x 16px pixels wide, so each page is 256px x 256px;
    16 characters on each line, 16 lines, 16 length for each glyph.

    .. warning::
        This provider is deprecated and should not be used when possible.
        Use the "unihex" provider instead.

    .. important::
        Characters above the `BMP <https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane>`_ (U+FFFF)
        are not handled.
    """

    minimum_pack_format = 4
    icon = "🖳"

    def __init__(self, provider: dict, origin: os.PathLike[str] | str, resources: dict[str, PIL.Image.Image | bytes]):
        self.resources = resources
        self.codepages_covered: list[int] = []
        self.glyphs: dict[str, mcfonts.glyphs.BitmapGlyph] = dict(self.construct_glyphs())
        super().__init__(
            "legacy_unicode",
            provider,
            origin,
            set(self.yield_characters()),
        )
        self.validate()

    def pretty_print(self) -> str:
        return f"{self.icon} legacy_unicode: {self.contents.get('template', 'no template')}"

    def validate(self) -> None:
        jsonschema.validate(self.contents, mcfonts.utils.schemas.SCHEMA_PROVIDER_LEGACY_UNICODE)

    def print_info(self) -> None:
        # TODO add the format here
        """Print information about this provider."""
        print(f"Template: {self.contents['template'] or mcfonts.constants.UNKNOWN_FIELD}")
        print(f"Sizes: {self.contents['sizes'] or mcfonts.constants.UNKNOWN_FIELD}")

    def construct_glyphs(
        self, ignore_empty: bool = True
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.AnyGlyph]]:
        yield from []

    def yield_glyphs(
        self, ignore_empty: bool = True
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.BitmapGlyph]]:
        for codepage, content in self.resources.items():
            # If template_\d\d\.png doesn't match codepage name, skip.
            if not re.match(
                self.contents["template"].replace("\\", "\\\\").replace("%s", r"(\d\d)"), codepage
            ) or not isinstance(content, PIL.Image.Image):
                continue
            codepage_num = re.match(codepage, r"\d\d")
            for index, glyph in enumerate(mcfonts.utils.resources.divide_resource_by_grid(content, (16, 16))):
                if glyph is None:
                    continue
                yield chr((int(codepage_num.group(1), 16) << 8) + index), mcfonts.glyphs.BitmapGlyph(glyph, 1)

    def yield_characters(self, ignore_padding: bool = True) -> collections.abc.Iterable[str]:
        for key in self.glyphs.keys():
            yield str(key)


def to_advances(glyphsizes: bytes, match_unicode_category: list[str] | None = None) -> dict[str, int]:
    """
    Translate a glyphsizes.bin file into an "advances" mapping, which goes inside a "space" provider.

    .. info::

        This function does not return a new provider.

    >>> to_advances(b"\\x00\\x00\\x00...")
    {
        "a": 0,
        "b": 0,
        "c": 0,
        "\uBEEF": 15
    }

    :param glyphsizes: The bytes of glyphsizes.bin.
    :param match_unicode_category:
        Only translate Unicode characters with these categories.
        By default, this is ``[Mc, Zp, Zs, Zl]``.
        This should cover most whitespace and marking characters.
    :returns: An "advances" dictionary.
    """
    if match_unicode_category is None:
        match_unicode_category = ["Mc", "Zp", "Zs", "Zl"]
    advances = {}
    for index, nibble in enumerate(glyphsizes):
        if unicodedata.category(char := chr(index)) in match_unicode_category:
            advances[char] = (nibble & 0xF) - (nibble >> 4 & 0xF)
    return advances


def build_template_for_char(char: str, path_to_template_textures: str | None = None) -> PIL.Image.Image:
    """
    Build an image of a template :term:`codepoint`.

    Templates are simple white boxes with a codepoint :term:`texture` inside them.
    This is intended for use with a "legacy_unicode" :term:`provider`.

    :param char:
        A single character.
        This character's codepoint is what goes inside the box.
    :param path_to_template_textures:
        The path to the folder that contains the digit textures.
        See the documentation for :func:`mcfonts.templates.generate_unicode_template_font`.
    :returns: A :class:`PIL.Image.Image` of the char template
    """
    codepoint = ord(char)
    templates = generate_unicode_template_font(path_to_template_textures)
    if codepoint > 0xFFFF:
        box = templates[-6]
        # 0xABCDEF -> A
        box.paste(templates[(codepoint & 0xF00000) >> 20], (2, 2))
        # 0xABCDEF -> B
        box.paste(templates[(codepoint & 0xF0000) >> 16], (6, 2))
        # 0xABCDEF -> C
        box.paste(templates[(codepoint & 0xF000) >> 12], (10, 2))
        # 0xABCDEF -> D
        box.paste(templates[(codepoint & 0xF00) >> 8], (2, 9))
        # 0xABCDEF -> E
        box.paste(templates[(codepoint & 0xF0) >> 4], (6, 9))
        # 0xABCDEF -> F
        box.paste(templates[(codepoint & 0xF)], (10, 9))
    else:
        box = templates[-4]
        # 0xABCD -> A
        box.paste(templates[(codepoint & 0xF000) >> 12], (2, 2))
        # 0xABCD -> B
        box.paste(templates[(codepoint & 0xF00) >> 8], (6, 2))
        # 0xABCD -> C
        box.paste(templates[(codepoint & 0xF0) >> 4], (2, 9))
        # 0xABCD -> D
        box.paste(templates[codepoint & 0xF], (6, 9))
    return box


def generate_unicode_template_font(path: str | None = None) -> dict[int, PIL.Image.Image]:
    """
    Generate a dictionary of hex -> sheet.

    Path must point to a folder where these files exist (PNG format):

    * ``<0-9>.png``
    * ``<a-f>.png``
    * ``box4.png``
    * ``box6.png``

    The file names **are** case-sensitive, and the textures for hex charlist **must** be 3 pixels wide by 6 pixels tall.

    * The sheet for "box6.png" must be 16px x 16px.
    * The sheet for "box4.png" must be 12px x 16px.
    * Hex characters are overlayed atop the box.
    * Box4 is for chars below U+10000 (4 points, F4E -> 0F4E; 4).
    * Box6 is for chars above U+FFFF (6 points, 1FAE6 -> 01FAE6; 6).

    Color does not matter.

    This is used for generating Unicode template characters,
    see :func:`mcfonts.utils.legacy_unicode.build_template_for_char`.

    :param path:
        Path to the folder where these textures exist.
        If this is falsy (None, ""), the path will be set automatically from the module and will
        use pre-made character textures that were distributed with this module.
    :returns:
        A dictionary that maps 0-15 to a glyph.
        -4 and -6 are box4 and box6, respectively.
    """
    if path:
        templates = mcfonts.utils.resources.expand_path(path)
    else:
        templates = mcfonts.utils.resources.expand_path(os.path.join(__file__, "../../template_hexchar_textures"))
    return {
        0: PIL.Image.open(f"{templates}/0.png"),
        1: PIL.Image.open(f"{templates}/1.png"),
        2: PIL.Image.open(f"{templates}/2.png"),
        3: PIL.Image.open(f"{templates}/3.png"),
        4: PIL.Image.open(f"{templates}/4.png"),
        5: PIL.Image.open(f"{templates}/5.png"),
        6: PIL.Image.open(f"{templates}/6.png"),
        7: PIL.Image.open(f"{templates}/7.png"),
        8: PIL.Image.open(f"{templates}/8.png"),
        9: PIL.Image.open(f"{templates}/9.png"),
        10: PIL.Image.open(f"{templates}/a.png"),
        11: PIL.Image.open(f"{templates}/b.png"),
        12: PIL.Image.open(f"{templates}/c.png"),
        13: PIL.Image.open(f"{templates}/d.png"),
        14: PIL.Image.open(f"{templates}/e.png"),
        15: PIL.Image.open(f"{templates}/f.png"),
        -4: PIL.Image.open(f"{templates}/box4.png"),
        -6: PIL.Image.open(f"{templates}/box6.png"),
    }


def align_unicode_page(sheet: PIL.Image.Image) -> PIL.Image.Image:
    """
    Align a Unicode page font sheet's characters to the left.

    This function is a shortcut for :func:`mcfonts.utils.resources.align_font_texture(sheet, (16, 16))`.

    :param sheet: The font sheet, not the individual character.
    :returns: The new font sheet.
    """
    return mcfonts.utils.resources.align_font_texture(sheet, (16, 16))
