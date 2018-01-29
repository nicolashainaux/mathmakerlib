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

from mathmakerlib.geometry import Point, EquilateralTriangle


def test_instanciation():
    """Check Triangle's instanciation."""
    t = EquilateralTriangle()
    assert t.type == 'EquilateralTriangle'
    assert t.side_length == 1


def test_simple_drawing():
    """Check drawing the Triangle."""
    t = EquilateralTriangle(name='KEY')
    assert t.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (K) at (0,0);
\coordinate (E) at (1,0);
\coordinate (Y) at (0.5,0.866);

% Draw EquilateralTriangle
\draw[thick] (K)
-- (E) node[midway, sloped, scale=0.5] {||}
-- (Y) node[midway, sloped, scale=0.5] {||}
-- cycle node[midway, sloped, scale=0.5] {||};

% Label Points
\draw (K) node[below left] {K};
\draw (E) node[below right] {E};
\draw (Y) node[above] {Y};
\end{tikzpicture}
"""
    t = EquilateralTriangle(start_vertex=Point(5, 7), name='KEY')
    assert t.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (K) at (5,7);
\coordinate (E) at (6,7);
\coordinate (Y) at (5.5,7.866);

% Draw EquilateralTriangle
\draw[thick] (K)
-- (E) node[midway, sloped, scale=0.5] {||}
-- (Y) node[midway, sloped, scale=0.5] {||}
-- cycle node[midway, sloped, scale=0.5] {||};

% Label Points
\draw (K) node[below left] {K};
\draw (E) node[below right] {E};
\draw (Y) node[above] {Y};
\end{tikzpicture}
"""


def test_drawing_with_labeled_sides():
    """Check drawing the Triangle."""
    t = EquilateralTriangle(name='WAX')
    t.setup_labels(['7.5 cm'])
    assert t.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (W) at (0,0);
\coordinate (A) at (1,0);
\coordinate (X) at (0.5,0.866);

% Draw EquilateralTriangle
\draw[thick] (W)
-- (A) node[midway, sloped, scale=0.5] {||}
-- (X) node[midway, sloped, scale=0.5] {||}
-- cycle node[midway, above, sloped] {7.5 cm} """\
r"""node[midway, sloped, scale=0.5] {||};

% Label Points
\draw (W) node[below left] {W};
\draw (A) node[below right] {A};
\draw (X) node[above] {X};
\end{tikzpicture}
"""
