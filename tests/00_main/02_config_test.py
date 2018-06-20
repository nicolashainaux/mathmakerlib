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

from mathmakerlib import config


def test_angles_setup_error():
    """Check exceptions raised by config."""
    with pytest.raises(TypeError) as excinfo:
        config.angles.DEFAULT_ARMSPOINTS_POSITION = 'a'
    assert str(excinfo.value) == 'DEFAULT_ARMSPOINTS_POSITION must be a '\
        'number, found <class \'str\'> instead.'


def test_receding_axis_angle_setup_error():
    """Check exceptions raised by config."""
    with pytest.raises(TypeError) as excinfo:
        config.oblique_projection.RECEDING_AXIS_ANGLE = 'a'
    assert str(excinfo.value) == 'RECEDING_AXIS_ANGLE must be a '\
        'number, found \'a\' instead.'


def test_ratio_setup_error():
    """Check exceptions raised by config."""
    with pytest.raises(TypeError) as excinfo:
        config.oblique_projection.RATIO = 'a'
    assert str(excinfo.value) == 'RATIO must be a '\
        'number, found \'a\' instead.'


def test_direction_setup_error():
    """Check exceptions raised by config."""
    with pytest.raises(ValueError) as excinfo:
        config.oblique_projection.DIRECTION = 'undefined'
    assert str(excinfo.value) == 'Incorrect direction value: '\
        '\'undefined\'. Available values belong to: {}.'\
        .format(config.DIRECTION_VALUES)


def test_dashpattern_setup_error():
    """Check exceptions raised by config."""
    with pytest.raises(ValueError) as excinfo:
        config.oblique_projection.DASHPATTERN = 'undefined'
    assert str(excinfo.value) == 'Incorrect dashpattern value: '\
        '\'undefined\'. Available values belong to: {}.'\
        .format(config.DASHPATTERN_VALUES)


def test_points_setup_error():
    """Check exceptions raised by config."""
    with pytest.raises(TypeError) as excinfo:
        config.points.DEFAULT_POSITION_PRECISION = 'a'
    assert str(excinfo.value) == 'DEFAULT_POSITION_PRECISION must be a '\
        'number, found <class \'str\'> instead.'
