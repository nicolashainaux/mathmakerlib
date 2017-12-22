# -*- coding: utf-8 -*-

# Mathmaker Lib offers lualatex-printable mathematical objects.
# Copyright 2006-2017 Nicolas Hainaux <nh.techn@gmail.com>

# This file is part of Mathmaker Lib.

# Mathmaker Lib is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.

# Mathmaker Lib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Mathmaker Lib; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

""" Module that monkey-patches the locale module so it remembers the last
arguments to setlocale() that didn't raise an exception and will allow them to
be retrieved later by calling a new function named setting_values() which is
also added by the patch.
Taken from https://stackoverflow.com/a/47930656/3926735
"""
import locale

_last_category, _last_locale = None, None


def my_setlocale(category, value=None):
    global _last_category, _last_locale

    try:
        result = _orig_setlocale(category, value)
    except locale.Error:
        raise  # Didn't work, ignore arguments.

    _last_category, _last_locale = category, value
    return result


def setting_values():
    global _last_category, _last_locale

    if _last_category is None:
        return locale.LC_ALL, 'C'

    return _last_category, _last_locale


# Monkey-patch the module.
_orig_setlocale = locale.setlocale
locale.setlocale = my_setlocale
locale.setting_values = setting_values  # New module function.
