#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Coverage reports are instances of :class:`mcfonts.coverage_reports.CoverageReport`.

They contain information on the :term:`coverage` of a specific font,
and contain functions for displaying this information.
"""
from __future__ import annotations

import typing
import unicodedata

import tinyunicodeblock

import mcfonts.utils.colors

PRIVATE_USE_PREFIX: str = "Private Use"


class CoverageReport:
    """
    A coverage report.

    Contains information of the number of characters covered, and the blocks covered.
    """

    def __init__(self, chars: set[str], blocks: dict[str, int]):
        """
        :param chars: A set of individual characters.
        :param blocks: A dictionary of ``{block name: chars covered}``.
        """
        self.chars: set[str] = chars
        """
        A set of the characters.
        """
        self.blocks: dict[str, int] = blocks
        """
        A dictionary of ``{block name: number of characters of this block}``.
        """

    def block_progress(self, show_empty: bool = True) -> None:
        """
        Print the block progress in each block.

            ✓ Basic Latin (U+0000-U+007F) [95/95, 100.00%]
            ~ Latin-1 Supplement (U+0080-U+00FF) [94/96, 97.92%]

        And, if `show_empty`:

            ❌ Arabic (U+0600-U+06FF) [0/255, 0.00%]

        :param show_empty:
            If True, blocks with no support will be shown.
            If False, blocks with no support will be omitted.
        """
        for block in tinyunicodeblock.BLOCKS_BYNAME:
            info = tinyunicodeblock.BLOCKS_BYNAME[block]
            start = ord(info[0])
            end = ord(info[1])
            number = self.blocks.get(block, 0)
            amount = end - start - info[2] + 1
            if block in self.blocks:
                if number >= amount:
                    if mcfonts.utils.colors.USE_COLORS:
                        print(f"{mcfonts.utils.colors.GREEN_FORE}✓ {block}{mcfonts.utils.colors.RESET_FORE}", end=" ")
                    else:
                        print(f"✓ {block}", end=" ")
                else:
                    if mcfonts.utils.colors.USE_COLORS:
                        print(f"{mcfonts.utils.colors.YELLOW_FORE}~ {block}{mcfonts.utils.colors.RESET_FORE}", end=" ")
                    else:
                        print(f"~ {block}", end=" ")
            elif show_empty:
                if mcfonts.utils.colors.USE_COLORS:
                    print(f"{mcfonts.utils.colors.RED_FORE}❌ {block}{mcfonts.utils.colors.RESET_FORE}", end=" ")
                else:
                    print(f"❌ {block}", end=" ")
            try:
                print(f"(U+{start:04X}-U+{end:04X}) [{number}/{amount}, {number / amount * 100:.2f}%]")
            except ZeroDivisionError:
                print(f"(U+{start:04X}-U+{end:04X}) [{number}, {number}.00%]")

    def compare(self, other: typing.Self) -> None:
        """
        Given `other`, a second instance of :class:`CoverageReport`, compare the two, using `self` as a baseline.

        The information compared is:

        * Character count
        * Blocks covered

        :param other: A second instance of :class:`mcfonts.coverage_reports.CoverageReport` to compare to.
        """
        if mcfonts.utils.colors.USE_COLORS:
            print(f"{mcfonts.utils.colors.BRIGHT}COUNTS{mcfonts.utils.colors.RESET_ALL}")
        else:
            print("COUNTS")
        print(":: stat: this | other (delta)")
        len_self = len(self.chars)
        len_other = len(other.chars)
        print(
            f"Characters: {len_self:,} | {len_other:,} " f"({mcfonts.utils.colors.color_number(len_other - len_self)})"
        )
        len_blocks = (len(self.blocks), len(other.blocks))
        print(
            f"Blocks: {len_blocks[0]:,} | {len_blocks[1]:,} ("
            f"{mcfonts.utils.colors.color_number(len_blocks[1] - len_blocks[0])})\n"
        )
        if mcfonts.utils.colors.USE_COLORS:
            print(f"{mcfonts.utils.colors.BRIGHT}BLOCKS{mcfonts.utils.colors.RESET_ALL}")
        else:
            print("BLOCKS")
        print(":: block: this | other (delta)")
        for block_name in (self.blocks | other.blocks).keys():
            block_info: tuple[int, int] = tinyunicodeblock.BLOCKS_BYNAME.get(block_name, (0, 0))
            block_this = self.blocks.get(block_name) or 0
            block_other = other.blocks.get(block_name) or 0
            print(f"{chr(block_info[0] + 14)} ", end="")
            if mcfonts.utils.colors.USE_COLORS:
                print(f"{mcfonts.utils.colors.BRIGHT}{block_name}{mcfonts.utils.colors.RESET_ALL}")
            else:
                print(block_name)
            print(
                f"\t{block_this:,}/{block_info[1]:,} | {block_other:,}/{block_info[1]:,} "
                f"({mcfonts.utils.colors.color_number(block_other - block_this)})"
            )

    def char_table(self, show_offsets: bool = True, no_glyph_char: str = "▯") -> None:
        """
        Print a table of every character in this font.

                ▼ Block Elements (U+2580-U+259F) ▼
                   0 1 2 3 4 5 6 7 8 9 A B C D E F
            U+258X ▀ ▁ ▂ ▃ ▄ ▅ ▆ ▇ █ ▉ ▊ ▋ ▌ ▍ ▎ ▏
            U+259X ▐ ░ ▒ ▓ ▔ ▕ ▖ ▗ ▘ ▙ ▚ ▛ ▜ ▝ ▞ ▟

        These are organized by their block, and order of appearance in the providers used to declare them.

        If :data:`mcfonts.colors.USE_COLORS` is True, a red or green color will be used to indicate if the character
        exists. If False, `no_glyph_char` will be displayed if the character does not exist.

        .. important:: If a character is Private Use, it will not be shown.

        :param show_offsets:
            If True, show the individual offsets for each character in a table-like format.
            If False, don't show offsets.
        :param no_glyph_char:
            The character to display when a font has no glyph for a character in a table.
            Default is '▯'.
        """
        for block in self.blocks:
            if PRIVATE_USE_PREFIX in block:
                # Skip PUA blocks
                continue
            info = tinyunicodeblock.BLOCKS_BYNAME.get(block, ("\0", "\0", 0))
            start = ord(info[0])
            end = ord(info[1])

            print(f"\n\t▼ {block} (U+{start:04X}-U+{end:04X}) ▼")
            if show_offsets:
                print("0 1 2 3 4 5 6 7 8 9 A B C D E F".rjust(len(f"{end:04X}") + 34))

            for row in range((end - start + 1) // 16):
                row_offset = start + (row * 16)
                if show_offsets:
                    print(f"U+{row_offset // 16:04X}X", end=" ")
                for codepoint in range(row_offset, row_offset + 16):
                    if (character := chr(codepoint)) in self.chars:
                        if mcfonts.utils.colors.USE_COLORS:
                            print(
                                f"{mcfonts.utils.colors.GREEN_FORE}{character}{mcfonts.utils.colors.RESET_FORE}",
                                end=" ",
                            )
                        else:
                            print(character, end=" ")
                    else:
                        if unicodedata.name(character, False) and mcfonts.utils.colors.USE_COLORS:
                            print(
                                f"{mcfonts.utils.colors.RED_FORE}{character}{mcfonts.utils.colors.RESET_FORE}", end=" "
                            )
                        else:
                            print(no_glyph_char, end=" ")
                print("")

    def block_summary(self, show_empty_blocks: bool = False) -> None:
        """
        Print a padded list of every block in the font, and their completion status.

            0000-007F     Basic Latin          Complete
            0080-00FF     Latin-1 Supplement   Partial

        And, if `show_empty_blocks` is True:

            0600-06FF     Arabic               None

        :param show_empty_blocks:
            If True, blocks with no support will be shown.
            If False, blocks with no support will be omitted.
        """
        block_name_length = 1
        # Have to know in advance the padding for block names
        for block_name in tinyunicodeblock.BLOCKS_BYNAME | tinyunicodeblock.CSUR_BYNAME:
            if block_name in self.blocks and (len_block := len(block_name)) > block_name_length:
                block_name_length = len_block
        for block, info in tinyunicodeblock.BLOCKS_BYNAME.items():
            # Use BLOCKS_BYNAME to support empty blocks.
            new_block = block
            if not show_empty_blocks and new_block not in self.blocks:
                continue
            if new_block in tinyunicodeblock.CSUR_BYNAME and mcfonts.utils.colors.USE_COLORS:
                new_block = f"{mcfonts.utils.colors.MAGENTA_BACK}{mcfonts.utils.colors.BLACK_FORE}{new_block}"
            start = ord(info[0])
            end = ord(info[1])
            block_range = f"{start:04X}-{end:04X}".ljust(13)
            amount = self.blocks.get(new_block, 0)
            if amount >= (end - start - info[2] + 1):
                completion = (
                    f"{mcfonts.utils.colors.GREEN_BACK}{mcfonts.utils.colors.BLACK_FORE}Complete"
                    if mcfonts.utils.colors.USE_COLORS
                    else "Complete"
                )
            elif amount > 0:
                completion = (
                    f"{mcfonts.utils.colors.YELLOW_BACK}{mcfonts.utils.colors.BLACK_FORE}Partial"
                    if mcfonts.utils.colors.USE_COLORS
                    else "Partial"
                )
            else:
                completion = (
                    f"{mcfonts.utils.colors.RED_BACK}{mcfonts.utils.colors.BLACK_FORE}None"
                    if mcfonts.utils.colors.USE_COLORS
                    else "None"
                )
            if mcfonts.utils.colors.USE_COLORS:
                print(
                    f"{block_range} {new_block.ljust(block_name_length + 1)} "
                    f"{completion}{mcfonts.utils.colors.RESET_BACK}{mcfonts.utils.colors.RESET_FORE}"
                )
            else:
                print(f"{block_range} {new_block.ljust(block_name_length + 1)} {completion}")
