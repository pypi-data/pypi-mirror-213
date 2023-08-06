#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""A bitmap provider, handling PNG glyphs."""
import collections.abc
import os
import typing

import PIL.Image
import PIL.ImageChops
import jsonschema
import unirange

import mcfonts.constants
import mcfonts.glyphs
import mcfonts.providers.base
import mcfonts.utils.image
import mcfonts.utils.schemas
import mcfonts.utils.unicode


class BitmapProvider(mcfonts.providers.base.BaseProvider):
    """
    The ``bitmap`` provider defines simple bitmap glyphs from a texture.

    It references a single PNG file and declares a "chars" list of strings.

    The characters inside each string entry inside the charlist will be
    mapped to the corresponding positions in the referenced file.

    The texture is evenly divided according to the number of entries and the length of these entries.
    """

    minimum_pack_format = 3
    icon = "🖼"

    def __init__(self, provider: dict, origin: os.PathLike | str, resource: PIL.Image.Image | None):
        self.contents = provider
        self.resource: PIL.Image.Image | None = resource
        self.glyph_cell = (0, 0)
        self.contents["height"] = self.contents.get("height", 8)  # Default height fallback
        if self.resource:
            if len(self.contents["chars"]) > 0:
                self.glyph_cell = (
                    self.resource.width // len(self.contents["chars"][0] or ""),
                    self.resource.height // len(self.contents["chars"]),
                )
            else:
                self.glyph_cell = (self.resource.width, self.resource.height)
        self.glyphs: dict[str, mcfonts.glyphs.BitmapGlyph] = dict(self.construct_glyphs(True))
        super().__init__("bitmap", provider, origin, set(self.yield_characters()))
        self.validate()

    def pretty_print(self) -> str:
        return f"{self.icon} bitmap: {self.contents.get('file', 'no resource')}, {len(self.glyphs):,} chars"

    def validate(self) -> None:
        jsonschema.validate(self.contents, mcfonts.utils.schemas.SCHEMA_PROVIDER_BITMAP)
        validate_charlist(self.contents["chars"], self.resource, self.glyph_cell)
        if self.resource:
            height = self.contents["height"]
            glyph_height = self.glyph_cell[1]
            if glyph_height % height != 0:
                mcfonts.logger.warning(
                    (
                        f"Provider has an invalid height ({height}), "
                        f"it must be a multiple of the glyph's height ({glyph_height})"
                    ),
                )
            if self.glyph_cell[0] > 256 or self.glyph_cell[1] > 256:
                # The limit for a character is 256, anything beyond is an error in atlas-stitching.
                # Will still try to make it work, but make no guarantee.
                mcfonts.logger.warning(
                    (
                        "Provider has excessively large glyph size, maximum character cell size is 256, "
                        f"but got {max(self.glyph_cell[0], self.glyph_cell[1])}."
                    ),
                )

    def get_glyphs_in_unirange(
        self, unirange_notation: str, include_missing: bool = False
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.BitmapGlyph | None]] | None:
        """
        Given `unirange_notation`, return a dictionary of the requested characters to their glyphs.

        :param unirange_notation:
            A string representing the requested range of chars.
            See https://pypi.org/project/unirange/.
        :param include_missing:
            Whether to yield characters for which there is no glyph.
        :returns:
            A yield of the requested glyphs that match `unirange_notation`.
            If `include_missing`, None will be yielded for missing characters.
        """
        if not self.resource:
            return
        for char in unirange.unirange_to_characters(unirange_notation):
            glyph = self.glyphs.get(char)
            if glyph is None and include_missing:
                yield char, None
            else:
                yield char, glyph

    def print_info(self, table_chars: bool = True) -> None:
        """
        Print information about this provider.

        :param table_chars:
            Whether to print a 'chars' list as a square table, or as a simple string.
        """
        super().print_info()
        print(f"File: {self.contents.get('file', mcfonts.constants.UNKNOWN_FIELD)}")
        print(f"Height: {self.contents.get('height', mcfonts.constants.UNKNOWN_FIELD)}")
        print(f"Ascent: {self.contents.get('ascent')}")
        if table_chars:
            print(f"Chars: ({len(self.contents['chars'][:1]):,}x{len(self.contents['chars']):,})")
            for charline in self.contents["chars"]:
                print(f"\t{' '.join(charline)}")
        else:
            print(f"Chars: {' '.join(''.join(self.contents['chars']))}")
        print(f"Count: {sum(len(x) for x in self.contents['chars']):,}")

    def construct_glyphs(
        self,
        ignore_empty_textures: bool = False,
    ) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.BitmapGlyph] | None]:
        """
        Extract every textured glyph from this provider.

        Each glyph includes its height and ascent. You can calculate the baseline from this.

        :param ignore_empty_textures: Whether to not include characters that have no pixel data.
        :returns: A yield of ``{codepoint: BitmapGlyph | None}``.
        """
        if not self.resource:
            return ()
        for y_index, charline in enumerate(self.contents["chars"]):
            if is_charline_empty(charline):
                continue
            for x_index, char in enumerate(charline):
                if char in mcfonts.constants.PADDING_CHARS:
                    continue

                glyph = self.resource.crop(
                    (
                        x_index * self.glyph_cell[0],
                        y_index * self.glyph_cell[1],
                        (x_index + 1) * self.glyph_cell[0],
                        (y_index + 1) * self.glyph_cell[1],
                    )
                )
                empty = mcfonts.utils.image.is_image_empty(glyph)
                if not empty:
                    height = self.contents["height"]
                    ascent = self.contents["ascent"]
                    yield char, mcfonts.glyphs.BitmapGlyph(
                        glyph, (ascent - height) * (self.glyph_cell[1] // height), height
                    )
                elif empty and not ignore_empty_textures:
                    yield char, None
        return ()

    def yield_glyphs(self) -> collections.abc.Iterable[tuple[str, mcfonts.glyphs.BitmapGlyph]]:
        yield from self.glyphs.items()

    def yield_characters(self, ignore_padding: bool = True) -> collections.abc.Iterable[str]:
        for charline in self.contents.get("chars", []):
            if ignore_padding and is_charline_empty(charline):
                continue
            for char in charline:
                if ignore_padding or char not in mcfonts.constants.PADDING_CHARS:
                    yield char

    def get_glyph_for_char(self, character: str) -> mcfonts.glyphs.BitmapGlyph | None:
        """
        Extract a desired character's sheet from this provider.

        Glyph textures that are mapped to spaces or null padding return None.
        If there's more than one sheet mapped to a character (duplicate characters),
        the first occurance will be returned.

        :param character: A single character.
        :returns: A :class:`PIL.Image.Image`, or None if no glyph exists.
        """
        # Ignore non-bitmap provider, or if codepoint is null or space.
        # (glyphs can't be assigned for padding characters).
        if character in mcfonts.constants.PADDING_CHARS or self.resource is None:
            return None
        return self.glyphs.get(character)

    def reload_to_monochrome(self) -> bool:
        """
        Replace the resource used in this provider with a grayscale version.

        If the resource is already grayscale or if there's no resource, False will be returned.
        Otherwise, True.

        This modifies the resource of this provider in place, and **can't be undone**.

        :returns: Boolean of success; if there's a resource, and it isn't already grayscale.
        """
        if self.resource:
            if self.resource.mode == "LA":
                return False
            self.resource = self.resource.convert("LA")
            return True
        return False


def pad_charlist(
    charlist: list[str],
    pad_amount: int = 0,
    pad_char: str = " ",
    pad_from: typing.Literal["left", "right"] = "right",
) -> list[str]:
    """
    Pad `charlist` so that all its strings have the same length.

    >>> pad_charlist(["abc", "de"])
    ['abc', 'de ']
    >>> pad_charlist(["abc", "defg"])
    ['abc ', 'defg']

    :param charlist: Character list to pad.
    :param pad_amount: What to pad the characters to; the ideal width.
        If this is 0, this will be determined from the largest length of strings in `charlist`.
    :param pad_char: The character to pad with, default is a space.
    :param pad_from: Direction to pad the string from, left => "___Text", right => "Text___".
    :returns: The padded charlist list.
    """
    if pad_from not in {"left", "right"}:
        raise ValueError('pad_from must be "left" or "right"')
    if pad_amount == 0:
        # Get the largest string based on length
        pad_amount = len(max(charlist, key=len))
    for index, charline in enumerate(charlist):
        if len(charline) != pad_amount:
            if pad_from == "left":
                # Rjust means justify to right
                charlist[index] = charline.rjust(pad_amount, pad_char[0])
            else:
                # Ljust means justify to left
                charlist[index] = charline.ljust(pad_amount, pad_char[0])
    return charlist


def assert_charlist_is_equal(charlist: list[str]) -> tuple[bool, int]:
    """
    Ensure that every string inside `charlist` has the same length as the first string.

    >>> assert_charlist_is_equal(["abc","de"])
    (False, 3)
    >>> assert_charlist_is_equal(["abc","def"])
    (True, 3)
    >>> assert_charlist_is_equal([])
    (True, 0)
    >>> assert_charlist_is_equal([""])
    (True, 0)

    :param charlist: The charlist of strings to check lengths of.
    :returns: A tuple of (if the lengths are equal, the expected length).
    """
    if len(charlist) == 0:
        return True, 0
    ideal = len(max(charlist, key=len))
    for charline in charlist:
        if len(charline) != ideal:
            return False, ideal
    return True, ideal


def resource_to_charlist(resource: PIL.Image.Image, char: str, cell_bounds: tuple[int, int] = (8, 8)) -> list[str]:
    """
    Given a path to a resource and a starting character, return an appropriate charlist.

    Return a provider that has a charlist that correctly encompasses all chars covered by
    the resource. Glyphs in the resource that are empty are skipped.

    :param resource: The resource to grab textures from.
    :param char:
        A single character.
        The codepoint of this will increase by 1 on every glyph.
    :param cell_bounds:
        The dimensions of an individual glyph in `resource`.
        Glyph dimensions must be the same throughout the whole of `resource`.
    :returns: A `chars` list.
    """
    charlist: list[str] = []
    charline: list[str] = []
    codepoint = ord(char)
    height = resource.height // cell_bounds[1]
    width = resource.width // cell_bounds[0]
    for height_offset in range(height):
        for width_offset in range(width):
            if mcfonts.utils.image.is_image_empty(
                resource.crop(
                    (
                        width_offset * cell_bounds[0],
                        height_offset * cell_bounds[1],
                        (width_offset + 1) * cell_bounds[0],
                        (height_offset + 1) * cell_bounds[1],
                    )
                )
            ):
                charline.append(" ")
            else:
                charline.append(chr(codepoint))
            codepoint += 1
        charlist.append("".join(charline))
        charline.clear()
    return charlist


def validate_charlist(
    charlist: list[str],
    resource: PIL.Image.Image | None = None,
    cell_bounds: tuple[int, int] = (8, 8),
):
    r"""
    Given `charlist`, ensure that it's valid and doesn't have any possible issues.

    Issues include:

    * Empty lines,
    * Uneven lines,
    * Duplicate characters,
    * \*Padding chars in places where glyph exists in `resource`,
    * \*Characters that will have an empty glyph in `resource`.

    \* Optional, requires `resource`.

    :param charlist: A charlist to validate.
    :param resource: An optional :class:`PIL.Image.Image` to validate glyph textures against.
    :param cell_bounds: Tuple of (glyph width, glyph height) for each glyph in `resource`.
    """
    char_traces: dict[str, tuple[int, int]] = {}
    for y_index, charline in enumerate(charlist):
        if not (len_charline := len(charline)):
            mcfonts.logger.warning(f"Charline {y_index:,} is empty.")
        elif not (charlist_length := assert_charlist_is_equal(charlist))[0]:
            mcfonts.logger.warning(
                (
                    "Uneven amount of characters in charlist,"
                    f"expected {charlist_length[1]:,}, got {len_charline:,} on line {y_index:,}."
                ),
            )
        for x_index, character in enumerate(charline):
            if character not in mcfonts.constants.PADDING_CHARS and character in char_traces:
                trace = char_traces[character]
                mcfonts.logger.warning(
                    (
                        f"Duplicate character {mcfonts.utils.unicode.pretty_print_char(character)} "
                        f"on charline {y_index:,} index {x_index:,}. "
                        f"Character was already defined at charline {trace[0]:,} index {trace[1]:,}."
                    ),
                )
            else:
                char_traces[character] = (y_index, x_index)
            if resource:
                if mcfonts.utils.image.is_image_invisible(
                    resource.crop(
                        (
                            x_index * cell_bounds[0],
                            y_index * cell_bounds[1],
                            (x_index + 1) * cell_bounds[0],
                            (y_index + 1) * cell_bounds[1],
                        )
                    )
                ) and not mcfonts.utils.unicode.is_char_invisible(character):
                    mcfonts.logger.debug(
                        (
                            "Empty glyph for character "
                            f"{mcfonts.utils.unicode.pretty_print_char(character)} on "
                            f"charline {y_index:,} index {x_index:,}."
                        ),
                    )


def fit_chars_into_charlist(chars: list[str], charlist_length: int = 16) -> collections.abc.Iterable[str]:
    """
    Given a list of chars, fit them into a charlist whose width is equal to `charlist_length`.

    >>> list(fit_chars_into_charlist(["thisisareallylongcharlist"]))
    ['thisisareallylon', 'gcharlist']
    >>> list(fit_chars_into_charlist(["thisisareallylongcharlist"], 5))
    ['thisi', 'sarea', 'llylo', 'ngcha', 'rlist']

    :param chars: A list of chars.
    :param charlist_length: The width to make each line of characters in the charlist equal to.
    :returns: Yield of lines in a charlist.
    """
    chars = list(charlist_to_chars(chars))
    for i in range(0, len(chars), charlist_length):
        yield "".join(char for char in chars[i : i + charlist_length])


def charlist_to_chars(charlist: list[str]) -> collections.abc.Iterable[str]:
    """
    Given `charlist`, yield all the characters that charlist covers.

    >>> chars = ['agtg', 'b', '5', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8']
    >>> list(charlist_to_chars(chars)
    ['a', 'g', 't', 'g', 'b', '5', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8']

    :param charlist: The charlist.
    :returns: A yield of characters.
    """
    for charline in charlist:
        # iterating over lines, charline is a string
        for character in charline:
            # iterating over chars, char is a str[1]
            yield character


def is_charline_empty(charline: str) -> bool:
    r"""
    Given `charline`, return if it contains only spaces or null bytes.

    >>> is_charline_empty("\0\0\0\x20\x20\x20\0\0")
    True
    >>> is_charline_empty("         ")
    True
    >>> is_charline_empty("      xxx")
    False

    :param charline: A single string, likely part_notation of a wider charlist.
    :returns: If `charline` is all spaces or null bytes.
    """
    return all(x in mcfonts.constants.PADDING_CHARS for x in charline)


def charlist_from_unicode_range(start: str, end: str, width: int = 16) -> list[str]:
    r"""
    | Given a starting character `start`, and an ending character `end`,
    | return a charlist that contains these characters in order,
    | and whose width is equal to `width`.

    >>> charlist_from_unicode_range("\u2600", "\u26ff")
    [
        '☀☁☂☃☄★☆☇☈☉☊☋☌☍☎☏',
        '☐☑☒☓☔☕☖☗☘☙☚☛☜☝☞☟',
        '☠☡☢☣☤☥☦☧☨☩☪☫☬☭☮☯',
        '☰☱☲☳☴☵☶☷☸☹☺☻☼☽☾☿',
        '♀♁♂♃♄♅♆♇♈♉♊♋♌♍♎♏',
        '♐♑♒♓♔♕♖♗♘♙♚♛♜♝♞♟',
        '♠♡♢♣♤♥♦♧♨♩♪♫♬♭♮♯',
        '♰♱♲♳♴♵♶♷♸♹♺♻♼♽♾♿',
        '⚀⚁⚂⚃⚄⚅⚆⚇⚈⚉⚊⚋⚌⚍⚎⚏',
        '⚐⚑⚒⚓⚔⚕⚖⚗⚘⚙⚚⚛⚜⚝⚞⚟',
        '⚠⚡⚢⚣⚤⚥⚦⚧⚨⚩⚪⚫⚬⚭⚮⚯',
        '⚰⚱⚲⚳⚴⚵⚶⚷⚸⚹⚺⚻⚼⚽⚾⚿',
        '⛀⛁⛂⛃⛄⛅⛆⛇⛈⛉⛊⛋⛌⛍⛎⛏',
        '⛐⛑⛒⛓⛔⛕⛖⛗⛘⛙⛚⛛⛜⛝⛞⛟',
        '⛠⛡⛢⛣⛤⛥⛦⛧⛨⛩⛪⛫⛬⛭⛮⛯',
        '⛰⛱⛲⛳⛴⛵⛶⛷⛸⛹⛺⛻⛼⛽⛾⛿'
    ]
    >>> charlist_from_unicode_range(" ", "\xff", 8)
    [
        ' !"#$%&'',
        '()*+,-./',
        '01234567',
        '89:;<=>?',
        '@ABCDEFG',
        'HIJKLMNO',
        'PQRSTUVW',
        'XYZ[\\]^_',
        '`abcdefg',
        'hijklmno',
        'pqrstuvw',
        'xyz{|}~\x7f',
        '\x80\x81\x82\x83\x84\x85\x86\x87',
        '\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f',
        '\x90\x91\x92\x93\x94\x95\x96\x97',
        '\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f',
        '\xa0¡¢£¤¥¦§',
        '¨©ª«¬\xad®¯',
        '°±²³´µ¶·',
        '¸¹º»¼½¾¿',
        'ÀÁÂÃÄÅÆÇ',
        'ÈÉÊËÌÍÎÏ',
        'ÐÑÒÓÔÕÖ×',
        'ØÙÚÛÜÝÞß',
        'àáâãäåæç',
        'èéêëìíîï',
        'ðñòóôõö÷',
        'øùúûüýþÿ'
    ]

    :param start: The starting single character.
    :param end:
        The ending single character.
        Codepoint must be greater than the codepoint of `start`.
    :param width: The number of characters to put in one row of the returned charlist.
    :returns: A charlist, with each string's length equal to `width`.
    """
    start_codepoint = ord(start)
    end_codepoint = ord(end)
    if end_codepoint <= start_codepoint:
        return []
    return list(fit_chars_into_charlist([chr(c) for c in range(start_codepoint, end_codepoint + 1)], width))
