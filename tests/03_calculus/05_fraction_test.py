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
# from decimal import Decimal

from mathmakerlib.exceptions import StopFractionReduction
from mathmakerlib.calculus import Sign, Number, Fraction


def test_instanciation_errors():
    """Check Fraction's instanciation exceptions."""
    with pytest.raises(TypeError) as excinfo:
        Fraction('+', 'x', 8)
    assert str(excinfo.value) == 'Numerator and denominator must be ' \
        'numbers. Got <class \'str\'> and <class \'int\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Fraction('+', 5, 8.4)
    assert str(excinfo.value) == 'Numerator and denominator must be ' \
        'integers. Got 5 and 8.4 instead.'
    with pytest.raises(TypeError) as excinfo:
        Fraction('x', 8)
    assert str(excinfo.value) == 'Numerator and denominator must be ' \
        'numbers. Got <class \'str\'> and <class \'int\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Fraction(5, 8.4)
    assert str(excinfo.value) == 'Numerator and denominator must be ' \
        'integers. Got 5 and 8.4 instead.'
    with pytest.raises(TypeError) as excinfo:
        Fraction('+', 8)
    assert str(excinfo.value) == 'Numerator and denominator must be ' \
        'numbers. Got <class \'int\'> and <class \'NoneType\'> instead.'


def test_instanciation():
    """Check Fraction's instanciation."""
    f = Fraction(5, 8)
    assert f.sign == '+'
    assert f.numerator == 5
    assert f.numerator == Number('5')
    assert f.denominator == 8
    assert f.denominator == Number('8')
    f = Fraction('+', 5, 8)
    assert f.sign == '+'
    assert f.numerator == 5
    assert f.numerator == Number('5')
    assert f.denominator == 8
    assert f.denominator == Number('8')
    f = Fraction('-', 5, 8)
    assert f.sign == '-'
    assert f.numerator == 5
    assert f.numerator == Number('5')
    assert f.denominator == 8
    assert f.denominator == Number('8')
    f = Fraction('-', -5, 8)
    assert f.sign == '-'
    assert f.numerator == -5
    assert f.numerator == Number('-5')
    assert f.denominator == 8
    assert f.denominator == Number('8')
    f = Fraction(from_decimal=Number('0.67'))
    assert f.numerator == 67
    assert f.denominator == 100
    assert f.printed == r'\dfrac{67}{100}'


def test_comparisons():
    """Check Fraction can be compared."""
    assert Fraction(5, 8) < 1
    assert Fraction(5, 8) <= 1
    assert Fraction(9, 8) > 1
    assert Fraction(9, 8) >= 1


def test_hash():
    """Check Fraction is hashable."""
    hash(Fraction('-', 5, 8))
    hash(Fraction(3, 4))


def test_equality():
    """Check Fraction __eq__ and __ne__."""
    assert Fraction(Sign('+'), 5, 8) == Fraction(5, 8)
    assert not (Fraction(Sign('+'), 5, 8) == Number('0.625'))
    assert Fraction('-', 5, 8) != Fraction(-5, 8)
    assert Fraction(Sign('+'), 5, 8) != Number('0.625')


def test__repr__():
    """Check __repr__ is correct."""
    assert repr(Fraction(3, 4)) == 'Fraction(3, 4)'
    assert repr(Fraction('-', 3, 4)) == 'Fraction(\'-\', 3, 4)'


def test_printing():
    """Check printing is correct."""
    assert Fraction(5, 8).printed == r'\dfrac{5}{8}'
    assert Fraction(5, 8).imprint(start_expr=False) == r'+\dfrac{5}{8}'
    assert Fraction(5, 8).imprint(start_expr=False, variant='user_input') \
        == '+5/8'
    assert Fraction(5, 8).uiprinted == '5/8'


def test_evaluation():
    """Check Fractions are correctly evaluated."""
    assert Fraction(3, 8).evaluate() == Number('0.375')
    assert Fraction(from_decimal=Number('1.79')).evaluate() == Number('1.79')


def test_reducing():
    """Check reducing is correct."""
    assert not Fraction(5, 8).is_reducible()
    assert Fraction(6, 8).is_reducible()
    assert Fraction(5, 8).reduced() == Fraction(5, 8)
    assert Fraction(6, 8).reduced() == Fraction(3, 4)
    with pytest.raises(TypeError) as excinfo:
        Fraction(6, 8).reduced_by('2')
    assert str(excinfo.value) == 'A Fraction can be reduced only by an ' \
        'integer, got <class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Fraction(6, 8).reduced_by(Number('2.4'))
    assert str(excinfo.value) == 'A Fraction can be reduced only by an ' \
        'integer, got 2.4 instead.'
    with pytest.raises(ValueError) as excinfo:
        Fraction(6, 8).reduced_by(4)
    assert str(excinfo.value) == 'Cannot divide 6 by 4 and get an integer.'
    with pytest.raises(ValueError) as excinfo:
        Fraction(6, 8).reduced_by(3)
    assert str(excinfo.value) == 'Cannot divide 8 by 3 and get an integer.'
    assert Fraction(6, 8).reduced_by(2) == Fraction(3, 4)
    assert Fraction(16, 8).reduced_by(8) == 2
    assert Fraction('-', 6, 8).reduced_by(2) == Fraction('-', 3, 4)
    assert Fraction('-', 16, 8).reduced_by(8) == -2
    assert Fraction(-6, 8).reduced_by(2) == Fraction(-3, 4)
    assert Fraction(-16, 8).reduced_by(8) == -2
    assert Fraction(6, -8).reduced_by(2) == Fraction(3, -4)
    assert Fraction(16, -8).reduced_by(8) == -2
    assert Fraction(6, 8).reduced_by(-2) == Fraction(3, 4)
    assert Fraction(16, 8).reduced_by(-8) == 2
    with pytest.raises(StopFractionReduction) as excinfo:
        Fraction(3, 4).reduce()
    assert str(excinfo.value) == 'Fraction(3, 4) can no further be reduced.'
    assert Fraction(6, 8).reduce() == Fraction(3, 4)
    assert Fraction(9, 3).reduce() == 3
