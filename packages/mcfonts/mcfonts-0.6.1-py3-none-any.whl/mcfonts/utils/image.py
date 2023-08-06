#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""Simple utilities for working with :class:`PIL.Image.Image`."""
from __future__ import annotations

import typing

import PIL.Image
import PIL.ImageOps


def is_image_empty(image: PIL.Image.Image) -> bool:
    """
    Determine if `image` has any pixel data.

    :param image: A :class:`PIL.Image.Image`.
    :returns: If `image` has pixel data.
    """
    extrema: tuple[int | tuple[int]] = image.getextrema()
    if isinstance(extrema[0], int):
        return extrema[0] == 0 and extrema[1] == 0
    band: tuple[int]
    for band in extrema:
        try:
            if band[0] != 0 or band[1] != 0:
                return False
        except IndexError:
            if band != 0:
                return False
    return True


def is_image_invisible(image: PIL.Image.Image) -> bool:
    """
    Determine if `image` has all invisible pixels; if alpha is 0.

    :param image: A :class:`PIL.Image.Image`.
    :returns: If `image` doesn't have any full-alpha pixels.
    """
    if image.mode == "RGBA":
        return all(pixel == 0 for pixel in image.getdata(3))
    if image.mode == "LA":
        return all(pixel == 0 for pixel in image.getdata(1))
    return False


def get_largest_effective_image_dimensions(
    images: list[PIL.Image.Image], isolate_dimensions: bool = True
) -> tuple[int, int]:
    """
    Given a list of images, return the width and height of the largest images in that list.

    This function operates based on the pixels inside an image;
    it crops out empty space and then determines the width and height.
    For a function that operates on an image's true width and height, see func:`get_largest_image_dimensions`.

    :param images: An iterable of the images to iterate over.
    :param isolate_dimensions:
        If True, the maximum height and width will be calculated.
        This means that dimensions (4, 6) (12, 8) (3, 9) will be (12, 9).

        If False, the maximum height and width is dependent on the maximum width found.
        This means that dimensions (4, 6) (12, 8) (3, 9) will be (12, 8).
        It is recommended that you leave this to True.
    :returns: A tuple of (maximum width, maximum height).
    """
    max_width = 0
    max_height = 0
    for glyph in images:
        if glyph:
            if bbox := glyph.getbbox():
                if (width := bbox[2] - bbox[0]) > max_width:
                    max_width = width
                    if not isolate_dimensions:
                        max_height = width
                    continue
                if (height := bbox[3] - bbox[1]) > max_height:
                    max_height = height
    return max_width, max_height


def get_largest_image_dimensions(
    images: typing.Iterable[PIL.Image.Image | None], isolate_dimensions: bool = True
) -> tuple[int, int]:
    """
    Given a list of images, return the width and height of the largest image's canvas in that list.

    This function is different from func:`get_largest_effective_image_dimensions` in that it
    does not calculate the real width and height that pixels in an image extend to. It only
    relies on the width and height of the image's *canvas* (the total space).

    :param images: A list of the glyphs to iterate over.
    :param isolate_dimensions:
        If True, the maximum height and width will be calculated separately.
        This means that dimensions (4, 6) (12, 8) (3, 9) will be (12, 9).

        If False, the maximum height and width is dependent on the maximum width found.
        This means that dimensions (4, 6) (12, 8) (3, 9) will be (12, 8).

        It is recommended that you leave this to True.
    :returns: A tuple of (maximum width, maximum height).
    """
    max_width = 0
    max_height = 0
    for glyph in images:
        if glyph and glyph.getbbox():
            if (width := glyph.width) > max_width:
                max_width = width
                if not isolate_dimensions:
                    max_height = width
                continue
            if (height := glyph.height) > max_height:
                max_height = height
    return max_width, max_height


def get_image_bearings(image: PIL.Image.Image) -> tuple[int, int]:
    """
    Return the two integers of the bearings of an image.

    Bearings are a "padding" from the edge of the canvas to image pixels.
    Left bearing is the distance from the left edge of the canvas to the most-left pixel data.
    Right bearing is the distance from the right edge of the canvas to the most-right pixel data.

    If return is (0, 0), there's no pixel data, the glyph is all spaces.

    :param image: A :class:`PIL.Image.Image` instance.
    :returns:
        Left bearing and right bearing.
        Returns (0, 0) if there's no pixel data.
    """
    try:
        bbox = image.getbbox()
        if bbox is None:
            raise TypeError
        return bbox[0], bbox[2]
    except TypeError:
        # Pure space, has no width
        return 0, 0
