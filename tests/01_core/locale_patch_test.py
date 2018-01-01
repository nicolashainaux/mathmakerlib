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

import sys
import locale
import pytest

from mathmakerlib import locale_patch

LOCALE_US = 'en' if sys.platform.startswith('win') else 'en_US.UTF-8'
LOCALE_FR = 'fr' if sys.platform.startswith('win') else 'fr_FR.UTF-8'


def test_errors():
    """Check errors are handled correctly."""
    with pytest.raises(locale.Error) as excinfo:
        locale.setlocale(locale.LC_ALL, 'undefined')
    assert str(excinfo.value) == 'unsupported locale setting'
    with pytest.raises(locale.Error) as excinfo:
        locale.setlocale(locale.LC_ALL, locale='undefined')
    assert str(excinfo.value) == 'unsupported locale setting'
    locale_patch._last_category = locale_patch._last_locale = None
    with pytest.raises(RuntimeError) as excinfo:
        locale.setting_values()
    assert str(excinfo.value) == 'You must sucessfully set the locale *after*'\
        ' having imported mathmakerlib and *before* you '\
        'try to print locale-related output using it. '\
        'This exception is typically raised when trying '\
        'to print a Number in a temporarily modified '\
        'locale when the locale is unset.'


def test_patched_set_locale():
    """Check behaviour when locale has een set."""
    locale.setlocale(locale.LC_ALL, LOCALE_FR)
    assert locale.setting_values() == (locale.LC_ALL, LOCALE_FR)
    locale.setlocale(locale.LC_ALL, locale=LOCALE_FR)
    assert locale.setting_values() == (locale.LC_ALL, LOCALE_FR)
    locale.setlocale(locale.LC_ALL, LOCALE_US)
