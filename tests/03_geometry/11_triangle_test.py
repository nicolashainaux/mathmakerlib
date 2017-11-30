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

from mathmakerlib.geometry import Point, Triangle


def test_instanciation_errors():
    """Check errors on Triangle's instanciation."""
    with pytest.raises(ValueError) as excinfo:
        Triangle(Point(0, 0), Point(0, 1))
    assert str(excinfo.value) == 'Three vertices are required to build a '\
        'Triangle. Found 2 instead.'


def test_instanciation():
    """Check Triangle's instanciation."""
    r = Triangle(Point(0, 0), Point(0, 1), Point(1, 1))
    assert r.type == 'Triangle'


def test_simple_drawing():
    """Check drawing the Triangle."""
    r = Triangle(Point(0, 0), Point(1, 0), Point(1, 1), name='BOT')
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (B) at (0,0);
\coordinate (O) at (1,0);
\coordinate (T) at (1,1);

% Draw Triangle
\draw[thick] (B)
-- (O)
-- (T)
-- cycle;

% Label Points
\draw (B) node[below left] {B};
\draw (O) node[below right] {O};
\draw (T) node[above] {T};
\end{tikzpicture}
"""


def test_drawing_with_labeled_sides():
    """Check drawing the Quadrilateral."""
    r = Triangle(Point(0, 0), Point(1, 0), Point(0, 1),
                 name='WAX')
    with pytest.raises(ValueError) as excinfo:
        r.setup_labels(labels=['one', 'two', 'three', 'four'])
    assert str(excinfo.value) == 'All three labels must be setup. Found '\
        '4 values instead.'
    with pytest.raises(ValueError) as excinfo:
        r.setup_labels(masks=[None, None])
    assert str(excinfo.value) == 'All three masks must be setup. Found '\
        '2 values instead.'
    r.setup_labels(labels=['one', 'two', 'three'])
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (W) at (0,0);
\coordinate (A) at (1,0);
\coordinate (X) at (0,1);

% Draw Triangle
\draw[thick] (W)
-- (A) node[midway, below, sloped] {one}
-- (X) node[midway, above, sloped] {two}
-- cycle node[midway, below, sloped] {three};

% Label Points
\draw (W) node[below left] {W};
\draw (A) node[right] {A};
\draw (X) node[above left] {X};
\end{tikzpicture}
"""
