#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
| Compacting is the process of taking every "bitmap" character texture provided
| by a Minecraft font provider and storing it in as little space as possible.

This means:

1. Finding the largest effective dimensions out of all the characters,
2. Expanding the dimensions of all other character textures to fit those new dimensions,
3. Creating a new texture that will fit all characters in those dimensions,
4. Sequencing them one-after-another while ignoring characters with a blank texture,
5. Creating a new charlist that corresponds with the compacted texture.

This contains functions for compacting any provider(s) into individual textures
(one for each provider), and for compacting a list of providers into a single, cohesive texture.
"""
from __future__ import annotations

import math

import PIL.Image
import PIL.ImageChops

import mcfonts.glyphs
import mcfonts.utils.image


def compact_glyphs(
    glyphs: list[mcfonts.glyphs.BitmapGlyph | mcfonts.glyphs.UnihexGlyph],
    chars_in_row: int = 0,
    cell_size: tuple[int, int] = (0, 0),
    square_cells: bool = True,
) -> tuple[PIL.Image.Image, tuple[int, int]]:
    """
    | Given a list of glyphs, return an image wherein all glyphs are compacted into a single sheet,
    | with the number of glyphs in one row matches ``chars_in_row`` (excluding exceptions).

    :param glyphs:
        A list of lists of [glyphs (:class:`PIL.Image.Image`), their height, and their ascent].
        Baseline can be calculated from this: :math:`height - ascent`.
    :param chars_in_row:
        How many characters to fit inside each row of the resulting sheet.
        Only positive values will set fixed rows.
        If this is negative or 0, this will be set so that the resulting sheet is square.
        By default, this is 0 (a square).
    :param cell_size:
        What size to make each glyph cell.
        If this is (0, 0), this will be set to the largest dimensions of every glyph in `glyphs`.
        If this is any other tuple of numbers,
    :param square_cells:
        If True, each glyph's width will equal its height.
        This is based on whichever number is largest.
        If False, each glyph's width will be unrelated to its height.
    :returns:
        A tuple containing (a modified `resource` with the least amount of padding between glyphs,
        and a tuple of the size of each glyph cell).
    """
    if chars_in_row <= 0:
        chars_in_row = math.ceil(math.sqrt(len(glyphs)))

    if cell_size == (0, 0):
        max_cell = mcfonts.utils.image.get_largest_effective_image_dimensions(
            list(glyph.get_image() for glyph in glyphs)
        )
    else:
        max_cell = cell_size
    if square_cells:
        maximum = max(max_cell)
        max_cell = (maximum, maximum)

    average_baseline = round(sum(glyph.get_height() - glyph.get_ascent() for glyph in glyphs) / len(glyphs))

    destination = PIL.Image.new(
        "RGBA",
        (max_cell[0] * chars_in_row, max_cell[1] * len(glyphs) // chars_in_row),
        (0, 0, 0, 0),
    )
    for index, glyph in enumerate(glyphs):
        destination.paste(
            PIL.ImageChops.offset(glyph.get_image(), 0, average_baseline - glyph.get_height() - glyph.get_ascent()),
            (
                (index % chars_in_row) * max_cell[0],
                (index // chars_in_row) * max_cell[1],
            ),
        )
    return destination, max_cell


def compact_images(
    images: list[PIL.Image.Image | None],
    chars_in_row: int = 0,
    cell_size: tuple[int, int] = (0, 0),
    square_cells: bool = True,
    include_empty_images: bool = True,
) -> tuple[PIL.Image.Image, tuple[int, int]]:
    """
    Similar to :func:`compact_glyphs` except that it works on plain :class:`~PIL.Image.Image` instead.
    """

    if not include_empty_images:
        images = list(image for image in images if image is not None)
    if chars_in_row <= 0:
        chars_in_row = math.ceil(math.sqrt(len(images)))

    if cell_size == (0, 0):
        max_cell = mcfonts.utils.image.get_largest_effective_image_dimensions(images)
    else:
        max_cell = cell_size
    if square_cells:
        maximum = max(max_cell)
        max_cell = (maximum, maximum)

    destination = PIL.Image.new(
        "RGBA",
        (max_cell[0] * chars_in_row, max_cell[1] * len(images) // chars_in_row),
        (0, 0, 0, 0),
    )
    for index, glyph in enumerate(images):
        if glyph:
            destination.paste(
                glyph,
                (
                    (index % chars_in_row) * max_cell[0],
                    (index // chars_in_row) * max_cell[1],
                ),
            )
    return destination, max_cell
