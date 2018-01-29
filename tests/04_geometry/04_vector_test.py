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
from mathmakerlib.geometry import Point
from mathmakerlib.geometry.vector import Vector


@pytest.fixture()
def pointO():
    return Point(0, 0, 'O')


@pytest.fixture()
def pointI():
    return Point(1, 0, 'I')


@pytest.fixture()
def pointJ():
    return Point(0, 1, 'J')


@pytest.fixture()
def pointA():
    return Point(1, 1, 'A')


def test_addition(pointO, pointI, pointJ, pointA):
    """Check Vectors' additions."""
    with pytest.raises(TypeError) as excinfo:
        Vector(pointO, pointI) + 'a'
    assert str(excinfo.value) == 'Can only add a Vector to another Vector. ' \
        'Got <class \'str\'> instead.'
    i = Vector(pointO, pointI)
    j = Vector(pointO, pointJ)
    assert (i + j).same_as(Vector(pointO, pointA))


def test_unit_vector(pointO, pointI, pointA):
    """Check unit vector creation."""
    i = Vector(pointO, pointI)
    assert i.unit_vector().same_as(i)
    u = Vector(pointO, pointA)
    assert u.unit_vector().same_as(
        Vector(pointO,
               Point(Number('0.707'), Number('0.707'))))


def test_bisector_vector(pointO, pointI, pointJ, pointA):
    """Check bisector of two vectors."""
    i = Vector(pointO, pointI)
    j = Vector(pointO, pointJ)
    a = Vector(pointO, pointA)
    assert i.bisector_vector(j).same_as(a)
    k = Vector(pointO, Point(2, 0))
    assert k.bisector_vector(j).same_as(a)
    with pytest.raises(TypeError) as excinfo:
        k.bisector_vector('j')
    assert str(excinfo.value) == 'Can only create the bisector with another ' \
        'Vector. Got a <class \'str\'> instead.'
