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
from mathmakerlib.geometry import Point, Rhombus


def test_instanciation_errors():
    """Check errors on Rhombus's instanciation."""
    with pytest.raises(TypeError) as excinfo:
        Rhombus(build_angle='30')
    assert str(excinfo.value) == 'Expected an integer as build_angle, '\
        'found <class \'str\'>.'


def test_instanciation():
    """Check Rhombus's instanciation."""
    r = Rhombus()
    assert r.type == 'Rhombus'
    assert all([s.mark == '||' for s in r.sides])
    assert r.side_length == Number(1)


def test_sides_labeling():
    """Check Rhombus's sides' labeling."""
    r = Rhombus()
    with pytest.raises(ValueError) as excinfo:
        r.lbl_side_length
    assert str(excinfo.value) == 'Found no side labeled as a Number.'
    for s in r.sides:
        s.unlock_label()
    r.sides[0].label = Number(3, unit='cm')
    r.sides[3].label = Number(4, unit='cm')
    with pytest.raises(ValueError) as excinfo:
        r.lbl_side_length
    assert str(excinfo.value) == 'Found different values for the sides: '\
        'Number(\'3 cm\') and Number(\'4 cm\').'
    for s in r.sides:
        s.lock_label()
    r.setup_labels([Number('1.5', unit='cm')])
    assert all([s.label_value == Number('1.5', unit='cm') for s in r.sides])


def test_simple_drawing():
    """Check drawing the Rhombus."""
    r = Rhombus(name='EASY')
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (E) at (0,0);
\coordinate (A) at (0.866,-0.5);
\coordinate (S) at (1.732,0);
\coordinate (Y) at (0.866,0.5);

% Draw Rhombus
\draw[thick] (E)
-- (A) node[midway, sloped, scale=0.5] {||}
-- (S) node[midway, sloped, scale=0.5] {||}
-- (Y) node[midway, sloped, scale=0.5] {||}
-- cycle node[midway, sloped, scale=0.5] {||};

% Label Points
\draw (E) node[left] {E};
\draw (A) node[below] {A};
\draw (S) node[right] {S};
\draw (Y) node[above] {Y};
\end{tikzpicture}
"""
    r = Rhombus(start_vertex=Point(2, 2), name='EASY')
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (E) at (2,2);
\coordinate (A) at (2.866,1.5);
\coordinate (S) at (3.732,2);
\coordinate (Y) at (2.866,2.5);

% Draw Rhombus
\draw[thick] (E)
-- (A) node[midway, sloped, scale=0.5] {||}
-- (S) node[midway, sloped, scale=0.5] {||}
-- (Y) node[midway, sloped, scale=0.5] {||}
-- cycle node[midway, sloped, scale=0.5] {||};

% Label Points
\draw (E) node[left] {E};
\draw (A) node[below] {A};
\draw (S) node[right] {S};
\draw (Y) node[above] {Y};
\end{tikzpicture}
"""
