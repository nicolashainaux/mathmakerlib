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

import pytest

from mathmakerlib.calculus import Unit, physical_quantity, Number


def test_physical_quantity():
    """Check physical_quantity()"""
    assert physical_quantity('mm') == 'length'
    assert physical_quantity('hL') == 'capacity'
    assert physical_quantity('pg') == 'mass'
    assert physical_quantity('undefined') is None


def test_Unit_errors():
    """Check the Unit class exceptions."""
    with pytest.raises(TypeError) as excinfo:
        Unit(6)
    assert str(excinfo.value) == 'content must be a str or a Unit. ' \
        'Got <class \'int\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Unit('cm', exponent=2)
    assert str(excinfo.value) == 'The exponent of an Exponented must be ' \
        'either None or a Printable object. Got <class \'int\'> instead.'


def test_Unit():
    """Check the Unit class."""
    assert Unit('cm').printed == 'cm'
    assert Unit('cm', exponent=Number(2)).printed == 'cm^{2}'
    u = Unit('cm')
    assert Unit(u).printed == 'cm'
    assert Unit(u, exponent=Number(2)).printed == 'cm^{2}'
    assert Unit(u, exponent=Number(3)).printed == 'cm^{3}'
    u = Unit('cm', exponent=Number(2))
    assert Unit(u).printed == 'cm^{2}'
    v = Unit('cm', exponent=Number(2))
    assert u == v
    w = Unit(v, exponent=Number(3))
    assert v != w
    w = Unit(v, exponent=Number(2))
    assert v == w
    assert u != 6


def test_printing():
    """Check printing."""
    assert Unit('cm', exponent=Number(2)).uiprinted == 'cm^2'
    assert Unit('cm', exponent=Number(2)).printed == 'cm^{2}'
    assert str(Unit('cm')) == 'cm'
    assert str(Unit('cm', exponent=Number(2))) == 'cm^2'


def test_repr():
    """Check __repr__."""
    assert repr(Unit('cm')) == 'Unit(\'cm\')'
    assert repr(Unit('cm', exponent=Number(2))) == 'Unit(\'cm\'^Number(\'2\'))'
