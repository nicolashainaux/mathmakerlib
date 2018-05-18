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

from mathmakerlib.geometry import Point
from mathmakerlib.geometry.bipoint import Bipoint


def test_repr():
    """Check Bipoint.__repr__()"""
    A = Point(0, 0, 'A')
    B = Point(1, 1, 'B')
    assert repr(Bipoint(A, B)) == 'Bipoint(Point A(0, 0), Point B(1, 1))'


def test_equality():
    """Check __eq__() is correct."""
    A = Point(0, 0, 'A')
    B = Point(1, 1, 'B')
    s = Bipoint(A, B)
    t = Bipoint(B, A)
    u = Bipoint(B, A)
    assert s != t
    assert t == u


def test_addition():
    """Check Bipoints' additions."""
    pointO = Point(0, 0, 'O')
    pointI = Point(1, 0, 'I')
    pointJ = Point(0, 1, 'J')
    pointA = Point(1, 1, 'A')
    with pytest.raises(TypeError) as excinfo:
        Bipoint(pointO, pointI) + 'a'
    assert str(excinfo.value) == 'Can only add a Bipoint to another '\
        'Bipoint. Found \'a\' instead.'
    i = Bipoint(pointO, pointI)
    j = Bipoint(pointO, pointJ)
    assert i + j == Bipoint(pointO, pointA)
    assert i.add(j) == Bipoint(pointO, pointA)