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

from mathmakerlib import required
from mathmakerlib.calculus import Number, Unit
from mathmakerlib.geometry import Point
from mathmakerlib.geometry.angle import AngleMark, Angle


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


def test_angle_mark():
    assert AngleMark().tikz_mark_attributes() \
        == '[draw, thick, angle radius = 0.25 cm]'
    assert AngleMark(color='green', thickness='thin').tikz_mark_attributes() \
        == '[draw, green, thin, angle radius = 0.25 cm]'
    assert AngleMark(radius=Number(0.5, unit=Unit('cm'))) \
        .tikz_mark_attributes() == '[draw, thick, angle radius = 0.5 cm]'
    with pytest.raises(TypeError) as excinfo:
        AngleMark(radius='2 cm')
    assert str(excinfo.value) == 'Expected a number as radius. Got ' \
        '<class \'str\'> instead.'


def test_instanciation_errors(pointO, pointI, pointJ):
    """Check Angle's instanciation exceptions."""
    with pytest.raises(ValueError) as excinfo:
        Angle(pointO, pointI)
    assert str(excinfo.value) == 'Three Points are required to build an ' \
        'Angle. Got 2 positional arguments instead.'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, 'J')
    assert str(excinfo.value) == 'Three Points are required to build an ' \
        'Angle. Positional argument #2 is <class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, pointJ, mark_right=1)
    assert str(excinfo.value) == '\'mark_right\' must be a boolean'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, pointJ, mark='right')
    assert str(excinfo.value) == 'An angle mark must belong to the ' \
        'AngleMark class. Got <class \'str\'> instead.'


def test_instanciation(pointO, pointI, pointJ, pointA):
    """Check Angle's instanciation."""
    theta = Angle(pointI, pointO, pointJ, mark_right=True)
    assert theta.measure == Number('90')
    assert theta.mark is None
    assert theta.mark_right
    assert theta.vertex == pointO
    assert theta.points == [pointI, pointO, pointJ]
    theta = Angle(pointA, pointO, pointI, mark=AngleMark())
    assert theta.measure == Number('45')
    assert not theta.mark_right
    assert theta.vertex == pointO
    assert theta.points == [pointA, pointO, pointI]


def test_marked_angles(pointO, pointI, pointJ, pointA):
    """Check Angle's instanciation."""
    required.tikz_library['angles'] = False
    theta = Angle(pointI, pointO, pointJ)
    assert theta.tikz_angle_mark() == ''
    theta.mark = AngleMark(color='red', thickness='ultra thick',
                           radius=Number(2))
    assert theta.tikz_angle_mark() \
        == 'pic [draw, red, ultra thick, angle radius = 2] {angle = I--O--J}'
    assert required.tikz_library['angles']
    required.tikz_library['angles'] = False
    theta.mark_right = True
    theta.mark = AngleMark()
    assert theta.tikz_angle_mark() == ''
    assert not required.tikz_library['angles']
    assert theta.tikz_rightangle_mark() == \
        '\draw[thick, cm={cos(0), sin(0), -sin(0), cos(0), (O)}]' \
        ' (0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);'
    assert theta.tikz_rightangle_mark(winding='clockwise') == \
        '\draw[thick, cm={cos(0), sin(0), -sin(0), cos(0), (O)}]' \
        ' (0.25 cm, 0) -- (0.25 cm, -0.25 cm) -- (0, -0.25 cm);'
    with pytest.raises(ValueError) as excinfo:
        theta.tikz_rightangle_mark(winding=None)
    assert str(excinfo.value) == 'Expect \'clockwise\' or \'anticlockwise\'. '\
        'Found \'None\' instead.'
