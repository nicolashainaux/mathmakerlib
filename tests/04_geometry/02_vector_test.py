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

from mathmakerlib.geometry import Point
from mathmakerlib.geometry.vector import Vector
from mathmakerlib.geometry.bipoint import Bipoint
from mathmakerlib.exceptions import ZeroVector


def test_instanciation_errors():
    """Check Vector's instanciation exceptions."""
    Point.reset_names()
    with pytest.raises(TypeError) as excinfo:
        Vector()
    assert str(excinfo.value) == 'Vector() takes one, two or three arguments '\
        '(0 given)'
    with pytest.raises(TypeError) as excinfo:
        Vector(Point(0, 0))
    assert str(excinfo.value) == 'a Vector can be created from one Bipoint, '\
        'found Point A(0, 0) instead.'
    Point.reset_names()
    with pytest.raises(TypeError) as excinfo:
        Vector(Point(0, 0), 4)
    assert str(excinfo.value) == 'a Vector can be created from two '\
        'arguments, either two Points or two numbers. Found Point A(0, 0) '\
        'and 4 instead.'
    with pytest.raises(ZeroVector) as excinfo:
        Vector(Point(1, 1), Point(1, 1), allow_zero_length=False)
    assert str(excinfo.value) == 'Explicitly disallowed creation of a '\
        'zero-length Vector.'


def test_instanciation():
    """Check Vector's instanciation."""
    u = Vector(Bipoint(Point(0, 0), Point(2, 5)))
    assert not u.three_dimensional
    u = Vector(Bipoint(Point(0, 0, 0), Point(2, 5)))
    assert u.three_dimensional
    v = Vector(Point(0, 0), Point(2, 5))
    assert not v.three_dimensional
    v = Vector(Point(0, 0, 0), Point(2, 5))
    assert v.three_dimensional
    w = Vector(2, 5)
    assert not w.three_dimensional
    assert w.z == 0
    assert w.x == 2
    assert w.y == 5
    assert w.coordinates == (2, 5, 0)
    w = Vector(2, 5, 0)
    assert w.three_dimensional


def test_repr():
    """Check Vector.__repr__()"""
    u = Vector(Bipoint(Point(0, 0), Point(2, 5)))
    assert repr(u) == 'Vector(2, 5)'
    u = Vector(Bipoint(Point(0, 0, 0), Point(2, 5)))
    assert repr(u) == 'Vector(2, 5, 0)'


def test_neg():
    """Check Vector.__neg__()"""
    u = Vector(2, 7)
    assert -u == Vector(-2, -7)
    u = Vector(-1, 8, -5)
    assert -u == Vector(1, -8, 5)


def test_equality():
    """Check __eq__() is correct."""
    assert Vector(1, 1) != Bipoint(Point(0, 0), Point(1, 1))
    assert Vector(1, 1) == Vector(Point(1, 1), Point(2, 2))


def test_addition():
    """Check Vectors' additions."""
    Ω = Point(0, 0, 'Ω')
    A = Point(1, 1, 'A')
    with pytest.raises(TypeError) as excinfo:
        Vector(0, 1) + Bipoint(Ω, A)
    assert str(excinfo.value) == 'Can only add a Vector to another Vector. '\
        'Found Bipoint(Point Ω(0, 0), Point A(1, 1)) instead.'
    u = Vector(1, 1)
    v = Vector(3, -7)
    assert u + v == Vector(4, -6)
    v = Vector(3, -7, 2)
    assert u + v == Vector(4, -6, 2)
    u = Vector(2, 5, -7)
    assert u + v == Vector(5, -2, -5)


def test_dot_product():
    """Check dot product of two Vectors."""
    Ω = Point(0, 0, 'Ω')
    A = Point(1, 1, 'A')
    with pytest.raises(TypeError) as excinfo:
        Vector(0, 1).dot(Bipoint(Ω, A))
    assert str(excinfo.value) == 'Can only calculate the dot product of a '\
        'Vector by another Vector. '\
        'Found Bipoint(Point Ω(0, 0), Point A(1, 1)) instead.'
    u = Vector(1, 1)
    v = Vector(3, -7)
    assert u.dot(v) == -4
    u = Vector(2, 5, -7)
    v = Vector(3, -7, 2)
    assert u.dot(v) == -43


def test_cross_product():
    """Check cross product of two Vectors."""
    Ω = Point(0, 0, 'Ω')
    A = Point(1, 1, 'A')
    with pytest.raises(TypeError) as excinfo:
        Vector(0, 1).cross(Bipoint(Ω, A))
    assert str(excinfo.value) == 'Can only calculate the cross product of a '\
        'Vector by another Vector. '\
        'Found Bipoint(Point Ω(0, 0), Point A(1, 1)) instead.'
    assert Vector(1, 0).cross(Vector(0, 1)) == Vector(0, 0, 1)
    assert Vector(1, 0, 0).cross(Vector(0, 1, 0)) == Vector(0, 0, 1)
    assert Vector(3, 4, 5).cross(Vector(2, 5, 6)) == Vector(-1, -8, 7)


def test_normalized():
    """Check unit Vector creation."""
    assert Vector(3, 4).normalized() == Vector(0.6, 0.8)
    v = Vector(3, 4, 0).normalized()
    assert v.three_dimensional
    assert v == Vector(0.6, 0.8, 0)
    assert Vector(12, 15, 16).normalized() == Vector(0.48, 0.6, 0.64)


def test_bisector():
    """Check bisector of two Vectors."""
    Ω = Point(0, 0)
    pointI = Point(1, 0)
    J = Point(0, 1)
    A = Point(1, 1)
    i = Vector(Ω, pointI)
    j = Vector(Ω, J)
    a = Vector(Ω, A)
    assert i.bisector(j) == a
    assert j.bisector(i) == -a
    k = Vector(Ω, Point(2, 0))
    assert k.bisector(j) == a
    with pytest.raises(TypeError) as excinfo:
        k.bisector('j')
    assert str(excinfo.value) == 'Can only create the bisector with another ' \
        'Vector. Found \'j\' instead.'


def test_angle_measure():
    """Check angle measure between two Vectors."""
    Ω = Point(0, 0)
    pointI = Point(1, 0)
    A = Point(1, 1)
    i = Vector(Ω, pointI)
    a = Vector(Ω, A)
    assert i.angle_measure(a) == 45
    assert a.angle_measure(i) == 315
