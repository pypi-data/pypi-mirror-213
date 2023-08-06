#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
Constants for mcfonts.

This contains templates for providers, charlists, etc.
Old versions are not stored, and only the latest release is included.
As of this release, 1.19.3 is the latest.

Use :const:`RELEASE_DEFAULT` when looking to template a Vanilla resource without a provider.
"""
from __future__ import annotations

EMPTY_FONT_JSON: dict[str, list] = {"providers": []}
"""An empty font JSON with no providers."""

RELEASE_DEFAULT: dict = {
    "providers": [
        {"type": "space", "advances": {" ": 4, "\u200c": 0}},
        {
            "type": "bitmap",
            "file": "minecraft:font/nonlatin_european.png",
            "ascent": 7,
            "chars": [
                "¡‰­·₴≠¿×ØÞһðøþΑΒ",
                "ΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣ",
                "ΤΥΦΧΨΩαβγδεζηθικ",
                "λμνξοπρςστυφχψωЂ",
                "ЅІЈЉЊЋАБВГДЕЖЗИК",
                "ЛМНОПРСТУФХЦЧШЩЪ",
                "ЫЬЭЮЯабвгдежзикл",
                "мнопрстуфхцчшщъы",
                "ьэюяєѕіјљњ–—‘’“”",
                "„…⁊←↑→↓⇄＋ƏəɛɪҮүӨ",
                "өʻˌ;ĸẞß₽€ѢѣѴѵӀѲѳ",
                "⁰¹³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁱ™",
                "ʔʕ⧈⚔☠ҚқҒғҰұӘәҖҗҢ",
                "ңҺאבגדהוזחטיכלמם",
                "נןסעפףצץקר¢¤¥©®µ",
                "¶¼½¾·‐‚†‡•‱′″‴‵‶",
                "‷‹›※‼‽⁂⁈⁉⁋⁎⁏⁑⁒⁗℗",
                "−∓∞☀☁☈Є☲☵☽♀♂⚥♠♣♥",
                "♦♩♪♫♬♭♮♯⚀⚁⚂⚃⚄⚅ʬ⚡",
                "⛏✔❄❌❤⭐⸘⸮⸵⸸⹁⹋⥝ᘔƐ߈",
                "ϛㄥⱯᗺƆᗡƎℲ⅁ꞰꞀԀꝹᴚ⟘∩",
                "Ʌ⅄ɐɔǝɟᵷɥᴉɾʞꞁɯɹʇʌ",
                "ʍʎԱԲԳԴԶԷԹԺԻԼԽԾԿՀ",
                "ՁՂՃՄՅՆՇՈՉՋՌՍՎՏՐՑ",
                "ՒՓՔՕՖՙաբգդեզէըթժ",
                "իլխծկհձղճմյնշոչպ",
                "ջռսվտրցւփքօֆևשתԸ",
                "՚՛՜՝՞՟ՠֈ֏¯ſƷʒǷƿȜ",
                "ȝȤȥ˙Ꝛꝛ‑⅋⏏⏩⏪⏭⏮⏯⏴⏵",
                "⏶⏷⏸⏹⏺⏻⏼⏽⭘▲▶▼◀●◦◘",
                "⚓⛨ĲĳǉꜨꜩꜹꜻﬀﬁﬂﬃﬅ�Ե",
                "Պᚠᚢᚣᚤᚥᚦᚧᚨᚩᚪᚫᚬᚭᚮᚯ",
                "ᚰᚱᚲᚳᚴᚶᚷᚸᚹᚺᚻᚼᚽᚾᚿᛀ",
                "ᛁᛂᛃᛄᛅᛆᛇᛈᛉᛊᛋᛌᛍᛎᛏᛐ",
                "ᛑᛒᛓᛔᛕᛖᛗᛘᛙᛚᛛᛜᛝᛞᛟᛠ",
                "ᛡᛢᛣᛤᛥᛦᛧᛨᛩᛪ᛫᛬᛭ᛮᛯᛰ",
                "ᛱᛲᛳᛴᛵᛶᛷᛸ☺☻¦☹ך׳״װ",
                "ױײ־׃׆´¨ᴀʙᴄᴅᴇꜰɢʜᴊ",
                "ᴋʟᴍɴᴏᴘꞯʀꜱᴛᴜᴠᴡʏᴢ§",
                "ɱɳɲʈɖɡʡɕʑɸʝʢɻʁɦʋ",
                "ɰɬɮʘǀǃǂǁɓɗᶑʄɠʛɧɫ",
                "ɨʉʊɘɵɤɜɞɑɒɚɝƁƉƑƩ",
                "ƲႠႡႢႣႤႥႦႧႨႩႪႫႬႭႮ",
                "ႯႰႱႲႳႴႵႶႷႸႹႺႻႼႽႾ",
                "ႿჀჁჂჃჄჅჇჍაბგდევზ",
                "თიკლმნოპჟრსტუფქღ",
                "ყშჩცძწჭხჯჰჱჲჳჴჵჶ",
                "ჷჸჹჺ჻ჼჽჾჿתּשׂפֿפּכּײַיִ",
                "וֹוּבֿבּꜧꜦɺⱱʠʗʖɭɷɿʅʆ",
                "ʓʚ₪₾֊ⴀⴁⴂⴃⴄⴅⴆⴡⴇⴈⴉ",
                "ⴊⴋⴌⴢⴍⴎⴏⴐⴑⴒⴣⴓⴔⴕⴖⴗ",
                "ⴘⴙⴚⴛⴜⴝⴞⴤⴟⴠⴥ⅛⅜⅝⅞⅓",
                "⅔✉☂☔☄⛄☃⌛⌚⚐✎❣♤♧♡♢",
                "⛈☰☱☳☴☶☷↔⇒⇏⇔⇵∀∃∄∉",
                "∋∌⊂⊃⊄⊅∧∨⊻⊼⊽∥≢⋆∑⊤",
                "⊥⊢⊨≔∁∴∵∛∜∂⋃⊆⊇□△▷",
                "▽◁◆◇○◎☆★✘₀₁₂₃₄₅₆",
                "₇₈₉₊₋₌₍₎∫∮∝⌀⌂⌘〒ɼ",
                "ƄƅẟȽƚƛȠƞƟƧƨƪƸƹƻƼ",
                "ƽƾȡȴȵȶȺⱥȻȼɆɇȾⱦɁɂ",
                "ɃɄɈɉɊɋɌɍɎɏẜẝỼỽỾỿ",
                "Ꞩꞩ𐌰𐌱𐌲𐌳𐌴𐌵𐌶𐌷𐌸𐌹𐌺𐌻𐌼𐌽",
                "𐌾𐌿𐍀𐍁𐍂𐍃𐍄𐍅𐍆𐍇𐍈𐍉𐍊🌧🔥🌊",
                "⅐⅑⅕⅖⅗⅙⅚⅟↉🗡🏹🪓🔱🎣🧪⚗",
                "⯪⯫Ɑ🛡✂🍖🪣🔔⏳⚑₠₡₢₣₤₥",
                "₦₩₫₭₮₰₱₲₳₵₶₷₸₹₺₻",
                "₼₿              ",
            ],
        },
        {
            "type": "bitmap",
            "file": "minecraft:font/accented.png",
            "height": 12,
            "ascent": 10,
            "chars": [
                "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏ",
                "ÐÑÒÓÔÕÖÙÚÛÜÝàáâã",
                "äåæçìíîïñòóôõöùú",
                "ûüýÿĀāĂăĄąĆćĈĉĊċ",
                "ČčĎďĐđĒēĔĕĖėĘęĚě",
                "ĜĝḠḡĞğĠġĢģĤĥĦħĨĩ",
                "ĪīĬĭĮįİıĴĵĶķĹĺĻļ",
                "ĽľĿŀŁłŃńŅņŇňŊŋŌō",
                "ŎŏŐőŒœŔŕŖŗŘřŚśŜŝ",
                "ŞşŠšŢţŤťŦŧŨũŪūŬŭ",
                "ŮůŰűŲųŴŵŶŷŸŹźŻżŽ",
                "žǼǽǾǿȘșȚțΆΈΉΊΌΎΏ",
                "ΐΪΫάέήίΰϊϋόύώЀЁЃ",
                "ЇЌЍЎЙйѐёђѓїћќѝўџ",
                "ҐґḂḃḊḋḞḟḢḣḰḱṀṁṖṗ",
                "ṠṡṪṫẀẁẂẃẄẅỲỳèéêë",
                "ŉǧǫЏḍḥṛṭẒỊịỌọỤụ№",
                "ȇƔɣʃ⁇ǱǲǳǄǅǆǇǈǊǋǌ",
                "ℹᵫꜲꜳꜴꜵꜶꜷꜸꜺꜼꜽꝎꝏꝠꝡ",
                "ﬄﬆᚡᚵƠơƯưẮắẤấẾếốỚ",
                "ớỨứẰằẦầỀềồỜờỪừẢả",
                "ẲẳẨẩẺẻổỞỂểỈỉỎỏỔở",
                "ỦủỬửỶỷẠạẶặẬậẸẹỆệ",
                "ỘộỢợỰựỴỵỐƕẪẫỖỗữ☞",
                "☜☮ẴẵẼẽỄễỒỠỡỮỸỹҘҙ",
                "ҠҡҪҫǶ⚠⓪①②③④⑤⑥⑦⑧⑨",
                "⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳ⒶⒷⒸⒹⒺ",
                "ⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊ",
                "ⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚ",
                "ⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ̧",
                "ʂʐɶǍǎǞǟǺǻȂȃȦȧǠǡḀ",
                "ḁȀȁḆḇḄḅᵬḈḉḐḑḒḓḎḏ",
                "ḌᵭḔḕḖḗḘḙḜḝȨȩḚḛȄȅ",
                "ȆᵮǴǵǦḦḧḨḩḪḫȞȟḤẖḮ",
                "ḯȊȋǏǐȈȉḬḭǰȷǨǩḲḳḴ",
                "ḵḺḻḼḽḶḷḸḹⱢḾḿṂṃᵯṄ",
                "ṅṆṇṊṋǸǹṈṉᵰǬǭȬȭṌṍ",
                "ṎṏṐṑṒṓȎȏȪȫǑǒȮȯȰȱ",
                "ȌȍǪṔṕᵱȒȓṘṙṜṝṞṟȐȑ",
                "ṚᵳᵲṤṥṦṧṢṣṨṩᵴṰṱṮṯ",
                "ṬẗᵵṲṳṶṷṸṹṺṻǓǔǕǖǗ",
                "ǘǙǚǛǜṴṵȔȕȖṾṿṼṽẆẇ",
                "ẈẉẘẌẍẊẋȲȳẎẏẙẔẕẐẑ",
                "ẓᵶǮǯẛꜾꜿǢǣᵺỻᴂᴔꭣȸʣ",
                "ʥʤʩʪʫȹʨʦʧꭐꭑ₧Ỻאַאָƀ",
                "ƂƃƇƈƊƋƌƓǤǥƗƖɩƘƙƝ",
                "ƤƥɽƦƬƭƫƮȗƱƜƳƴƵƶƢ",
                "ƣȢȣʭʮʯﬔﬕﬗﬖﬓӐӑӒӓӶ",
                "ӷҔҕӖӗҼҽҾҿӚӛӜӝӁӂӞ",
                "ӟӢӣӤӥӦӧӪӫӰӱӮӯӲӳӴ",
                "ӵӸӹӬӭѶѷӔӺԂꚂꚀꚈԪԬꚄ",
                "ԄԐӠԆҊӃҞҜԞԚӅԮԒԠԈԔ",
                "ӍӉԨӇҤԢԊҨԤҦҎԖԌꚐҬꚊ",
                "ꚌԎҲӼӾԦꚔҴꚎҶӋҸꚒꚖꚆҌ",
                "ԘԜӕӻԃꚃꚁꚉԫԭꚅԅԑӡԇҋ",
                "ӄҟҝԟԛӆԯԓԡԉԕӎӊԩӈҥ",
                "ԣԋҩԥҧҏԗԍꚑҭꚋꚍԏҳӽӿ",
                "ԧꚕҵꚏҷӌҹꚓꚗꚇҍԙԝἈἀἉ",
                "ἁἊἂἋἃἌἄἍἅἎἆἏἇᾺὰᾸ",
                "ᾰᾹᾱΆάᾈᾀᾉᾁᾊᾂᾋᾃᾌᾄᾍ",
                "ᾅᾎᾆᾏᾇᾼᾴᾶᾷᾲᾳἘἐἙἑἚ",
                "ἒἛἓἜἔἝἕῈΈὲέἨἠῊὴἩ",
                "ἡἪἢἫἣἬἤἭἥἮἦἯἧᾘᾐᾙ",
                "ᾑᾚᾒᾛᾓᾜᾔᾝᾕᾞᾖᾟᾗΉήῌ",
                "ῃῂῄῆῇῚὶΊίἸἰἹἱἺἲἻ",
                "ἳἼἴἽἵἾἶἿἷῘῐῙῑῒΐῖ",
                "ῗῸὸΌόὈὀὉὁὊὂὋὃὌὄὍ",
                "ὅῬῤῥῪὺΎύὙὑὛὓὝὕὟὗ",
                "ῨῠῩῡϓϔῢΰῧὐὒὔῦὖῺὼ",
                "ΏώὨὠὩὡὪὢὫὣὬὤὭὥὮὦ",
                "Ὧὧᾨᾠᾩᾡᾪᾢᾫᾣᾬᾤᾭᾥᾮᾦ",
                "ᾯᾧῼῳῲῴῶῷ☯☐☑☒ƍƺⱾȿ",
                "ⱿɀᶀꟄꞔᶁᶂᶃꞕᶄᶅᶆᶇᶈᶉᶊ",
                "ᶋᶌᶍꟆᶎᶏᶐᶒᶓᶔᶕᶖᶗᶘᶙᶚ",
                "ẚ⅒⅘₨₯           ",
            ],
        },
        {
            "type": "bitmap",
            "file": "minecraft:font/ascii.png",
            "ascent": 7,
            "chars": [
                "                ",
                "                ",
                " !\"#$%&'()*+,-./",
                "0123456789:;<=>?",
                "@ABCDEFGHIJKLMNO",
                "PQRSTUVWXYZ[\\]^_",
                "`abcdefghijklmno",
                "pqrstuvwxyz{|}~ ",
                "                ",
                "            £  ƒ",
                "      ªº  ¬   «»",
                "░▒▓│┤╡╢╖╕╣║╗╝╜╛┐",
                "└┴┬├─┼╞╟╚╔╩╦╠═╬╧",
                "╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀",
                "             ∅∈ ",
                "≡±≥≤⌠⌡÷≈°∙ √ⁿ²■ ",
            ],
        },
        {
            "type": "legacy_unicode",
            "sizes": "minecraft:font/glyph_sizes.bin",
            "template": "minecraft:font/unicode_page_%s.png",
        },
    ]
}
"""The font JSON of default.json, the default Minecraft font."""
RELEASE_ALT: dict = {
    "providers": [
        {
            "type": "bitmap",
            "file": "minecraft:font/ascii_sga.png",
            "ascent": 7,
            "chars": [
                "                ",
                "                ",
                "                ",
                "                ",
                " ABCDEFGHIJKLMNO",
                "PQRSTUVWXYZ     ",
                " abcdefghijklmno",
                "pqrstuvwxyz     ",
                "                ",
                "                ",
                "                ",
                "                ",
                "                ",
                "                ",
                "                ",
                "                ",
            ],
        }
    ]
}
"""The font JSON of alt.json, the SGA font."""
RELEASE_UNIFORM: dict = {
    "providers": [
        {
            "type": "legacy_unicode",
            "sizes": "minecraft:font/glyph_sizes.bin",
            "template": "minecraft:font/unicode_page_%s.png",
        }
    ]
}
"""The font JSON of uniform.json, the Unicode fallback font."""

PROVIDER_NONLATIN: dict = RELEASE_DEFAULT["providers"][1]
"""The default provider for nonlatin-european."""
PROVIDER_ACCENTED: dict = RELEASE_DEFAULT["providers"][2]
"""The default provider for accented."""
PROVIDER_ASCII: dict = RELEASE_DEFAULT["providers"][3]
"""The default provider for ASCII."""

CHARLIST_NONLATIN = PROVIDER_NONLATIN["chars"]
"""The default charlist for nonlatin-european."""
CHARLIST_ACCENTED = PROVIDER_ACCENTED["chars"]
"""The default charlist for accented."""
CHARLIST_ASCII = PROVIDER_ASCII["chars"]
"""The default charlist for ASCII."""

PADDING_CHARS = {"\0", " "}
"""Characters that act as padding; glyphs cannot be assigned to these chars."""

UNKNOWN_FIELD = "???"
