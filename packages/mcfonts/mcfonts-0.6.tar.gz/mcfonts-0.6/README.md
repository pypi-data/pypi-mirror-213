[![mcfonts](logo.png)](https://gitlab.com/whoatemybutter/mcfonts)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Pylint](https://img.shields.io/badge/pylint-9.94-ffbf48)](https://pylint.pycqa.org/en/latest/)
[![License](https://img.shields.io/badge/license-MIT-a51931)](https://spdx.org/licenses/MIT.html)
[![PyPi](https://img.shields.io/pypi/v/mcfonts)](https://pypi.org/project/mcfonts/)
[![GitLab Release (latest by SemVer)](https://img.shields.io/gitlab/v/release/38935127?sort=semver)](https://gitlab.com/whoatemybutter/mcfonts/-/releases)

**mcfonts** is a versatile, fast, and extensible package for working with Minecraft fonts.
<br/>
mcfonts works with any font JSON and can export every kind of texture & size, no matter the amount or complexity.
<br/>
It can be used anywhere in places that deal with Minecraft fonts.

> ⚠️ mcfonts is in beta. API may change at any time, read the changelog carefully.

---

## Table of contents
- [📦 Installation](#-installation)
- [🧮 Features](#-features)
- [🛠 Usage](#-usage)
- [❓ Why?](#-why)
- [📒 Documentation](#-documentation)
    - [Building locally](#building-locally)
- [📰 Changelog](#-changelog)
- [📜 License](#-license)
    - [🚫 Disclaimer](#-disclaimer)
- [📎 Links](#-links)

---

## 📦 Installation

`mcfonts` is available on PyPI.
It requires a Python version of **at least 3.11.0.**

To install `mcfonts` with pip, run:
```shell
python -m pip install mcfonts
```

If you would like the ability to generate documentation alongside it, run:
```shell
python -m pip install mcfonts[docs]
```

### "externally-managed-environment"

This error occurs on some Linux distributions such as Fedora 38 and Ubuntu 23.04.
It can be solved by either:

1. Using a [virtual environment (venv)](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
2. Using [pipx](https://github.com/pypa/pipx)

### Dependencies

* [fontTools](https://pypi.org/project/fontTools/): for exporting to OpenType
* [lxml](https://pypi.org/project/lxml/): for fast XML parsing
* [Pillow](https://pypi.org/project/Pillow/): for processing font textures
* [tinyunicodeblock](https://pypi.org/project/tinyunicodeblock/): for font coverage summaries
* [jsonschema](https://pypi.org/project/jsonschema): for the font JSON validation
* [unirange](https://pypi.org/project/unirange/): for special unirange shortcuts

#### Optional dependencies

`docs`: Generating documentation
* [sphinx](https://pypi.org/project/sphinx/): for generating documentation
* [sphinx-autoapi](https://pypi.org/project/sphinx-autoapi/): for generating code documentation
* [sphinxext-opengraph](https://pypi.org/project/sphinxext-opengraph/): for meta tags
* [sphinx-immaterial](https://pypi.org/project/sphinx-immaterial/): for documentation theme

---

## 🧮 Features

* Handles these providers:
    * `space`
    * `bitmap`
    * `legacy_unicode`
    * `ttf`
    * `unihex`
    * `reference`
* Warns of invalid data
* Finds oversights that the Vanilla client does not notice
* Generates optimized and space-saving glyph paths
* Works with any font, not just Vanilla
* Works on fonts with double, triple, or quadruple scales
* Generates summaries of fonts
* Allows easy inspection of a font's details
* Contains glyph utilities and compacting functions
* Works on new 1.20+ `unihex` and `reference` providers

---

## 🛠 Usage
Using `mcfonts` is simple.

```python
import mcfonts

font = mcfonts.from_java_font_file("path/to/font.json")
# Do stuff with `font`...
```

### Exporting

To export to OpenType:

```python
import mcfonts

font = mcfonts.from_java_font_file("path/to/font.json")
font.export("My cool font").save("My cool font.otf")
```
That's it. Your font is at `./My cool font.otf`.

If you have a font with ~200 characters, it generated in ~0.3 seconds.
<br/>
If you have a font with ~2,000 characters, it generated in ~3.2 seconds.
<br/>
If you have a font with ~13,000 characters, it generated in ~9.9 seconds.
<br/>
If you have a font with ~60,000 characters, you've made a mistake.
<small>(your font generated in ~1 minute, 14 seconds.)</small>

> ❗ Note: Only OpenType fonts are supported for exporting.</br>
> Use other utilities such as [FontForge](https://fontforge.org/en-US/) to convert between formats.

---

## ❓ Why?
### ⏳ It's fast

In the time it has taken you to read this sentence,
a font with 1,000 glyphs has already been generated.

A 13,000 glyph font takes 10 seconds.

A simple 100 glyph font? A fraction of a second; it takes 0.1s.

### ➿ It's versatile

`mcfonts` works on fonts of any height, ascent, and size.

It correctly compensates & warns about oversized characters,
translucent textures, and invalid data.

### 🧠 It makes sense

Fonts are organized by a class, instead of using individual functions.

Providers, too, have their own classes.

Exporting and compacting are separated into their own functions, which makes debugging & modification easy.

> **`mcfonts` does not fix mistakes in fonts.**

It will extrapolate missing data, but empty/corrupt textures, invalid numbers,
or extreme cases will result in an error when trying to create a `MinecraftFont` instance with them.

This gives you the ability to correct these problems, instead of silently making them work
(sometimes with limited effectiveness) and keeping you in the dark about future issues.

### 📜 It's documented

`mcfonts` has extensive documentation, both externally and in the source code.
Functions are carefully written with rST-style docstrings,
and module variables are given precise descriptions.

---

## 📒 Documentation

Documentation for `mcfonts` is available at https://mcfonts.readthedocs.io.

### Building locally
You can build the documentation yourself by grabbing a copy of the source code:

```shell
git clone https://gitlab.com/whoatemybutter/mcfonts.git
cd mcfonts/docs
```

The documenation has a few requirements, install them all with:
```shell
python -m pip install -r requirements.txt
```

Run `make html` to begin building the documentation.
It will be at `_build/html/index.html`.

---

## 📰 Changelog

The changelog is at [CHANGELOG.md](CHANGELOG.md).

---

## 📜 License

`mcfonts` is licensed under the [MIT license](https://spdx.org/licenses/MIT.html).
<br/>
Fonts created with this tool are under **no explicit license**; you can license them in any way you want.
This includes under a paid license.<br/>
*By default, fonts created by this tool are under the public domain.*

Although credit is embedded in exported fonts, *removing this credit **is** allowed*,
and the function parameter `mcfonts.MinecraftFont.export(include_credit)` may be set to `False`.
<br/>

**Keeping it in is greatly appreciated and helps make `mcfonts` better.
There is no disadvantage to leaving the credit in.**

### 🚫 Disclaimer

> **mcfonts is not affiliated, endorsed, created, supported, or an official product
> by Mojang Studios or by Microsoft Corporation or by any of their associates in any way.**

---

## 📎 Links

* [Minecraft Wiki - Fonts](https://minecraft.fandom.com/wiki/Resource_Pack#Fonts)
* [OpenType specification](https://docs.microsoft.com/en-us/typography/opentype/spec/)
* [FontForge](https://fontforge.org/)
