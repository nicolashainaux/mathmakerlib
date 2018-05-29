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


@pytest.fixture()
def rc(): return RightCuboid(dimensions=(4, 3, 2), name='FLAVORED')


def test_instanciation_start_vertex_error():
    """Check errors when instanciating a new RightCuboid."""
    with pytest.raises(TypeError) as excinfo:
        RightCuboid(start_vertex=Number(0.8))
    assert str(excinfo.value) == 'start_vertex must be a Point; found '\
        'Number(\'0.8\') instead.'


def test_instanciation_2D_start_vertex_error():
    """Check errors when instanciating a new RightCuboid."""
    with pytest.raises(TypeError) as excinfo:
        RightCuboid(start_vertex=Point(2, 3, 'A'))
    assert str(excinfo.value) == 'start_vertex must be a three-dimensional '\
        'Point. Found this two-dimensional Point instead: Point A(2, 3).'


def test_instanciation_dimension_error():
    """Check errors when instanciating a new RightCuboid."""
    with pytest.raises(TypeError) as excinfo:
        RightCuboid(start_vertex=Point(0, 0, 0))
    assert str(excinfo.value) == 'dimensions must be a tuple or a list. '\
        'Found None instead.'


def test_instanciation_no3D_dimension_error():
    """Check errors when instanciating a new RightCuboid."""
    with pytest.raises(TypeError) as excinfo:
        RightCuboid(start_vertex=Point(0, 0, 0), dimensions=(2, 4))
    assert str(excinfo.value) == 'dimensions must have a length of 3. ' \
        'Found (2, 4) instead.'


def test_instanciation(rc):
    """Check new RightCuboids instanciations."""
    assert rc.width == 4
    assert rc.depth == 3
    assert rc.height == 2
    assert rc.vertices[0] == Point(0, 0, 0)


def test_unset_labels_width_error(rc):
    """Check errors when accessing an unset attribute of a RightCuboid."""
    with pytest.raises(AttributeError) as excinfo:
        rc.lbl_width
    assert str(excinfo.value) == 'Labels must be set before trying to get '\
        'them.'


def test_unset_labels_depth_error(rc):
    """Check errors when accessing an unset attribute of a RightCuboid."""
    with pytest.raises(AttributeError) as excinfo:
        rc.lbl_depth
    assert str(excinfo.value) == 'Labels must be set before trying to get '\
        'them.'


def test_unset_labels_height_error(rc):
    """Check errors when accessing an unset attribute of a RightCuboid."""
    with pytest.raises(AttributeError) as excinfo:
        rc.lbl_height
    assert str(excinfo.value) == 'Labels must be set before trying to get '\
        'them.'


def test_unset_labels_volume_error(rc):
    """Check errors when accessing an unset attribute of a RightCuboid."""
    with pytest.raises(AttributeError) as excinfo:
        rc.lbl_volume
    assert str(excinfo.value) == 'Labels must be set before trying to get '\
        'them.'


def test_setup_labels_error(rc):
    """Check errors when accessing an unset attribute of a RightCuboid."""
    with pytest.raises(TypeError) as excinfo:
        rc.setup_labels((4, 5))
    assert str(excinfo.value) == 'labels argument must be a list or tuple, '\
        'of length 3. Found (4, 5) instead.'


def test_volume_from_labels(rc):
    """Check calculation of volume from labels of a RightCuboid."""
    rc.setup_labels((4, 5, 6))
    assert rc.lbl_volume == 120
