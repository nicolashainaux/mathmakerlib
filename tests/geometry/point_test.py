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
    assert p.name == 'A'
    assert p.label == 'A'
    p = Point('A', 0, 0, label='?')
    assert p.name == 'A'
    assert p.label == '?'


def test_repr():
    """Check __repr__ is correct."""
    assert repr(Point('A', 0, 0)) == 'Point A(0; 0)'


def test_equality():
    """Check __eq__, __ne__, coordinates are correct."""
    p = Point('A', 0, 0)
    assert p != 'A'
    assert not(p == 0)
    assert p == Point('A', 0, 0, shape=r'$\bullet$')
    assert p != Point('B', 0, 0)
    assert p == Point('A', 0, 0, label='?')
    assert p.coordinates == Point('B', 0, 0).coordinates


def test_drawing():
    """Check drawing is correct."""
    p = Point('A', 0, 0)
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Point
\coordinate (A) at (0,0);

% Draw Point
\draw (A) node {$\times$};

% Label Point
\draw (A) node[below] {A};
\end{tikzpicture}
"""
    p.label_position = None
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Point
\coordinate (A) at (0,0);

% Draw Point
\draw (A) node {$\times$};

% Label Point
\draw (A) node {A};
\end{tikzpicture}
"""
    p.label = ''
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Point
\coordinate (A) at (0,0);

% Draw Point
\draw (A) node {$\times$};

% Label Point

\end{tikzpicture}
"""
    p.label = None
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Point
\coordinate (A) at (0,0);

% Draw Point
\draw (A) node {$\times$};

% Label Point

\end{tikzpicture}
"""
