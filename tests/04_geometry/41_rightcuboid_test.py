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
from mathmakerlib.geometry import Point, RightCuboid


def test_instanciation_errors():
    """Check errors when instanciating a new RightCuboid."""
    with pytest.raises(TypeError) as excinfo:
        RightCuboid(start_vertex=Number(0.8))
    assert str(excinfo.value) == 'start_vertex must be a Point; found '\
        'Number(\'0.8\') instead.'
    with pytest.raises(TypeError) as excinfo:
        RightCuboid(start_vertex=Point(2, 3, 'A'))
    assert str(excinfo.value) == 'start_vertex must be a three-dimensional '\
        'Point. Found this two-dimensional Point instead: Point A(2, 3).'
    with pytest.raises(TypeError) as excinfo:
        RightCuboid(start_vertex=Point(0, 0, 0))
    assert str(excinfo.value) == 'dimensions must be a tuple or a list. '\
        'Found None instead.'
    with pytest.raises(TypeError) as excinfo:
        RightCuboid(start_vertex=Point(0, 0, 0), dimensions=(2, 4))
    assert str(excinfo.value) == 'dimensions must have a length of 3. ' \
        'Found (2, 4) instead.'


def test_instanciation():
    """Check new RightCuboids instanciations."""
    rc = RightCuboid(dimensions=(4, 3, 2), name='FLAVORED')
    assert rc.width == 4
    assert rc.depth == 3
    assert rc.height == 2
    assert rc.vertices[0] == Point(0, 0, 0)
