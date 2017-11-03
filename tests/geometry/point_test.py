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

from mathmakerlib.geometry.point import Point


def test_instanciation():
    """Check Point's instanciation."""
    p = Point('A', 0, 0)
    assert Point(p) == p
    assert p.x == p.y == 0
    assert p.label == 'A'


def test_repr():
    """Check __repr__ is correct."""
    assert repr(Point('A', 0, 0)) == 'Point A(0; 0)'


def test_equality():
    """Check __eq__ and __ne__ are correct."""
    assert Point('A', 0, 0) == Point('A', 0, 0, shape=r'$\bullet$')
    assert Point('A', 0, 0) != Point('B', 0, 0)


def test_drawing():
    """Check drawing is correct."""
    p = Point('A', 0, 0)
    assert p.drawn == r"""
\begin{tikzpicture}
\coordinate (A) at (0,0);
\draw (A) node {$\times$};
\draw (A) node[below] {A};
\end{tikzpicture}
"""
    assert p.draw(label_position='above') == r"""
\begin{tikzpicture}
\coordinate (A) at (0,0);
\draw (A) node {$\times$};
\draw (A) node[above] {A};
\end{tikzpicture}
"""
    p.label_position = None
    assert p.drawn == r"""
\begin{tikzpicture}
\coordinate (A) at (0,0);
\draw (A) node {$\times$};
\draw (A) node {A};
\end{tikzpicture}
"""
