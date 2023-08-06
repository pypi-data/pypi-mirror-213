#!/usr/bin/env python3
# coding=utf-8
# SPDX-License-Identifier: MIT
"""
ANSI color escapes.
The global variable ``USE_COLORS`` controls whether these will be used in outputs.

* Set :const:`USE_COLORS` to False to **disable** colored output.
* Set :const:`USE_COLORS` to True to **enable** colored output.
"""
from __future__ import annotations

USE_COLORS = True
"""
Whether to include ANSI color escapes in some prints.
Set this to False if your console/terminal does not support ANSI color escapes.
"""

_CSI = "\x1b["
BLACK_FORE = f"{_CSI}30m"
RED_FORE = f"{_CSI}31m"
GREEN_FORE = f"{_CSI}32m"
YELLOW_FORE = f"{_CSI}33m"
BLUE_FORE = f"{_CSI}34m"
MAGENTA_FORE = f"{_CSI}35m"
CYAN_FORE = f"{_CSI}36m"
WHITE_FORE = f"{_CSI}37m"
RESET_FORE = f"{_CSI}39m"

BLACK_BACK = f"{_CSI}40m"
RED_BACK = f"{_CSI}41m"
GREEN_BACK = f"{_CSI}42m"
YELLOW_BACK = f"{_CSI}43m"
BLUE_BACK = f"{_CSI}44m"
MAGENTA_BACK = f"{_CSI}45m"
CYAN_BACK = f"{_CSI}46m"
WHITE_BACK = f"{_CSI}47m"
RESET_BACK = f"{_CSI}49m"

RESET_ALL = f"{_CSI}0m"
BRIGHT = f"{_CSI}1m"
DIM = f"{_CSI}2m"


def color_number(number: float | int) -> str:
    """
    Given `number`, return a colorized and pretty-print version of that number.

    .. note::
        If :data:`mcfonts.colors.USE_COLORS` is False, color will not be applied.

    If `number` is negative, it will be in red.
    If `number` is positive, it will be in green.
    If `number` is zero, it will have no colors.

    >>> color_number(4)
    '\\x1b[32m+4\\x1b[39m'
    >>> color_number(-4)
    '\\x1b[31m-4\\x1b[39m'
    >>> color_number(-39924)
    '\\x1b[31m-39,924\\x1b[39m'

    :param number: The number, positive or negative.
    :returns: A string representing `number` with ANSI color codes.
    """
    if number < 0 and USE_COLORS:
        return f"{RED_FORE}{number:,}{RESET_FORE}"
    if number == 0 or not USE_COLORS:
        return f"{number:,}"
    if USE_COLORS:
        return f"{GREEN_FORE}+{number:,}{RESET_FORE}"
    return f"+{number:,}"
