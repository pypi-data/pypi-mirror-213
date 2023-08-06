#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
**mcfonts** is a versatile, fast, and extensible package for working with Minecraft fonts.

mcfonts works with any valid font JSON and can export every kind of texture and sizing.

| For more information, see `<https://gitlab.com/whoatemybutter/mcfonts/>`_.
| Read the documentation online at `<https://mcfonts.rtfd.io>`_.

----

| Licensed under the MIT license, see https://choosealicense.com/licenses/mit/ for details.
| Formatted with Black, see https://github.com/psf/black.
| Checked with Pylint, see https://pylint.org/.
"""
from __future__ import annotations

import collections.abc
import io
import json
import logging
import math
import os
import os.path
import shutil
import sys
import tempfile
import typing
import warnings
import zipfile

import PIL.Image
import fontTools.ttLib.ttFont
import lxml.etree
import tinyunicodeblock
import unirange

import mcfonts.compacting
import mcfonts.constants
import mcfonts.coverage_reports
import mcfonts.exceptions
import mcfonts.filters
import mcfonts.glyphs
import mcfonts.providers.base
import mcfonts.providers.bitmap
import mcfonts.providers.options
import mcfonts.providers.reference
import mcfonts.providers.space
import mcfonts.providers.unihex
import mcfonts.providers.utils
import mcfonts.utils.colors
import mcfonts.utils.exporting
import mcfonts.utils.resources

__author__ = "WhoAteMyButter"
__version__ = (0, 6)
__license__ = "MIT"

if sys.version_info < (3, 11, 0):
    raise RuntimeError(f"minimum Python version is 3.11.0, you are running {sys.version.split(' ', 1)[0]}")

# Decompression bombs will error, as they should
warnings.simplefilter("error", PIL.Image.DecompressionBombWarning)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(relativeCreated)d] [%(name)s/%(levelname)s]: (at %(funcName)s()) %(message)s",
)


class MinecraftFont:
    """
    The MinecraftFont class.

    Requires the providers of a provider file, and the associated resources mapping.

    You should never instantiate this class directly.
    Use :mod:`mcfonts.importing`.

    If you need to add, modify, or remove providers, do it through :attr:`self.providers`;
    it's a list of Provider classes, each containing relevant fields and methods.

    Be sure to run :meth:`mcfonts.MinecraftFont.validate` after making any changes;
    it won't be done automatically.

    .. warning::
        If more than one :class:`mcfonts.providers.OptionsProvider` is present in `provider_list`,
        only the **last** one will be used.

    :param provider_list:
        A list of providers, all which are instances of :data:`mcfonts.providers.utils.AnyProvider`.
    :param is_monochrome:
        Whether font resources are loaded in grayscale or not.
        Default is True.
    """

    def __init__(
        self,
        provider_list: list[mcfonts.providers.utils.AnyProvider | mcfonts.providers.options.OptionsProvider],
        is_monochrome: bool = True,
    ):
        self.providers: list[mcfonts.providers.utils.AnyProvider] = []
        """
        A list of all the providers, not including OptionsProvider.
        Do not iterate over this! Use :meth:`yield_providers` instead.
        """
        self.options: mcfonts.providers.options.OptionsProvider | None = None
        for provider in provider_list:
            if isinstance(provider, mcfonts.providers.options.OptionsProvider):
                self.options = provider
            else:
                self.providers.append(provider)
        self.is_monochrome: bool = is_monochrome

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.providers + [self.options]}, {self.is_monochrome})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __hash__(self) -> int:
        return hash((self.providers, self.is_monochrome, self.options))

    def __add__(self, other: typing.Self) -> typing.Self:
        new_providers: list[
            mcfonts.providers.utils.AnyProvider | mcfonts.providers.options.OptionsProvider
        ] = self.providers
        if self.options:
            new_providers.append(self.options)
        return MinecraftFont(new_providers, self.is_monochrome) + other

    def __iadd__(self, other: typing.Self) -> typing.Self:
        self.providers += other.providers
        if other.is_monochrome is False:
            self.is_monochrome = False
        self.validate()
        return self

    def __len__(self) -> int:
        return len(list(self.yield_characters()))

    def export(
        self,
        font_name: str,
        filter_instance: mcfonts.filters.Filter | None = None,
        include_credits: bool = True,
    ) -> fontTools.ttLib.TTFont:
        """
        Export the Minecraft font into an OpenType font with Type 2 Charstring outlines.

        The font is crafted through a TTX file (font XML), and characters are added in tables and
        given self-descriptive name mappings: ``("u0954", "u1fae4", "u2605")``.

        For some fields, the font's name will be "Minecraft <font name>".

        The font mustn't contain over 65,535 characters, or else any additional characters
        won't be added, and the font will be saved prematurely.

        :param font_name:
            The name of the resulting font, not what its filename is.
            This will be passed to: :func:`mcfonts.utils.sanitize_font_name`.
        :param filter_instance:
            An optional instance of :class:`mcfonts.filters.Filter`.
            If supplied, filter rules will be obeyed.
        :param include_credits:
            To include basic copyright information and credits in the font file.
        """
        font_xml = lxml.etree.XML(mcfonts.utils.exporting.XML_FONT_TEMPLATE)
        characters: set[str] = set()
        num_providers = 0
        # Set the space character pre-emptively
        mcfonts.utils.exporting.set_space_to_char(font_xml, " ", 4)
        for provider in self.yield_providers():
            if (
                filter_instance
                and filter_instance.should_ignore_provider(provider.__class__)
                == mcfonts.filters.FilterResult.SKIP_PROVIDER
            ):
                logger.info(f"Skipping provider {num_providers + 1:,} {provider.pretty_print()} (filtered)")
                continue
            logger.info(f"Working on provider {num_providers + 1:,} {provider.pretty_print()}")
            try:
                for character, glyph in provider.yield_glyphs():
                    if self.options:
                        glyph.export_to_character(
                            font_xml, character, characters, self.options.get_options_for_char(character)
                        )
                    else:
                        glyph.export_to_character(font_xml, character, characters)
                    characters.add(character)
                num_providers += 1
            except mcfonts.exceptions.GlyphLimitError:
                logger.warning("Font has too many characters (over 65,535), truncating and saving immediately.")
                break
        mcfonts.utils.exporting.set_font_name(font_xml, font_name, include_credits)
        mcfonts.utils.exporting.set_ulunicoderange(font_xml, characters)
        logger.info("Compiling...")
        font = fontTools.ttLib.ttFont.TTFont(recalcTimestamp=False, recalcBBoxes=False, sfntVersion="OTTO")
        font.importXML(io.StringIO(lxml.etree.tostring(font_xml, encoding=str)))
        logger.info(f"Exported {len(characters):,} characters from {num_providers:,} provider(s).")
        return font

    def yield_providers(
        self, unwind_reference_children: bool = True
    ) -> collections.abc.Iterable[
        mcfonts.providers.utils.AnyProvider | mcfonts.providers.reference.AnyProviderNotReference
    ]:
        """
        Yield the providers in this font.

        By default, this will unpack reference providers and yield its children instead.
        Reference providers will never yield the same referenced font twice if `unwind_reference_children` is True.

        :param unwind_reference_children:
            Whether to yield a reference provider's children instead of the reference provider plainly.
            Usually, this is a good idea.
            This also prevents the same font from being yielded twice.
        :returns: A yield of AnyProvider, or AnyProviderNotReference if not `unwind_reference_children`.
        """
        referenced_providers: list[str] = []
        for provider in self.providers:
            if isinstance(provider, mcfonts.providers.reference.ReferenceProvider) and unwind_reference_children:
                # Reference providers require no duplication, so store each font ID and check it.
                if (referenced := provider.contents["id"]) in referenced_providers:
                    # It's already been yielded, ignore it now.
                    continue
                # Not yielded yet.
                referenced_providers.append(referenced)
                yield from provider.yield_children()
            else:
                yield provider

    def yield_characters(self) -> collections.abc.Iterable[str]:
        """
        Yield all the characters this font covers and has a definition for.

        .. note:: Any character in :const:`mcfonts.constants.PADDING_CHARS` isn't counted.

        :returns: A yield of strings of individual characters.
        """
        provider: mcfonts.providers.utils.AnyProvider
        for provider in self.yield_providers():
            yield from provider.yield_characters()

    def save(self, indent: int | str | None = "\t") -> None:
        """
        Recursively write all providers to their original file locations.

        This is different from exporting.
        The file is indented by default.

        .. warning:: Not to be confused with :func:`export()`.

        .. warning:: Doesn't save resources.

        :param indent:
            The indentation level, refer to :func:`json.dump()` for possible values.
        """
        origin_cache: dict[str, list[dict]] = {}
        providers = []
        for wound_provider in self.yield_providers(False):
            if isinstance(wound_provider, mcfonts.providers.reference.ReferenceProvider):
                providers.extend(wound_provider.yield_children())
            providers.append(wound_provider)
        if self.options:
            providers.append(self.options)

        for provider in providers:
            if (origin_str := str(provider.origin)) not in origin_cache:
                origin_cache[origin_str] = []
            origin_cache[origin_str].append(provider.contents)

        for path, contents in origin_cache.items():
            with open(path, "w+", encoding="utf-8") as open_path:
                json.dump({"providers": contents}, open_path, ensure_ascii=False, indent=indent)

    def count_providers(self) -> dict[str, int]:
        """
        Return a counted summary of the providers this font contains.

        This is future-proof, and will work with any provider as long as it has a "type" key.

        :returns: A summary of font's providers.
        """
        result = {}
        for provider in self.yield_providers():
            if (provider_type := provider.provider_type) not in result:
                result[provider_type] = 1
            else:
                result[provider_type] += 1
        return result

    def count_providers_total(self) -> int:
        """
        Count the number of providers in the font.

        :returns: Number of providers.
        """
        return len(self.count_providers())

    def print_info(self, table_chars: bool = True, summary_only: bool = False) -> None:
        """
        Print basic information about the font.

        :param table_chars:
            Whether to print a 'chars' list as a square table, or as a simple string.
            This only applies to :class:`mcfonts.providers.BitmapProvider`.
        :param summary_only:
            If True, will only print the number of characters and providers.
        """
        if not summary_only:
            for provider in self.yield_providers():
                if isinstance(provider, mcfonts.providers.bitmap.BitmapProvider):
                    provider.print_info(table_chars)
                else:
                    provider.print_info()
            print("\n")
        print(f"Characters: {len(list(self.yield_characters())):,}")
        print(f"Providers: {self.count_providers_total():,}")

    def validate(self) -> None:
        """Run basic structure checks on the providers of the font JSON."""
        if len(self.providers) < 1:
            logger.warning("There are no providers.")
        for provider in self.yield_providers():
            if isinstance(provider, mcfonts.providers.base.BaseProvider):
                provider.validate()
            else:
                raise mcfonts.exceptions.ProviderError(
                    mcfonts.providers.utils.format_provider_message(provider, "is not a valid provider.")
                )

    def compact(
        self,
        chars_in_row: int = 0,
        cell_size: tuple[int, int] = (0, 0),
        square_cells: bool = True,
        output_file: str | None = None,
    ) -> tuple[list[str], PIL.Image.Image, tuple[int, int]]:
        """
        Take all "bitmap" providers and export every character sheet into a single sheet.

        Characters are scaled according to the largest effective bounding box in all providers.

        :param chars_in_row:
            How many characters to fit inside each row of the resulting sheet.
            If this is 0, this will be set to the length of the first string in the
            "charlist" list. If this is negative, this will be set so that the resulting sheet is
            square. By default, this is 0 (auto first string).
        :param cell_size:
            What size to make each glyph cell.
            If this is (0, 0),
            this will be set to the largest dimensions of every glyph in `glyphs`.
            If this is any other tuple of numbers, TODO actually finish this
        :param square_cells:
            If True, each glyph's width will equal its height.
            This is based on whichever number is largest.
            If False, each glyph's width will be unrelated to its height.
        :param output_file: Where to write the sheet to. If this is None, nothing will be
            written.
        :returns: A list of the new characters, and the new file as a :class:`PIL.Image.Image`.
        """
        extracted: dict[str, mcfonts.glyphs.BitmapGlyph | mcfonts.glyphs.UnihexGlyph] = {}
        provider: mcfonts.providers.utils.AnyProvider
        for provider in self.yield_providers():
            if isinstance(provider, (mcfonts.providers.bitmap.BitmapProvider, mcfonts.providers.unihex.UnihexProvider)):
                extracted.update(dict(provider.yield_glyphs()))

        if chars_in_row == 0:
            chars_in_row = max(
                len(provider.contents["chars"][0] or "")
                for provider in self.yield_providers()
                if isinstance(provider, mcfonts.providers.bitmap.BitmapProvider)
            )
        elif chars_in_row < 0:
            chars_in_row = math.ceil(math.sqrt(len(extracted)))

        compacted = mcfonts.compacting.compact_glyphs(list(extracted.values()), chars_in_row, cell_size, square_cells)
        sheet = (
            list(mcfonts.providers.bitmap.fit_chars_into_charlist(list(extracted.keys()), chars_in_row)),
            compacted[0],
            compacted[1],
        )
        if output_file:
            with open(mcfonts.utils.resources.expand_path(output_file), "wb") as open_output_file:
                sheet[1].save(open_output_file)
        return sheet

    def coverage_report(self) -> mcfonts.coverage_reports.CoverageReport:
        """
        Build a report of what characters this font contains.

        This includes information like how many characters are in the font,
        and what Unicode blocks are covered.

        :returns: A dictionary of ``{"chars": int, "blocks": {str: int}}``.
        """
        chars: list[str] = []
        blocks: dict[str, int] = {}
        for char in self.yield_characters():
            chars.append(char)
            if (block := tinyunicodeblock.block(char, include_csur=True)) in blocks:
                blocks[block] += 1
            else:
                blocks[block] = 1
        return mcfonts.coverage_reports.CoverageReport(set(chars), blocks)

    def get_glyphs_in_unirange(self, unirange_notation: str) -> dict[str, mcfonts.glyphs.BitmapGlyph]:
        """
        Given a `unirange_notation`, return a dictionary of the requested chars to their glyphs.

        :param unirange_notation:
            A string representing the requested range of chars.
            See https://pypi.org/project/unirange/.
        :returns: A list of the requested glyphs that match `unirange_notation`.
        """
        ranged_glyphs: dict[str, mcfonts.glyphs.BitmapGlyph] = {}
        for provider in self.yield_providers():
            if isinstance(provider, mcfonts.providers.bitmap.BitmapProvider):
                if (ranged := provider.get_glyphs_in_unirange(unirange_notation)) is not None:
                    ranged_glyphs |= dict(ranged)
        return ranged_glyphs

    def get_covering_providers(self, unirange_notation: str) -> list[mcfonts.providers.utils.AnyProvider]:
        """
        Given a codepoint range, return a list of providers that cover these characters.

        :param unirange_notation:
            A string representing the requested range of chars.
            See https://pypi.org/project/unirange/.
        :returns: A list of the providers that cover codeopints defined in `unirange_notation`.
        """
        result = []
        covers = unirange.unirange_to_characters(unirange_notation)
        for provider in self.yield_providers():
            if not isinstance(provider, mcfonts.providers.space.SpaceProvider):
                # Ignore padding chars
                covers.difference_update(mcfonts.constants.PADDING_CHARS)
            if provider.chars_covered.intersection(covers):
                result.append(provider)
        return result

    def reload_to_monochrome(self) -> None:
        """
        Replace the resources used in the providers with a grayscale version.

        If the resource is already grayscale, this will have no effect.
        This modifies the resource of this provider in place, and **can't be undone**.
        """
        if self.is_monochrome:
            mcfonts.logger.info("Font is already in monochrome; can't reload")
            return
        for provider in self.yield_providers():
            if isinstance(provider, mcfonts.providers.bitmap.BitmapProvider):
                provider.reload_to_monochrome()
        self.is_monochrome = True

    def compare(self, other: typing.Self):
        """
        Given `other`, compare the two, using `self` as a baseline.

        The information compared is:

        * Character count
        * Blocks covered
        * Providers included

        :param other: A second instance of :class:`mcfonts.MinecraftFont` to compare to.
        """
        self.coverage_report().compare(other.coverage_report())
        if mcfonts.utils.colors.USE_COLORS:
            print(f"\n{mcfonts.utils.colors.BRIGHT}PROVIDERS{mcfonts.utils.colors.RESET_ALL}")
        else:
            print("\nPROVIDERS")
        print(":: type: this | other (delta)")
        providers_this = {"bitmap": 0, "space": 0, "ttf": 0, "legacy_unicode": 0}
        providers_other = providers_this.copy()
        for provider in self.yield_providers():
            providers_this[provider.provider_type] += 1
        for provider in other.yield_providers():
            providers_other[provider.provider_type] += 1
        for provider_type in ("bitmap", "space", "ttf", "legacy_unicode"):
            amount_this = providers_this[provider_type]
            amount_other = providers_other[provider_type]
            print(
                f"\t{provider_type}: "
                f"{amount_this} | {amount_other} "
                f"({mcfonts.utils.colors.color_number(amount_other - amount_this)})"
            )

    def regenerate_charlists(self) -> dict:
        """
        Iterate through each resource and analyse it.

        For each resource, an entry will be made in a dictionary that contains the same height and ascent fields as
        the original, except the "chars" list will be updated to reflect the glyphs in the associated resource.

        .. warning::
            This only works if the first character in the original charlist is present,
            **and** if the order is incremental (U+0100, then U+0101, then U+0102, so on).

            If this condition isn't true, this function **will** fail.
            There are **no** checks for this rule.

        :returns: A dictionary matching a normal font JSON, with each "chars" list updated.
        """
        result: dict[str, list] = {"providers": []}
        if self.options:
            result["providers"].append(self.options.contents)
        for provider in self.yield_providers():
            if isinstance(provider, mcfonts.providers.bitmap.BitmapProvider) and provider.resource:
                old_contents = provider.contents
                old_contents["chars"] = mcfonts.providers.bitmap.resource_to_charlist(
                    provider.resource,
                    chr(int(os.path.basename(provider.contents["file"]).split("-", 1)[0].split(".", 1)[0], 16)),
                    provider.glyph_cell,
                )
                result["providers"].append(old_contents)
            else:
                result["providers"].append(provider.contents)
        return result


def from_java_font_file(
    file_path: str,
    read_colors: bool = False,
    strict: bool = True,
) -> mcfonts.MinecraftFont:
    """
    Load a Java Edition font JSON into a :class:`mcfonts.MinecraftFont`.

    Requires a "providers" list, and missing files will raise an error.

    :param file_path:
        The file path to the font JSON.
    :param read_colors:
        If True, glyph will be loaded in RGBA. If false, loaded in LA.
        RGBA images incur **heavy** time cost. Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error.
        * Missing files will raise an error.

        If False:

        * Bad providers will be ignored.
        * Missing files will be skipped.
    :returns: A :class:`mcfonts.MinecraftFont` instance.
    :raises FileNotFoundError: If a referenced file is not found and `strict` is True.
    """
    with open(file_path, encoding="utf-8") as datafp:
        file_contents: dict = json.load(datafp, strict=False)
    return from_java_font_contents(file_contents, file_path, read_colors, strict)


def from_java_font_contents(
    file_contents: dict,
    file_path: str,
    read_colors: bool = False,
    strict: bool = True,
) -> mcfonts.MinecraftFont:
    """
    Load a Java Edition font JSON into a :class:`mcfonts.MinecraftFont`.

    Requires a "providers" list, and missing files will raise an error.

    :param file_contents:
        The contents of the font JSON file, loaded as a dictionary.
        This dictionary should include the base "providers" key.
    :param file_path:
        The path to the font JSON.
        This is needed for loading resources.
    :param read_colors:
        If True, glyph will be loaded in RGBA (Red, Green, Blue, Alpha). If false, loaded in LA.
        RGBA images incur **heavy** time cost. Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error.
        * Missing files will raise an error.
        If False:

        * Bad providers will be ignored.
        * Missing files will be skipped.
    :returns: A :class:`mcfonts.MinecraftFont` instance.
    :raises FileNotFoundError: If a referenced file isn't found and `strict` is True.
    """
    provider_content = file_contents.get("providers", [])
    if read_colors:
        mode = "RGBA"
    else:
        mode = "LA"
    return mcfonts.MinecraftFont(
        list(
            mcfonts.providers.utils.load_all(
                provider_content, mcfonts.utils.resources.expand_path(file_path), strict, mode
            )
        ),
        not read_colors,
    )


def from_java_pack_folder(
    folder_path: str,
    font_file_name: str = "default.json",
    namespace: str = "minecraft",
    read_colors: bool = False,
    strict: bool = True,
) -> mcfonts.MinecraftFont:
    """
    Load a Java Edition resource pack into a :class:`mcfonts.MinecraftFont`.

    The font must be in the path ``assets/<namespace>/font/<fontfile>``.

    :param folder_path:
        The path to the folder that contains a resource pack.
        This is not the ``assets`` folder, nor is it a ZIP file.
        The files inside this folder should be ``assets/``, and ``pack.mcmeta``.
    :param font_file_name:
        The name of the font file.
        By default, this is "default.json".
    :param namespace:
        The namespace to find assets in.
        By default, this is "minecraft".
    :param read_colors:
        If True, glyph will be loaded in 'RGBA'.
        If False, loaded in 'LA'.
        RGBA images incur **heavy** time cost. Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error.
        * Missing files will raise an error.

        If False:

        * Bad providers will be ignored.
        * Missing files will be skipped.
    :returns: A :class:`mcfonts.MinecraftFont` instance.
    :raises FileNotFoundError: If a referenced file isn't found and `strict` is True.
    """
    return from_java_font_file(
        os.path.join(
            mcfonts.utils.resources.expand_path(folder_path),
            f"assets/{namespace}/font/{font_file_name}",
        ),
        read_colors,
        strict,
    )


def from_java_pack_zip(
    file_path: str, password: bytes | None = None, read_colors: bool = False, strict: bool = True
) -> mcfonts.MinecraftFont:
    """
    Load a Java Edition resource pack ZIP into a :class:`mcfonts.MinecraftFont`.

    The font must be in the path ``assets/<namespace>/font/<fontfile>``.

    :param file_path:
        The path to the ZIP file.
    :param password:
        Password to use when reading the ZIP file.
        Set to ``None`` if there is no password.
    :param read_colors:
        If True, glyph will be loaded in 'RGBA'.
        If False, loaded in 'LA'.
        RGBA images incur **heavy** time cost. Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error.
        * Missing files will raise an error.

        If False:

        * Bad providers will be ignored.
        * Missing files will be skipped.

    :returns: A :class:`mcfonts.MinecraftFont` instance.
    :raises FileNotFoundError: If a referenced file isn't found and `strict` is True.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(mcfonts.utils.resources.expand_path(file_path)) as zip_file:
            zip_file.extractall(temp_dir, pwd=password)
        return from_java_pack_folder(temp_dir, read_colors=read_colors, strict=strict)


def from_java_resource_template(
    file_path: str,
    template_provider: dict | None = None,
    read_colors: bool = False,
    strict: bool = True,
) -> mcfonts.MinecraftFont:
    """
    | Given the path to a texture and the contents of an individual font provider,
    | return a :class:`mcfonts.MinecraftFont` instance with it, and the resource in `file_path`.

    ``template_provider["file"]`` can be any value, it will be overwritten anyway,
    although it must exist.

    :param file_path:
        The path to the PNG :term:`resource` that needs templating.
    :param template_provider:
        An individual provider dictionary.
        Not a list of providers.
        By default, this is :const:`mcfonts.utils.templates.PROVIDER_ASCII`.
    :param read_colors:
        If True, glyph will be loaded in 'RGBA'.
        If False, loaded in 'LA'.
        RGBA images incur **heavy** time cost. Be careful.
    :param strict:
        If a provider has bad data,
        an exception will be raised and no provider list will be returned if this is True.
        If this is False, it will be ignored.
    :returns:
        A :class:`mcfonts.MinecraftFont` instance.
    """
    if template_provider is None:
        template_provider = mcfonts.constants.PROVIDER_ASCII
    # Make a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Put the PNG file into the temp dir to later read all-together.
        shutil.copy(file_path := mcfonts.utils.resources.expand_path(file_path), temp_dir)
        # Make a temporary fake provider file
        with tempfile.NamedTemporaryFile("w+", dir=temp_dir) as temp_file:
            # Overwrite default file, use expanded argument with modifications
            try:
                template_provider["file"] = mcfonts.utils.resources.expand_resource_location(file_path)
            except KeyError as exception:
                if strict:
                    raise exception
            json.dump(template_provider, temp_file, ensure_ascii=False)
        return from_java_font_file(temp_file.name, read_colors, strict)


def from_java_ambiguous(path: str, read_colors: bool = False, strict: bool = True) -> mcfonts.MinecraftFont:
    """
    For file paths where the file pointed to is of an unknown type; it could be a JSON, ZIP, or directory.

    This function automatically figures out which function to use, and returns a MinecraftFont.

    :param path:
        The path to either a file or a folder.
    :param read_colors:
        If True, glyph will be loaded in 'RGBA'.
        If False, loaded in 'LA'.
        RGBA images incur **heavy** time cost. Be careful.
    :param strict:
        If True:

        * Bad providers will raise an error.
        * Missing files will raise an error.

        If False:

        * Bad providers will be ignored.
        * Missing files will be skipped.

    :returns: A :class:`mcfonts.MinecraftFont` instance.
    """
    if path.endswith(".json"):
        return from_java_font_file(path, read_colors, strict)
    if os.path.isdir(path):
        return from_java_pack_folder(path, read_colors=read_colors, strict=strict)
    # Not a JSON, not a directory, must be a ZIP.
    return from_java_pack_zip(path, read_colors=read_colors, strict=strict)
