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

from mathmakerlib.calculus import Number
from mathmakerlib.exceptions import MathmakerLibError, StopCalculation
from mathmakerlib.exceptions import ZeroBipoint, ZeroVector
from mathmakerlib.exceptions import ZeroLengthLineSegment


def test_MathmakerLibError():
    """Check the main mathmakerlib exception."""
    with pytest.raises(MathmakerLibError) as excinfo:
        raise MathmakerLibError
    assert str(excinfo.value) == 'An error occured in Mathmaker Lib'


def test_StopCalculation():
    """Check StopCalculation exception."""
    with pytest.raises(StopCalculation) as excinfo:
        raise StopCalculation(Number('7.6'))
    assert str(excinfo.value) == 'No further calculation can be done on ' \
        'Number(\'7.6\').'


def test_ZeroBipoint():
    """Check ZeroBipoint exception."""
    with pytest.raises(ZeroBipoint) as excinfo:
        raise ZeroBipoint
    assert str(excinfo.value) == 'Abusive use of a zero Bipoint.'


def test_ZeroVector():
    """Check ZeroVector exception."""
    with pytest.raises(ZeroVector) as excinfo:
        raise ZeroVector
    assert str(excinfo.value) == 'Abusive use of a zero Vector.'


def test_ZeroLengthLineSegment():
    """Check ZeroLengthLineSegment exception."""
    with pytest.raises(ZeroLengthLineSegment) as excinfo:
        raise ZeroLengthLineSegment
    assert str(excinfo.value) == 'Abusive use of a zero-length LineSegment.'
