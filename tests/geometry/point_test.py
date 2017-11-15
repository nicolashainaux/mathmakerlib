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

from mathmakerlib.geometry import Point


def test_instanciation_errors():
    """Check Point's instanciation exceptions."""
    with pytest.raises(TypeError) as excinfo:
        Point('A', 0, 0)
    assert str(excinfo.value) == 'Expected a number as abscissa, ' \
        'got \'A\' instead.'
    with pytest.raises(TypeError) as excinfo:
        Point(0, 'A', 0)
    assert str(excinfo.value) == 'Expected a number as ordinate, ' \
        'got \'A\' instead.'


def test_instanciation():
    """Check Point's instanciation."""
    p = Point(0, 0, 'A')
    assert p.x == p.y == 0
    assert p.name == 'A'
    assert p.label == 'A'
    p = Point(0, 0, 'A', label='?')
    assert p.name == 'A'
    assert p.label == '?'


def test_automatic_naming():
    """Check automatic naming of Points."""
    Point.reset_names()
    Point(0, 0, 'A')
    q = Point(1, 1)
    assert q.name == 'B'
    Point.reset_names()
    q = Point(1, 1)
    assert q.name == 'A'
    q = Point(1, 1, 'C')
    q = Point(1, 1)
    assert q.name == 'B'
    q = Point(1, 1)
    assert q.name == 'D'
    for _ in range(23):
        q = Point(1, 1)
    assert q.name == 'A$_1$'
    for _ in range(26):
        q = Point(1, 1)
    assert q.name == 'A$_2$'
    Point.reset_names()
    p = Point(1, 1)  # 'A'
    q = Point(1, 1)  # 'B'
    p.name = 'C'  # 'A' is free
    q = Point(1, 1)
    assert q.name == 'A'
    q = Point(1, 1)
    assert q.name == 'D'


def test_repr():
    """Check __repr__ is correct."""
    assert repr(Point(0, 0, 'A')) == 'Point A(0; 0)'


def test_equality():
    """Check __eq__, __ne__, coordinates are correct."""
    p = Point(0, 0, 'A')
    assert p != 'A'
    assert not(p == 0)
    assert p == Point(0, 0, 'A', shape=r'$\bullet$')
    assert p != Point(0, 0, 'B')
    assert p == Point(0, 0, 'A', label='?')
    assert p.coordinates == Point(0, 0, 'B').coordinates


def test_drawing():
    """Check drawing is correct."""
    p = Point(0, 0, 'A')
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
    p = Point(0, 0, 'A', color='pink')
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Point
\coordinate (A) at (0,0);

% Draw Point
\draw[pink] (A) node {$\times$};

% Label Point
\draw (A) node[below] {A};
\end{tikzpicture}
"""
    p = Point(0, 0, 'A')
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
