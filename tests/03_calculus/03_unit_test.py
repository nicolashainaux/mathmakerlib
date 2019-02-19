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
from decimal import Decimal

from mathmakerlib import required
from mathmakerlib.calculus import Unit, physical_quantity, Number
from mathmakerlib.calculus import difference_of_orders_of_magnitude


def test_physical_quantity():
    """Check physical_quantity()"""
    assert physical_quantity('mm') == 'length'
    assert physical_quantity('hL') == 'capacity'
    assert physical_quantity('pg') == 'mass'
    assert physical_quantity(Unit('pg')) == 'mass'
    assert physical_quantity(Unit('mm', exponent=2)) == 'area'
    assert physical_quantity(Unit('mm', exponent=3)) == 'volume'
    assert physical_quantity('undefined') is None
    assert physical_quantity(r'\officialeuro') == 'currency'
    assert physical_quantity(r'\textdegree') == 'angle'


def test_difference_of_orders_of_magnitude_exceptions():
    """Check wrong units trigger an error."""
    with pytest.raises(TypeError) as excinfo:
        difference_of_orders_of_magnitude('cm', 'hL')
    assert str(excinfo.value) == 'Cannot give the difference of orders of ' \
        'magnitude between two units that do not belong to the same physical '\
        'quantity (cm and hL).'


def test_difference_of_orders_of_magnitude():
    """Check the difference of orders of magnitude is calculated correctly."""
    assert difference_of_orders_of_magnitude('L', 'mL') == Decimal('1000')
    assert difference_of_orders_of_magnitude('cm', 'm') == Decimal('0.01')
    assert difference_of_orders_of_magnitude('kg', 'mg') == Decimal('1000000')


def test_Unit_errors():
    """Check the Unit class exceptions."""
    with pytest.raises(TypeError) as excinfo:
        Unit(6)
    assert str(excinfo.value) == 'content must be a str or a Unit. ' \
        'Got <class \'int\'> instead.'


def test_Unit():
    """Check the Unit class."""
    assert Unit('cm').printed == r'\si{cm}'
    assert Unit('cm', exponent=Number(2)).printed == r'\si{cm^{2}}'
    u = Unit('cm')
    assert Unit(u).printed == r'\si{cm}'
    assert Unit(u, exponent=2).printed == r'\si{cm^{2}}'
    assert Unit(u, exponent=Number(3)).printed == r'\si{cm^{3}}'
    u = Unit('cm', exponent=2)
    assert Unit(u).printed == r'\si{cm^{2}}'
    v = Unit('cm', exponent=2)
    assert u == v
    w = Unit(v, exponent=3)
    assert v != w
    w = Unit(v, exponent=2)
    assert v == w
    assert u != 6


def test_printing():
    """Check printing."""
    assert Unit('cm', exponent=2).uiprinted == 'cm^2'
    assert Unit('cm', exponent=2).printed == r'\si{cm^{2}}'
    assert str(Unit('cm')) == 'cm'
    assert str(Unit('cm', exponent=2)) == 'cm^2'
    required.package['eurosym'] = False
    Unit(r'\officialeuro').printed
    assert required.package['eurosym']


def test_repr():
    """Check __repr__."""
    assert repr(Unit('cm')) == 'Unit(\'cm\')'
    assert repr(Unit('cm', exponent=2)) == 'Unit(\'cm\'^Number(\'2\'))'
