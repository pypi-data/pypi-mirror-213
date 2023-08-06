#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Functions for exporting various character/provider formats into XML-representable data.

Contains functions for transforming and handling font XMLs.
"""
from __future__ import annotations

import datetime
import re

import lxml.etree

import mcfonts.exceptions
import mcfonts.utils.unicode

XML_FONT_TEMPLATE: bytes = b"""<?xml version="1.0" encoding="UTF-8"?>
<ttFont sfntVersion="OTTO" ttLibVersion="4.34">
    <GlyphOrder>
        <GlyphID id="0" name=".notdef"/>
    </GlyphOrder>
    <head>
        <tableVersion value="1.0"/>
        <fontRevision value="1.0"/>
        <checkSumAdjustment value="0x910274da"/>
        <magicNumber value="0x5f0f3cf5"/>
        <flags value="00000000 00001011"/>
        <unitsPerEm value="1000"/>
        <created value="Mon Jan  1 00:00:00 0000"/>
        <modified value="Mon Jan  1 00:00:00 0000"/>
        <xMin value="-12500"/>
        <yMin value="-12500"/>
        <xMax value="12500"/>
        <yMax value="12500"/>
        <macStyle value="00000000 00000000"/>
        <lowestRecPPEM value="8"/>
        <fontDirectionHint value="2"/>
        <indexToLocFormat value="0"/>
        <glyphDataFormat value="0"/>
    </head>
    <hhea>
        <tableVersion value="0x00010000"/>
        <ascent value="1250"/>
        <descent value="-250"/>
        <lineGap value="250"/>
        <advanceWidthMax value="12500"/>
        <minLeftSideBearing value="0"/>
        <minRightSideBearing value="0"/>
        <xMaxExtent value="1125"/>
        <caretSlopeRise value="1"/>
        <caretSlopeRun value="0"/>
        <caretOffset value="0"/>
        <reserved0 value="0"/>
        <reserved1 value="0"/>
        <reserved2 value="0"/>
        <reserved3 value="0"/>
        <metricDataFormat value="0"/>
        <numberOfHMetrics value="1"/>
    </hhea>
    <maxp>
        <tableVersion value="0x5000"/>
        <numGlyphs value="0"/>
    </maxp>
    <OS_2>
        <!-- The fields 'usFirstCharIndex' and 'usLastCharIndex' will be recalculated by the compiler -->
        <version value="5"/>
        <xAvgCharWidth value="660"/>
        <usWeightClass value="400"/>
        <usWidthClass value="5"/>
        <fsType value="00000000 00000000"/>
        <ySubscriptXSize value="650"/>
        <ySubscriptYSize value="700"/>
        <ySubscriptXOffset value="0"/>
        <ySubscriptYOffset value="140"/>
        <ySuperscriptXSize value="650"/>
        <ySuperscriptYSize value="700"/>
        <ySuperscriptXOffset value="0"/>
        <ySuperscriptYOffset value="480"/>
        <yStrikeoutSize value="50"/>
        <yStrikeoutPosition value="256"/>
        <sFamilyClass value="0"/>
        <panose>
            <bFamilyType value="2"/>
            <bSerifStyle value="0"/>
            <bWeight value="5"/>
            <bProportion value="0"/>
            <bContrast value="0"/>
            <bStrokeVariation value="0"/>
            <bArmStyle value="0"/>
            <bLetterForm value="0"/>
            <bMidline value="6"/>
            <bXHeight value="6"/>
        </panose>
        <ulUnicodeRange1 value="00000000 00000000 00000000 00000000"/>
        <ulUnicodeRange2 value="00000000 00000000 00000000 00000000"/>
        <ulUnicodeRange3 value="00000000 00000000 00000000 00000000"/>
        <ulUnicodeRange4 value="00000000 00000000 00000000 00000000"/>
        <achVendID value="pMCF"/>
        <fsSelection value="00000000 00000000"/>
        <usFirstCharIndex value="32"/>
        <usLastCharIndex value="0"/>
        <sTypoAscender value="875"/>
        <sTypoDescender value="-125"/>
        <sTypoLineGap value="4"/>
        <usWinAscent value="1250"/>
        <usWinDescent value="250"/>
        <!-- This will be filled in automatically -->
        <ulCodePageRange1 value="00000000 00000000 00000000 00000000"/>
        <ulCodePageRange2 value="00000000 00000000 00000000 00000000"/>
        <sxHeight value="600"/>
        <sCapHeight value="1000"/>
        <usDefaultChar value="32"/>
        <usBreakChar value="32"/>
        <usMaxContext value="0"/>
        <usLowerOpticalPointSize value="0"/>
        <usUpperOpticalPointSize value="1"/>
    </OS_2>
    <name></name>
    <cmap>
        <tableVersion version="0"/>
    </cmap>
    <post>
        <formatType value="3.0"/>
        <italicAngle value="0.0"/>
        <underlinePosition value="0"/>
        <underlineThickness value="0"/>
        <isFixedPitch value="0"/>
        <minMemType42 value="0"/>
        <maxMemType42 value="0"/>
        <minMemType1 value="0"/>
        <maxMemType1 value="0"/>
    </post>
    <CFF>
        <major value="1"/>
        <minor value="0"/>
        <CFFFont name="Default">
            <version value="001.000"/>
            <Notice value=""/>
            <FullName value="Default"/>
            <FamilyName value="Default"/>
            <Weight value="Regular"/>
            <isFixedPitch value="0"/>
            <ItalicAngle value="0"/>
            <UnderlinePosition value="0"/>
            <UnderlineThickness value="0"/>
            <PaintType value="0"/>
            <CharstringType value="2"/>
            <FontMatrix value="0.001 0 0 0.001 0 0"/>
            <FontBBox value="0 -250 1125 1250"/>
            <StrokeWidth value="0"/>
            <!-- charset is dumped separately as the 'GlyphOrder' element -->
            <Encoding name="StandardEncoding"/>
            <Private>
                <BlueValues value="0 0 500 500 700 700"/>
                <BlueScale value="0.039625"/>
                <BlueShift value="0"/>
                <BlueFuzz value="1"/>
                <ForceBold value="0"/>
                <StdHW value="125" />
                <StdVW value="125" />
                <StemSnapH value="125 250" />
                <StemSnapV value="125 250" />
                <LanguageGroup value="0"/>
                <ExpansionFactor value="0.06"/>
                <initialRandomSeed value="0"/>
                <defaultWidthX value="750"/>
                <nominalWidthX value="900"/>
            </Private>
            <CharStrings>
                <CharString name=".notdef">
                500 hmoveto 750 -375 -750 vlineto -125 -125 rmoveto 1000 625 -1000 vlineto endchar
                </CharString>
            </CharStrings>
        </CFFFont>
        <GlobalSubrs/>
    </CFF>
    <GDEF>
        <Version value="0x00010000"/>
        <GlyphClassDef/>
    </GDEF>
    <hmtx>
        <mtx name=".notdef" width="750" lsb="0"/>
    </hmtx>
    <DSIG>
        <!-- note that the Digital Signature will be invalid after recompilation! -->
        <tableHeader flag="0x0" numSigs="0" version="1"/>
    </DSIG>
</ttFont>"""
"""
Bytes of a blank TTF XML, with a ``.notdef`` glyph already embedded.
You must call :func:`lxml.etree.XML` with this.
"""

ULUNICODERANGE_BIT_MAP: dict[tuple[int, int], int] = {
    (0x0000, 0x007F): 0,
    (0x0080, 0x00FF): 1,
    (0x0100, 0x017F): 2,
    (0x0180, 0x024F): 3,
    (0x0250, 0x02AF): 4,
    (0x1D00, 0x1D7F): 4,
    (0x1D80, 0x1DBF): 4,
    (0x02B0, 0x02FF): 5,
    (0xA700, 0xA71F): 5,
    (0x0300, 0x036F): 6,
    (0x1DC0, 0x1DFF): 6,
    (0x0370, 0x03FF): 7,
    (0x2C80, 0x2CFF): 8,
    (0x0400, 0x04FF): 9,
    (0x0500, 0x052F): 9,
    (0x2DE0, 0x2DFF): 9,
    (0xA640, 0xA69F): 9,
    (0x0530, 0x058F): 10,
    (0x0590, 0x05FF): 11,
    (0xA500, 0xA63F): 12,
    (0x0600, 0x06FF): 13,
    (0x0750, 0x077F): 13,
    (0x07C0, 0x07FF): 14,
    (0x0900, 0x097F): 15,
    (0x0980, 0x09FF): 16,
    (0x0A00, 0x0A7F): 17,
    (0x0A80, 0x0AFF): 18,
    (0x0B00, 0x0B7F): 19,
    (0x0B80, 0x0BFF): 20,
    (0x0C00, 0x0C7F): 21,
    (0x0C80, 0x0CFF): 22,
    (0x0D00, 0x0D7F): 23,
    (0x0E00, 0x0E7F): 24,
    (0x0E80, 0x0EFF): 25,
    (0x10A0, 0x10FF): 26,
    (0x2D00, 0x2D2F): 26,
    (0x1B00, 0x1B7F): 27,
    (0x1100, 0x11FF): 28,
    (0x1E00, 0x1EFF): 29,
    (0x2C60, 0x2C7F): 29,
    (0xA720, 0xA7FF): 29,
    (0x1F00, 0x1FFF): 30,
    (0x2000, 0x206F): 31,
    (0x2E00, 0x2E7F): 31,
    (0x2070, 0x209F): 32,
    (0x20A0, 0x20CF): 33,
    (0x20D0, 0x20FF): 34,
    (0x2100, 0x214F): 35,
    (0x2150, 0x218F): 36,
    (0x2190, 0x21FF): 37,
    (0x27F0, 0x27FF): 37,
    (0x2900, 0x297F): 37,
    (0x2B00, 0x2BFF): 37,
    (0x2200, 0x22FF): 38,
    (0x2A00, 0x2AFF): 38,
    (0x27C0, 0x27EF): 38,
    (0x2980, 0x29FF): 38,
    (0x2300, 0x23FF): 39,
    (0x2400, 0x243F): 40,
    (0x2440, 0x245F): 41,
    (0x2460, 0x24FF): 42,
    (0x2500, 0x257F): 43,
    (0x2580, 0x259F): 44,
    (0x25A0, 0x25FF): 45,
    (0x2600, 0x26FF): 46,
    (0x2700, 0x27BF): 47,
    (0x3000, 0x303F): 48,
    (0x3040, 0x309F): 49,
    (0x30A0, 0x30FF): 50,
    (0x31F0, 0x31FF): 50,
    (0x3100, 0x312F): 51,
    (0x31A0, 0x31BF): 51,
    (0x3130, 0x318F): 52,
    (0xA840, 0xA87F): 53,
    (0x3200, 0x32FF): 54,
    (0x3300, 0x33FF): 55,
    (0xAC00, 0xD7AF): 56,
    (0x10000, 0x10FFFF): 57,
    (0x10900, 0x1091F): 58,
    (0x4E00, 0x9FFF): 59,
    (0x2E80, 0x2EFF): 59,
    (0x2F00, 0x2FDF): 59,
    (0x2FF0, 0x2FFF): 59,
    (0x3400, 0x4DBF): 59,
    (0x20000, 0x2A6DF): 59,
    (0x3190, 0x319F): 59,
    (0xE000, 0xF8FF): 60,
    (0x31C0, 0x31EF): 61,
    (0xF900, 0xFAFF): 61,
    (0x2F800, 0x2FA1F): 61,
    (0xFB00, 0xFB4F): 62,
    (0xFB50, 0xFDFF): 63,
    (0xFE20, 0xFE2F): 64,
    (0xFE10, 0xFE1F): 65,
    (0xFE30, 0xFE4F): 65,
    (0xFE50, 0xFE6F): 66,
    (0xFE70, 0xFEFF): 67,
    (0xFF00, 0xFFEF): 68,
    (0xFFF0, 0xFFFF): 69,
    (0x0F00, 0x0FFF): 70,
    (0x0700, 0x074F): 71,
    (0x0780, 0x07BF): 72,
    (0x0D80, 0x0DFF): 73,
    (0x1000, 0x109F): 74,
    (0x1200, 0x137F): 75,
    (0x1380, 0x139F): 75,
    (0x2D80, 0x2DDF): 75,
    (0x13A0, 0x13FF): 76,
    (0x1400, 0x167F): 77,
    (0x1680, 0x169F): 78,
    (0x16A0, 0x16FF): 79,
    (0x1780, 0x17FF): 80,
    (0x19E0, 0x19FF): 80,
    (0x1800, 0x18AF): 81,
    (0x2800, 0x28FF): 82,
    (0xA000, 0xA48F): 83,
    (0xA490, 0xA4CF): 83,
    (0x1700, 0x171F): 84,
    (0x1720, 0x173F): 84,
    (0x1740, 0x175F): 84,
    (0x1760, 0x177F): 84,
    (0x10300, 0x1032F): 85,
    (0x10330, 0x1034F): 86,
    (0x10400, 0x1044F): 87,
    (0x1D000, 0x1D0FF): 88,
    (0x1D100, 0x1D1FF): 88,
    (0x1D200, 0x1D24F): 88,
    (0x1D400, 0x1D7FF): 89,
    (0xF0000, 0xFFFFD): 90,
    (0x100000, 0x10FFFD): 90,
    (0xFE00, 0xFE0F): 91,
    (0xE0100, 0xE01EF): 91,
    (0xE0000, 0xE007F): 92,
    (0x1900, 0x194F): 93,
    (0x1950, 0x197F): 94,
    (0x1980, 0x19DF): 95,
    (0x1A00, 0x1A1F): 96,
    (0x2C00, 0x2C5F): 97,
    (0x2D30, 0x2D7F): 98,
    (0x4DC0, 0x4DFF): 99,
    (0xA800, 0xA82F): 100,
    (0x10000, 0x1007F): 101,
    (0x10080, 0x100FF): 101,
    (0x10100, 0x1013F): 101,
    (0x10140, 0x1018F): 102,
    (0x10380, 0x1039F): 103,
    (0x103A0, 0x103DF): 104,
    (0x10450, 0x1047F): 105,
    (0x10480, 0x104AF): 106,
    (0x10800, 0x1083F): 107,
    (0x10A00, 0x10A5F): 108,
    (0x1D300, 0x1D35F): 109,
    (0x12000, 0x123FF): 110,
    (0x12400, 0x1247F): 110,
    (0x1D360, 0x1D37F): 111,
    (0x1B80, 0x1BBF): 112,
    (0x1C00, 0x1C4F): 113,
    (0x1C50, 0x1C7F): 114,
    (0xA880, 0xA8DF): 115,
    (0xA900, 0xA92F): 116,
    (0xA930, 0xA95F): 117,
    (0xAA00, 0xAA5F): 118,
    (0x10190, 0x101CF): 119,
    (0x101D0, 0x101FF): 120,
    (0x102A0, 0x102DF): 121,
    (0x10280, 0x1029F): 121,
    (0x10920, 0x1093F): 121,
    (0x1F030, 0x1F09F): 122,
    (0x1F000, 0x1F02F): 122,
}
"""
A mapping of (block codepoint start, block codepoint end) to ulUnicodeRange bit.
It is best to store a single 128 bit number and then split it up for processing later.
See https://learn.microsoft.com/en-us/typography/opentype/spec/os2#ur.
"""


def allocate_char(font_xml: lxml.etree._Element, char: str) -> None:
    """
    Allocate a Unicode character in a font.

    This doesn't assign any character data or widths.

    :param font_xml: The font XML.
    :param char: A single character.
    :raises mcfonts.exceptions.GlyphLimitError: If there are more than 65,535 glyphs in the font; can't add more.
    """

    if (metrics_num := int((metrics := font_xml.find("hhea/numberOfHMetrics")).get("value"))) >= 65535:
        raise mcfonts.exceptions.GlyphLimitError()
    metrics.set("value", str(metrics_num + 1))

    num_glyphs = font_xml.find("maxp/numGlyphs")
    num_glyphs.set("value", str(int(num_glyphs.get("value")) + 1))

    cmap = font_xml.find("cmap")
    codepoint = ord(char)
    uni = f"u{codepoint:04X}"
    make_cmap(
        font_xml,
        (codepoint <= 0xFFFF and (cmap.find("cmap_format_4")) is None),  # BMP
        (codepoint < 0xFFFF and (cmap.find("cmap_format_12") is None)),  # above BMP
    )
    lxml.etree.SubElement(
        cmap.find("cmap_format_12"), "map", {"code": f"0x{codepoint:X}", "name": uni, "language": "0"}
    )

    if codepoint <= 0xFFFF:
        lxml.etree.SubElement(
            cmap.find("cmap_format_4"), "map", {"code": f"0x{codepoint:X}", "name": uni, "language": "0"}
        )

    lxml.etree.SubElement(font_xml.find("GDEF/GlyphClassDef"), "ClassDef", {"glyph": uni, "class": "1"})

    lxml.etree.SubElement(font_xml.find("GlyphOrder"), "GlyphID", {"name": uni})


def make_cmap(font_xml: lxml.etree._Element, format_4: bool = True, format_12: bool = True) -> None:
    """
    Insert cmap subtables in `font_xml`. These are used for mapping glyph IDs to Unicode codepoints.

    If `format_4`, cmap_format_4 will be added. If `format_12`, cmap_format_12 will be added.

    * Format 4: https://learn.microsoft.com/en-us/typography/opentype/spec/cmap#format-4-segment-mapping-to-delta-values
    * Format 12: https://learn.microsoft.com/en-us/typography/opentype/spec/cmap#format-12-segmented-coverage

    :param font_xml: A font XML.
    :param format_4:
        Whether to insert a cmap format 4 subtable.
        See https://learn.microsoft.com/en-us/typography/opentype/spec/cmap#format-4-segment-mapping-to-delta-values.
    :param format_12:
        Whether to insert a cmap format 12 subtable.
        See https://learn.microsoft.com/en-us/typography/opentype/spec/cmap#format-12-segmented-coverage.
    """

    cmap = font_xml.find("cmap")
    if format_12 and cmap.find("cmap_format_12") is None:
        lxml.etree.SubElement(
            cmap,
            "cmap_format_12",
            {
                "platformID": "0",
                "platEncID": "4",
                "language": "0",
                "length": "4120",
                "nGroups": "323",
                "format": "12",
                "reserved": "0",
            },
        )
    if format_4 and cmap.find("cmap_format_4") is None:
        lxml.etree.SubElement(
            cmap,
            "cmap_format_4",
            {
                "platformID": "3",
                "platEncID": "4",
                "language": "0",
            },
        )


def set_program_to_char(
    font_xml: lxml.etree._Element, program: list[str | int], char: str, replace: bool = True
) -> None:
    """
    Set a program to a character.

    This is how character data is added to the font.
    The character must be allocated already; that isn't done in this function.

    If the character isn't in the font, add it.
    If it's and ``replace`` is True, set it to the new character data.
    Otherwise, do nothing.

    :param font_xml: The font XML.
    :param program: A list of strings of the glyph's program.
    :param char: A single character.
    :param replace: If the character already has data, overwrite.
    :returns: Nothing, font is modified in-place.
    :raises GlyphLimitError: If there are more than 65,535 glyphs in the font; can't add more.
    """
    uni = f"u{ord(char):04X}"
    charstrings = font_xml.find("CFF/CFFFont/CharStrings")
    charstring_xml = font_xml.find(f"{charstrings}/CharString[@name='{uni}']")
    if charstring_xml is None:
        # Doesn't exist
        lxml.etree.SubElement(charstrings, "CharString", {"name": uni}).text = " ".join(str(x) for x in program)
        lxml.etree.SubElement(font_xml.find("hmtx"), "mtx", {"name": uni, "width": str(program[0]), "lsb": "0"})
    elif replace:
        # Exists already in the charstrings, replace it too
        charstring_xml.text = " ".join(str(x) for x in program)
        font_xml.find(f"hmtx/mtx[@name='{uni}']").set("width", str(program[0]))


def set_space_to_char(font_xml: lxml.etree._Element, char: str, width: int, replace: bool = True) -> None:
    """
    Add/set a space character to the font, only defining its width.

    The character must be allocated already.
    That isn't done in this function.

    If the glyph isn't in the font, add it.
    If it's and ``replace`` is True, set it to the new value.
    Otherwise, do nothing.

    :param font_xml: The font XML.
    :param char: A single character.
    :param width: The width of the space, unscaled.
    :param replace: If the character already has data, overwrite.
    :returns: Nothing, font is modified in-place.
    :raises GlyphLimitError: If there are more than 65,535 glyphs in the font; can't add more.
    """
    uni = f"u{ord(char):04X}"
    charstrings = font_xml.find("CFF/CFFFont/CharStrings")
    width = abs(width) * 125

    if (charstring_xml := font_xml.find(f"{charstrings}/CharString[@name='{uni}']")) is None:
        # Doesn't exist
        lxml.etree.SubElement(charstrings, "CharString", {"name": uni}).text = f"{width} endchar"
        lxml.etree.SubElement(font_xml.find("hmtx"), "mtx", {"name": uni, "width": str(width), "lsb": "0"})
    elif replace:
        # Exists already in the charstrings, replace it too
        charstring_xml.text = f"{width} endchar"
        font_xml.find(f"hmtx/mtx[@name='{uni}']").set("width", str(width))


def add_namerecord_to_font(font_xml: lxml.etree._Element, data: str, name_id: int) -> None:
    """
    Set a namerecord in a font.

    This doesn't check if such a namerecord already exists; this will add new namerecords.

    * 0 -> Copyright
    * 1 -> Font family
    * 2 -> Font subfamily
    * 3 -> Unique font ID
    * 4 -> Full font name, ID 1 + 2
    * 5 -> Version: "Version maj.min"
    * 6 -> PostScript name
    * 7 -> Trademark
    * 8 -> Manufacturer
    * 9 -> Designer
    * 10 -> Descriptions

    See more at https://docs.microsoft.com/en-us/typography/opentype/spec/name#name-ids.

    All are encoded at (0, 4) and (3, 1), Unicode 2.0+ full.

    :param font_xml: The font XML.
    :param data: Whatever string to add.
    :param name_id: The ID of the namerecord.
    :returns: Nothing, font is modified in-place.
    """
    unicode_platenc = "3"  # Default value for Unicode BMP only.
    windows_platenc = "1"  # Default value for Windows BMP only.

    if any(ord(char) > 0xFFFF for char in data):  # Full Unicode
        unicode_platenc = "4"
        windows_platenc = "10"

    name_id = str(name_id)

    name_elements = font_xml.find("name")

    lxml.etree.SubElement(
        name_elements,
        "namerecord",
        {"platformID": "0", "platEncID": unicode_platenc, "nameID": name_id, "langID": "0x0"},
    ).text = data  # Unicode
    lxml.etree.SubElement(
        name_elements,
        "namerecord",
        {"platformID": "1", "platEncID": "32", "nameID": name_id, "langID": "0x0"},
    ).text = data.encode(
        "latin-1", errors="backslashreplace"
    )  # Macintosh (latin-1 only)
    lxml.etree.SubElement(
        name_elements,
        "namerecord",
        {"platformID": "3", "platEncID": windows_platenc, "nameID": name_id, "langID": "0x409"},
    ).text = data  # Windows


def set_cfffont_name(font_xml: lxml.etree._Element, font_name: str, family_name: str) -> None:
    """
    Set the font's appropriate CFF name in 'CFF ' tables.

    This is different from changing the 'name' tables, see :func:`add_namerecord_to_font` instead.

    :param font_xml: The font XML.
    :param font_name: The name of the font (doesn't include "Regular" or related weights).
    :param family_name: The family name of the font (doesn't include "Regular" or related weights).
    :returns: Nothing, font is modified in-place.
    """
    cfffont = font_xml.find("CFF/CFFFont")
    cfffont.set("name", sanitize_font_name(font_name))
    cfffont.find("FullName").set("value", font_name)
    cfffont.find("FamilyName").set("value", family_name)
    mcfonts.logger.debug(f"exporting: set CFF font name to {font_name}, family {family_name}")


def set_font_times(font_xml: lxml.etree._Element) -> None:
    """
    Set the font's created and modified times, in the format of ``%a %b %d %X %Y``.

    :param font_xml: The font XML.
    :returns: Nothing, font is modified in-place.
    """
    time = datetime.datetime.now().strftime("%a %b %d %X %Y")
    font_xml.find("head/created").set("value", time)
    font_xml.find("head/modified").set("value", time)


def set_notdef_in_font(font_xml: lxml.etree._Element, program: list[str]) -> None:
    """
    Set the ``.notdef`` character of the font.

    .. note::
        The default font template already has a default notdef, so use this for setting it to something else.

    :param font_xml: The font XML.
    :param program: A list of strings of the glyph's program.
    :returns: Nothing, font is modified in-place.
    """
    font_xml.find("CFF/CFFFont/CharStrings/CharString[@name='.notdef']").text = " ".join(str(x) for x in program)
    font_xml.find("hmtx/mtx[@name='.notdef']").set("width", str(program[0]))
    mcfonts.logger.debug("exporting: set notdef")


def set_font_name(font_xml: lxml.etree._Element, font_name: str, include_credits: bool = True) -> None:
    """
    Set the font's name to `font_xml` in all appropriate places.

    This is different from :func:`set_cfffont_name`, which sets the name for only CFF tables.

    :param font_xml: The font XML.
    :param font_name: The name of the font.
    :param include_credits: If credits and links to mcfonts are included in the namerecords.
    """
    font_name = font_name.encode("ascii", "ignore").decode("utf-8")  # Ignore anything not in ASCII
    add_namerecord_to_font(font_xml, font_name, 1)
    set_cfffont_name(font_xml, font_name, font_name)
    add_namerecord_to_font(font_xml, "Regular", 2)
    if include_credits:
        add_namerecord_to_font(font_xml, "🄯 Public domain", 0)
        add_namerecord_to_font(font_xml, f"mcfonts: {font_name} Regular: {hash(font_xml)}", 3)
        add_namerecord_to_font(font_xml, "mcfonts", 8)
        add_namerecord_to_font(font_xml, f"{font_name} has no trademark.", 7)
        add_namerecord_to_font(font_xml, "https://gitlab.com/whoatemybutter/mcfonts", 11)
        add_namerecord_to_font(
            font_xml,
            (
                "This font is under no explicit licensing. "
                "This font's author may have additional licensing terms, contact them."
            ),
            13,
        )
    else:
        add_namerecord_to_font(font_xml, f"{font_name} Regular: {hash(font_xml)}", 3)
    add_namerecord_to_font(font_xml, f"{font_name} Regular", 4)
    add_namerecord_to_font(
        font_xml,
        f"Version 1.0; {datetime.date.strftime(datetime.date.today(), '%B %d, %Y')}",
        5,
    )
    add_namerecord_to_font(font_xml, sanitize_font_name(font_name), 6)
    set_font_times(font_xml)


EXCLUDED_FONT_NAME_CHARS = re.compile(r"[{}\[\]() <>%/]")


def sanitize_font_name(font_name: str) -> str:
    """
    Ensure ``sanitized_font_name`` is a valid PostScript font name.

    A PostScript font name can't:

    * Contain ``(){}[]<;>%/`` or space
    * Be longer than 63 characters
    * Have non-ASCII characters

    >>> sanitize_font_name("\u2600 This is a really long name!")
    '_This_is_a_really_long_name!'
    >>> sanitize_font_name("(secret info) [do not leak]")
    '_secret_info___do_not_leak_'
    >>> sanitize_font_name("a really long name with over 63 characters I guarentee it you won't believe it")
    'a_really_long_name_with_over_63_characters_I_guarentee_it_you_w'

    :param font_name: The font name to sanitize.
    :returns: A valid PostScript font name.
    """
    return EXCLUDED_FONT_NAME_CHARS.sub("_", font_name)[:63].encode("ascii", "ignore").decode("ascii")


def generate_ulunicoderange(characters: set[str]) -> list[str]:
    """
    Given a set of characters, return a list of ulUnicodeRanges, with bits set appropriately.

    See https://learn.microsoft.com/en-us/typography/opentype/spec/os2#ur.

    >>> generate_ulunicoderange({"A", "B", "\u2600", "\u1BFF", "\uFFFD"})
    [
        '00000000 00000000 00000000 00000000',
        '00000000 00000000 00000000 00100000',
        '00000000 00000000 01000000 00000000',
        '00000000 00000000 00000000 00000001',
    ]

    :param characters: A set of characters.
    :return: A list of ulUnicodeRanges, as strings, in order from 1 to 4.
    """
    ul = 0
    for character in characters:
        codepoint = ord(character)
        for unicode_range, bit in ULUNICODERANGE_BIT_MAP.items():
            if unicode_range[0] <= codepoint <= unicode_range[1]:
                # Set the `bit`th bit in integer `ul`.
                # See https://stackoverflow.com/a/28360656.
                ul ^= (-1 ^ ul) & (1 << bit)
    ul_binary_string = f"{ul:0128b}"
    ul_finished = []
    # Split string into lengths, see https://stackoverflow.com/a/13673133.
    for elem in (ul_binary_string[i : i + 32] for i in range(0, 128, 32)):
        ul_finished.append(" ".join([elem[i : i + 8] for i in range(0, 32, 8)]))
    return ul_finished[::-1]


def set_ulunicoderange(font_xml: lxml.etree._Element, characters: set[str]) -> None:
    """
    Generate the ulUnicodeRanges corresponding to `characters` and set them in `font_xml`.

    :param font_xml: A font XML.
    :param characters: A set of characters to generate ulUnicodeRanges for.
    """
    ul = generate_ulunicoderange(characters)
    os2 = font_xml.find("OS_2")
    os2.find("ulUnicodeRange1").set("value", ul[0])
    os2.find("ulUnicodeRange2").set("value", ul[1])
    os2.find("ulUnicodeRange3").set("value", ul[2])
    os2.find("ulUnicodeRange4").set("value", ul[3])
