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

from mathmakerlib.calculus import Number
from mathmakerlib.geometry import IsoscelesTriangle


def test_instanciation():
    """Check IsoscelesTriangle's instanciation."""
    t = IsoscelesTriangle()
    assert t.type == 'IsoscelesTriangle'
    assert t.base_length == Number('1.5')
    assert t.equal_legs_length == Number('1')
    assert t.sides[1].mark == '||'
    assert t.sides[2].mark == '||'


def test_simple_drawing():
    """Check drawing the Triangle."""
    t = IsoscelesTriangle(name='GUM')
    assert t.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (G) at (0,0);
\coordinate (U) at (1.5,0);
\coordinate (M) at (0.75,0.661);

% Draw IsoscelesTriangle
\draw[thick] (G)
-- (U)
-- (M) node[midway, sloped, scale=0.5] {||}
-- cycle node[midway, sloped, scale=0.5] {||};

% Label Points
\draw (G) node[left] {G};
\draw (U) node[right] {U};
\draw (M) node[above] {M};
\end{tikzpicture}
"""


def test_drawing_with_labeled_sides():
    """Check drawing the Triangle."""
    t = IsoscelesTriangle(name='GUM')
    assert t.winding == 'anticlockwise'
    t.setup_labels(['1.5 cm', '1 cm'])
    assert t.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (G) at (0,0);
\coordinate (U) at (1.5,0);
\coordinate (M) at (0.75,0.661);

% Draw IsoscelesTriangle
\draw[thick] (G)
-- (U) node[midway, below, sloped] {1.5 cm}
-- (M) node[midway, sloped, scale=0.5] {||}
-- cycle node[midway, above, sloped] {1 cm} """\
r"""node[midway, sloped, scale=0.5] {||};

% Label Points
\draw (G) node[left] {G};
\draw (U) node[right] {U};
\draw (M) node[above] {M};
\end{tikzpicture}
"""
    t = IsoscelesTriangle(name='GUM', winding='clockwise')
    assert t.winding == 'clockwise'
    t.setup_labels(['1.5 cm', '1 cm'])
    assert t.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (G) at (1.5,0);
\coordinate (U) at (0,0);
\coordinate (M) at (0.75,0.661);

% Draw IsoscelesTriangle
\draw[thick] (G)
-- (U) node[midway, below, sloped] {1.5 cm}
-- (M) node[midway, above, sloped] {1 cm} node[midway, sloped, scale=0.5] {||}
-- cycle """\
r"""node[midway, sloped, scale=0.5] {||};

% Label Points
\draw (G) node[right] {G};
\draw (U) node[left] {U};
\draw (M) node[above] {M};
\end{tikzpicture}
"""
