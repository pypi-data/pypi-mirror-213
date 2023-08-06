#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
TODO doc
- this
- add basic doc for all getters
"""
from __future__ import annotations

import abc
import dataclasses
import math

import PIL.Image
import fontTools.pens.t2CharStringPen
import lxml.etree

import mcfonts.constants
import mcfonts.exceptions
import mcfonts.utils.exporting
import mcfonts.utils.image
import mcfonts.utils.unihex

BITMAP_EXPORT_PIXEL_THRESHOLD = 180
UNIHEX_EXPORT_PIXEL_ON = "1"
SPACE_EXPORT_MAX_ADVANCE = 12500


class Glyph(abc.ABC):
    """The base Glyph class. Should never be called or instantiated."""

    @abc.abstractmethod
    def get_width(self) -> int:
        """Width of the glyph."""

    @abc.abstractmethod
    def export_to_character(
        self,
        font_xml: lxml.etree._Element,
        character: str,
        allocated_characters: set[str],
        char_options: dict | None = None,
    ) -> None:
        """
        Export this glyph to a character in a font XML.

        The font XML is mutated in-place and nothing is returned.

        :param font_xml: The font XML as a :class:`lxml.etree._Element`.
        :param character: A string of a single character for what Unicode character to export and assign the glyph to.
        :param allocated_characters: A set of all the characters the `font_xml` already has an allocation for.
        :param char_options:
            An optional dictionary of character options.
            Get this from :meth:`mcfonts.providers.options.OptionsProvider.get_options_for_char`.

            This is deprecated since v0.6 and will be removed in v0.7.
        :raises mcfonts.exceptions.CharacterPaddingError: If character is a padding character.
        """

    @abc.abstractmethod
    def get_ascent(self) -> int:
        """Ascent of the glyph."""

    @abc.abstractmethod
    def get_height(self) -> int:
        """Height of the glyph. This is not always equal to the glyph's image, if applicable."""

    @abc.abstractmethod
    def get_program(
        self,
        char_options: dict | None = None,
    ) -> list[str, int] | None:
        """
        Type 2 charstring program. This is used in exporting and can be cached for better performance.

        :param char_options:
            A specialized dictionary that should be derived from an instance of
            :class:`mcfonts.providers.options.OptionsProvider`.

            This is deprecated since v0.6 and will be removed in v0.7.
        """

    @abc.abstractmethod
    def construct_program(self, pixel_size: int, options: dict | None = None) -> list[str | int] | None:
        """
        Create a Type 2 charstring program.

        If the glyph is empty or has no white pixels, None will be returned.
        Otherwise, a list *(the program)* will be returned.

        .. warning::

            These charstrings are **not** optimized or checked for overlaps.
            In FontForge, use :menuselection:`E&lement -> O&verlap -> &Remove Overlap` manually afterward.

        :param pixel_size:
            How big each pixel should be.
        :param options:
            A specialized dictionary that should be derived from an instance of
            :class:`mcfonts.providers.options.OptionsProvider`.

            Should be in the form of {field*: value}.
            For example, an Options dictionary of ``{"width": {"a": 4}, "spacing": {"a": 2}}``
            should transform into ``{"width": 4, "spacing": 2}``;
            use :meth:`mcfonts.providers.options.OptionsProvider.get_options_for_char` for this.

            This is deprecated since v0.6 and will be removed in v0.7.
        :returns:
            A list of strings of the glyph's program, or None if there was no pixel data in ``glyph``.
        """


@dataclasses.dataclass
class BitmapGlyph(Glyph):
    """
    A bitmap glyph.

    Must contain an image and ascent.
    Height, ascent, and bearings are optional.
    Bearings and width are lazily-loaded.
    """

    image: PIL.Image.Image
    """Required image."""
    ascent: int
    """Required ascent."""
    height: int | None = None
    """Optional height. Lazy default is 8 if None."""
    width: int | None = None
    """Optional width. Lazy default is `self.image.width`."""
    bearings: tuple[int, int] | None = None
    """Optional padding from the edges of the canvas."""
    program: list[str, int] | None = None
    """Optional Type 2 charstring program of the glyph."""

    def get_bearings(self) -> tuple[int, int]:
        """
        From :func:`mcfonts.utils.resources.get_image_bearings`:

        | Bearings are a "padding" from the edge of the canvas to image pixels.
        | Left bearing is the distance from the left edge of the canvas to the most-left pixel data.
        | Right bearing is the distance from the right edge of the canvas to the most-right pixel data.

        This is lazily-loaded.
        """
        if self.bearings is None:
            self.bearings = mcfonts.utils.image.get_image_bearings(self.image)
        return self.bearings

    def get_width(self) -> int:
        """
        Width of the glyph's image.

        This is lazily-loaded.
        """
        if self.width is None:
            self.width = self.image.width
        return self.width

    def get_image(self) -> PIL.Image.Image:
        """The image of the glyph."""
        if self.image.mode not in {"RGBA", "LA"}:
            self.image = self.image.convert("RGBA")
        return self.image

    def get_height(self) -> int:
        """
        The height of the glyph; this is not necessarily the glyph's image width.

        This is lazily-loaded.
        """
        if self.height is None:
            self.height = 8
        return self.height

    def get_ascent(self) -> int:
        """The glyph's ascent."""
        return self.ascent

    def get_program(
        self,
        char_options: dict | None = None,
    ) -> list[str, int] | None:
        if self.program is None:
            self.program = self.construct_program(
                # Em size (1000) divided by 8 (standard width) = 125,
                # divide this by scale (glyph height / JSON height) to get how big each "pixel" will translate to.
                125 // (self.image.height // self.get_height()),
                char_options,
            )
        return self.program

    def export_to_character(
        self,
        font_xml: lxml.etree._Element,
        character: str,
        allocated_characters: set[str] | None = None,
        char_options: dict | None = None,
    ) -> None:
        if allocated_characters is None:
            allocated_characters = set()
        if character in mcfonts.constants.PADDING_CHARS:
            raise mcfonts.exceptions.CharacterPaddingError()
        if character not in allocated_characters:
            mcfonts.utils.exporting.allocate_char(font_xml, character)
        if program := self.get_program(char_options):  # If we have a program.
            mcfonts.utils.exporting.set_program_to_char(font_xml, program, character)
        else:
            # Nothing here; it was a space.
            mcfonts.utils.exporting.set_space_to_char(font_xml, character, 1)

    def construct_program(self, pixel_size: int, options: dict | None = None) -> list[str | int] | None:
        if options is None:
            options = {}
        if (bearings := self.get_bearings()) == (0, 0):
            return None
        pen = fontTools.pens.t2CharStringPen.T2CharStringPen(0, {})
        modifiers = [0, 0]
        width = bearings[1]
        spacing = 1
        if options.get("fullwidth", False) is True:
            width = self.get_width()
        # If shift is [0, 0], ignore it.
        if options.get("shift", [0, 0]) != [0, 0]:
            modifiers = options["shift"]
        if options.get("spacing") is not None:
            spacing = options["spacing"]
        if options.get("width") is not None:
            width = options["width"]

        ascent = self.get_ascent()
        height = self.get_image().height

        for index, pixel in enumerate(self.get_image().convert("LA").getdata(1)):
            if pixel >= BITMAP_EXPORT_PIXEL_THRESHOLD:
                glyph_width = self.get_image().width
                x_real = (index % glyph_width) + modifiers[0]
                y_real = height - (index // glyph_width) + ascent + modifiers[1]
                pen.moveTo(
                    (
                        x_real * pixel_size,
                        y_real * pixel_size,
                    )
                )  # Left X, top right.

                pen.lineTo(
                    (
                        (x_real + 1) * pixel_size,
                        y_real * pixel_size,
                    )
                )  # Down Y, bottom left.

                pen.lineTo(
                    (
                        (x_real + 1) * pixel_size,
                        (y_real - 1) * pixel_size,
                    )
                )  # Right X, bottom right.

                pen.lineTo(
                    (
                        x_real * pixel_size,
                        (y_real - 1) * pixel_size,
                    )
                )  # Done with pixel.

                pen.closePath()
        program: list[int | str] = pen.getCharString().program
        program[0] = (width + spacing) * pixel_size  # Set the width correctly.
        return program


@dataclasses.dataclass
class SpaceGlyph(Glyph):
    """
    A space glyph.

    Contans one required field, the glyph's width.
    """

    width: int
    """The width of the glyph."""
    program: list[str, int] | None = None
    """Optional Type 2 charstring program of the glyph."""

    def export_to_character(
        self,
        font_xml: lxml.etree._Element,
        character: str,
        allocated_characters: set[str],
        char_options: dict | None = None,
    ) -> None:
        width = self.get_width()
        if math.isinf(width) or math.isnan(width):
            width = 20
        if character not in allocated_characters:
            mcfonts.utils.exporting.allocate_char(font_xml, character)
        mcfonts.utils.exporting.set_space_to_char(font_xml, character, width)

    def get_width(self) -> int:
        return self.width

    def get_ascent(self) -> int:
        return 1

    def get_height(self) -> int:
        return 8

    def get_program(
        self,
        char_options: dict | None = None,
    ) -> list[str, int] | None:
        if self.program is None:
            self.program = self.construct_program(125)
        return self.program

    def construct_program(self, pixel_size: float, options: dict | None = None) -> list[str | int] | None:
        return [int(min(abs((self.get_width() * pixel_size)), SPACE_EXPORT_MAX_ADVANCE)), "endchar"]


@dataclasses.dataclass
class UnihexGlyph(Glyph):
    """
    A unihex glyph.

    Must contain a bit string.
    Width, image, and bearings are optional.
    Width, image, and bearings are lazily-loaded.

    TODO more stuff here about what it is, what it does, etc.
    """

    bit_string: str
    """The bit string; does not include the `codepoint:` starting portion."""
    width: int | None
    """The width of the glyph. Equal to ``len(self.bit_string) // 4``."""
    image: PIL.Image.Image | None
    """
    An optional image of the glyph, comparable to a :class:`BitmapGlyph`.
    If possible, try not to use this.
    """
    bearings: tuple[int, int] | None
    """An optional tuple of the glyph's bearings, comparable to a :class:`BitmapGlyph`."""
    size_override: tuple[int, int] | None
    """
    An optional tuple of the glyph's size override.
    
    The first value is the starting column, and the second value is the ending column.
    When exporting, data outside of these columns will be discarded.
    If this is None, this is lazily-calculated to be ``(0, self.get_width())``.
    """
    program: list[str, int] | None = None
    """Optional Type 2 charstring program of the glyph."""

    def export_to_character(
        self,
        font_xml: lxml.etree._Element,
        character: str,
        allocated_characters: set[str],
        char_options: dict | None = None,
    ) -> None:
        if character not in allocated_characters:
            mcfonts.utils.exporting.allocate_char(font_xml, character)
        if program := self.get_program(char_options):  # If we have a program.
            mcfonts.utils.exporting.set_program_to_char(font_xml, program, character, False)
        else:
            # Nothing here; it was a space.
            mcfonts.utils.exporting.set_space_to_char(font_xml, character, 1, False)

    def get_width(self) -> int:
        if self.width is None:
            self.width = len(self.bit_string) >> 2
        return self.width

    def get_image(self) -> PIL.Image.Image:
        """
        The image of the glyph.

        This is lazily-loaded.
        """
        if self.image is None:
            self.image = mcfonts.utils.unihex.bit_string_to_image(self.bit_string)
        return self.image

    def get_bit_string(self) -> str:
        """The bit string is the portion after the ``codepoint:``."""
        return self.bit_string

    def get_bearings(self) -> tuple[int, int]:
        """See :func:`mcfonts.utils.unihex.get_unihex_bearings`."""
        if self.bearings is None:
            self.bearings = mcfonts.utils.unihex.get_unihex_bearings(self.get_bit_string())
        return self.bearings

    def get_ascent(self) -> int:
        return 1

    def get_height(self) -> int:
        return 8

    def get_program(
        self,
        char_options: dict | None = None,
    ) -> list[str, int] | None:
        if self.program is None:
            self.program = self.construct_program(
                # Em size (1000) divided by 10 = 100
                # divide this by scale (glyph height / JSON height) to get how big each "pixel" will translate to.
                125,
                char_options,
            )
        return self.program

    def construct_program(self, pixel_size: int, options: dict | None = None) -> list[str | int] | None:
        pen = fontTools.pens.t2CharStringPen.T2CharStringPen(0, {})
        glyph_width = self.get_width()
        size = self.get_size_override()
        index = 0
        bearings = self.get_bearings()
        for row in mcfonts.utils.unihex.bit_string_to_rows(self.get_bit_string()):
            for pixel in row:
                if pixel == UNIHEX_EXPORT_PIXEL_ON:
                    x_real = index % glyph_width
                    # - 1 to correct for baseline
                    y_real = (index // glyph_width) - 1
                    if x_real < min(size[0], 0) or x_real > min(size[1], glyph_width):
                        # Size overrides say to cut it off
                        continue
                    x_real -= bearings[0]
                    pen.moveTo(
                        (
                            x_real * pixel_size,
                            y_real * pixel_size,
                        )
                    )  # Left X, top right.

                    pen.lineTo(
                        (
                            (x_real + 1) * pixel_size,
                            y_real * pixel_size,
                        )
                    )  # Down Y, bottom left.

                    pen.lineTo(
                        (
                            (x_real + 1) * pixel_size,
                            (y_real - 1) * pixel_size,
                        )
                    )  # Right X, bottom right.

                    pen.lineTo(
                        (
                            x_real * pixel_size,
                            (y_real - 1) * pixel_size,
                        )
                    )  # Done with pixel.

                    pen.closePath()
                index += 1
        program: list[int | str] = pen.getCharString().program
        program[0] = (bearings[1] - bearings[0] + 1) * pixel_size  # Set the width correctly.
        return program

    def get_size_override(self) -> tuple[int, int]:
        """Size override is a tuple of 2 integers of the starting and ending columns for a glyph."""
        if self.size_override is None:
            self.size_override = (0, self.get_width())
        return self.size_override


AnyGlyph = BitmapGlyph | SpaceGlyph | UnihexGlyph
"""
Any glyph, either Bitmap, Space, or Unihex.

However, the method names will obviously vary. Check instances first.
All of these inherit from the metaclass :class:`Glyph`.
"""
