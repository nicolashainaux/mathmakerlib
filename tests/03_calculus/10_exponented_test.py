# -*- coding: utf-8 -*-

# Mathmaker Lib offers lualatex-printable mathematical objects.
# Copyright 2006-2019 Nicolas Hainaux <nh.techn@gmail.com>

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

import pytest

from mathmakerlib.calculus import Number, Exponented


def test_exponented_errors():
    """Check initialization exceptions."""
    with pytest.raises(TypeError) as excinfo:
        Exponented('No Printable')
    assert str(excinfo.value) == 'The content of an Exponented must be a ' \
        'Printable object. An int would be ' \
        'accepted (turned into Number). Got <class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Exponented(3, exponent='No Printable')
    assert str(excinfo.value) == 'The exponent of an Exponented must be ' \
        'either None or a Printable object. An int would be ' \
        'accepted (turned into Number). Got <class \'str\'> instead.'


def test_repr():
    """Check __repr__."""
    assert repr(Exponented(Number(3))) == 'Exponented(Number(\'3\'))'
    assert repr(Exponented(Number(3), exponent=4)) \
        == 'Exponented(Number(\'3\')^Number(\'4\'))'


def test_exponented():
    """Check initialization."""
    assert Exponented(Number(3)).printed == '3'
    assert Exponented(3, exponent=2).printed == '3^{2}'
    assert Exponented(Number(-3), exponent=2).printed == '(-3)^{2}'
    assert Exponented(3, exponent=Exponented(6, exponent=2))\
        .printed == '3^{6^{2}}'
