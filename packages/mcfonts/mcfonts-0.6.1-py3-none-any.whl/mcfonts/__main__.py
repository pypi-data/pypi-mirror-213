#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""Command-line tool front-end for mcfonts."""
from __future__ import annotations

import argparse
import sys

import PIL.Image

import mcfonts.utils.resources
import mcfonts.compacting

if __name__ == "__main__":

    INPUT_HELP = (
        "Path to folder, JSON, or ZIP file of font. "
        "If folder, this folder must be a resource pack. "
        "If JSON, this file must be a font JSON file. "
        "If ZIP, this file must be a resource pack archive. "
        "If -, stdin is used."
    )

    parser = argparse.ArgumentParser(
        description="""
        mcfonts is a versatile, fast, and extensible package for working with Minecraft fonts.
        
        The CLI front-end does not expose every possible option.
        For more in-depth usage, import the mcfonts module in Python.
        """
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="mcfonts " + ".".join(str(x) for x in mcfonts.__version__),
    )

    subparsers = parser.add_subparsers(title="Functions")

    export_parser = subparsers.add_parser("export", help="export a font file to an OpenType font")
    export_parser.add_argument(
        "input",
        type=argparse.FileType(),
        default=(None if sys.stdin.isatty() else sys.stdin),
        help=INPUT_HELP,
    )
    export_parser.add_argument("outfile", type=argparse.FileType("wb"), default=sys.stdout)
    export_parser.add_argument(
        "-c",
        "--color",
        default=False,
        action="store_true",
        help="To read colors in referenced resources",
    )
    export_parser.add_argument("-n", "--font-name", help="What the font name of the output should be")
    export_parser.set_defaults(export=True)

    info_parser = subparsers.add_parser("info", help="print information about a font file")
    info_parser.add_argument(
        "input",
        type=argparse.FileType(),
        default=(None if sys.stdin.isatty() else sys.stdin),
        help=INPUT_HELP,
    )

    info_parser.add_argument(
        "-t",
        "--table-chars",
        action="store_true",
        default=False,
        help="to put characters into a formatter table or put in single list",
    )
    info_parser.add_argument(
        "-s",
        "--summary-only",
        action="store_true",
        default=False,
        help="to print only a small summary",
    )
    info_parser.set_defaults(info=True)

    compact_parser = subparsers.add_parser("compact", help="fit the glyphs in the minimum amount of space needed")
    compact_parser.add_argument(
        "input",
        type=argparse.FileType("rb"),
        default=(None if sys.stdin.isatty() else sys.stdin),
        help="Path to PNG file.",
    )
    compact_parser.add_argument(
        "char-counts",
        nargs=2,
        type=int,
        default=(16, 16),
        help="Two numbers of the characters in each row and column of the input file.",
    )
    compact_parser.add_argument(
        "-c",
        "--chars-in-row",
        type=int,
        default=16,
        help="The desired number of glyphs to put in one row, set to 0 for square. Default is 16.",
    )
    compact_parser.add_argument("outfile", type=argparse.FileType("wb"), default=sys.stdout)
    compact_parser.set_defaults(compact=True)

    compare_parser = subparsers.add_parser("compare", help="compare two fonts")
    compare_parser.add_argument(
        "input1",
        type=argparse.FileType("rb"),
        default=(None if sys.stdin.isatty() else sys.stdin),
        help=INPUT_HELP,
    )
    compare_parser.add_argument(
        "input2",
        type=argparse.FileType("rb"),
        default=(None if sys.stdin.isatty() else sys.stdin),
        help=INPUT_HELP,
    )
    compare_parser.add_argument(
        "-s",
        "--swap",
        action="store_true",
        default=(None if sys.stdin.isatty() else sys.stdin),
        help="swap the order of fonts compared",
    )
    compare_parser.set_defaults(compare=True)

    vargs = vars(parser.parse_args(args=None if sys.argv[1:] else ["--help"]))

    if vargs.get("export", False):
        mcfonts.from_java_font_file(vargs["input"].name, vargs["color"]).export(vargs["font_name"]).save(
            vargs["outfile"], False
        )
    elif vargs.get("info", False):
        mcfonts.from_java_ambiguous(vargs["input"].name).print_info(
            vargs.get("table_chars", False), vargs.get("summary_only", False)
        )
    elif vargs.get("compact"):
        resource = PIL.Image.open(vargs["input"])
        cell_size = tuple(vargs["char_counts"])
        compacted = mcfonts.compacting.compact_images(
            list(mcfonts.utils.resources.divide_resource_by_grid(resource, cell_size)),
            vargs["chars_in_row"](resource.width // cell_size[0], resource.height // cell_size[1]),
        )
        compacted[0].save(vargs["outfile"])
        print(compacted[1])
    elif vargs.get("compare"):
        font1 = mcfonts.from_java_ambiguous(vargs["input1"].name)
        font2 = mcfonts.from_java_ambiguous(vargs["input2"].name)
        if vargs.get("swap", False):
            font2.compare(font1)
        else:
            font1.compare(font2)
