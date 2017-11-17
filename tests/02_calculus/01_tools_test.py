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
from decimal import Decimal

from mathmakerlib.calculus import is_number, is_integer, is_natural
from mathmakerlib.calculus import prime_factors


def test_is_number():
    """Check numbers are correctly identified."""
    assert is_number(104)
    assert is_number(1.0)
    assert is_number(4 + 9.0 ** 3)
    assert is_number(Decimal('4'))
    assert not is_number('4')
    assert not is_number([1])


def test_is_integer():
    """Check integers are correctly identified."""
    assert is_integer(9)
    assert is_integer(-9)
    assert is_integer(10 + 59 // 7)
    assert is_integer(1.0)
    assert is_integer(-1.0)
    assert is_integer(Decimal('1.0'))
    assert is_integer(Decimal('-1.0'))
    assert not is_integer(Decimal('1.01'))
    assert not is_integer(Decimal('-1.01'))
    with pytest.raises(TypeError):
        is_integer('1.0')
    with pytest.raises(TypeError):
        is_integer('-1.0')


def test_is_natural():
    """Check naturals are correctly identified."""
    assert is_natural(0)
    assert is_natural(-0)
    assert is_natural(9)
    assert not is_natural(-9)
    assert is_natural(10 + 59 // 7)
    assert is_natural(1.0)
    assert not is_natural(-1.0)
    assert is_natural(Decimal('1.0'))
    assert not is_natural(Decimal('-1.0'))
    assert not is_natural(Decimal('1.01'))
    assert not is_natural(Decimal('-1.01'))
    with pytest.raises(TypeError):
        is_natural('1.0')
    with pytest.raises(TypeError):
        is_natural('-1.0')


def test_prime_factors():
    """Checks prime_factors() results."""
    with pytest.raises(TypeError) as excinfo:
        prime_factors('a')
    assert str(excinfo.value) == 'The argument must be an integer.'
    assert prime_factors(1) == []
    assert prime_factors(2) == [2]
    assert prime_factors(3) == [3]
    assert prime_factors(4) == [2, 2]
    assert prime_factors(10) == [2, 5]
    assert prime_factors(16) == [2, 2, 2, 2]
    assert prime_factors(31) == [31]
    assert prime_factors(16065) == [3, 3, 3, 5, 7, 17]
    assert all(type(n) is int for n in prime_factors(210))
