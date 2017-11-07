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
from decimal import Decimal

from mathmakerlib.calculus.number import Number
from mathmakerlib.geometry.point import Point
from mathmakerlib.geometry.linesegment import LineSegment


@pytest.fixture()
def A():
    return Point('A', 0, 0)


@pytest.fixture()
def B():
    return Point('B', 1, 1)


@pytest.fixture()
def C():
    return Point('C', 2, 2)


@pytest.fixture()
def D():
    return Point('D', 4, 0)


@pytest.fixture()
def E():
    return Point('E', 1, 0)


def test_instanciation_errors(A, B):
    """Check LineSegment's instanciation exceptions."""
    with pytest.raises(TypeError) as excinfo:
        LineSegment('A', B)
    assert str(excinfo.value) == 'Both arguments should be Points, got a ' \
        '<class \'str\'> as first argument instead.'
    with pytest.raises(TypeError) as excinfo:
        LineSegment(A, lambda x: 2 * x)
    assert str(excinfo.value) == 'Both arguments should be Points, got a ' \
        '<class \'function\'> as second argument instead.'
    with pytest.raises(ValueError) as excinfo:
        LineSegment(A, B, '4 cm')
    assert str(excinfo.value) == 'One LineSegment, or two Points are ' \
        'required to create a LineSegment. Got 3 objects instead.'
    with pytest.raises(TypeError) as excinfo:
        LineSegment(A, label='4 cm')
    assert str(excinfo.value) == 'If only one argument is provided, it must ' \
        'be another LineSegment. Got a <class \'tuple\'> instead.'
    with pytest.raises(ValueError) as excinfo:
        LineSegment(B, B)
    assert str(excinfo.value) == 'Cannot instantiate a LineSegment if both ' \
        'endpoints have the same coordinates: (1; 1).'
    s = LineSegment(A, B)
    with pytest.warns(UserWarning) as record:
        LineSegment(s, label='4 cm')
    assert len(record) == 1
    assert str(record[0].message) == 'LineSegment copy: ignoring parameter ' \
        '(label or thickness).'
    with pytest.warns(UserWarning) as record:
        LineSegment(s, thickness='thin')
    assert len(record) == 1
    assert str(record[0].message) == 'LineSegment copy: ignoring parameter ' \
        '(label or thickness).'


def test_instanciation(A, B):
    """Check LineSegment's instanciation."""
    s = LineSegment(A, B)
    assert s.thickness == 'thick'
    assert s.label is None
    assert s.endpoints[0] == A
    assert s.endpoints[1] == B
    t = LineSegment(s)
    assert t.thickness == 'thick'
    assert t.label is None
    assert t.endpoints[0] == A
    assert t.endpoints[1] == B


def test_some_setters(A, B):
    """Check thickness and label_mask setters."""
    s = LineSegment(A, B)
    with pytest.raises(ValueError) as excinfo:
        s.thickness = 'undefined'
    assert str(excinfo.value).startswith('Cannot use \'undefined\' as '
                                         'thickness for a LineSegment. '
                                         'Available values are in: ')
    s.thickness = ''
    assert s.thickness is None
    with pytest.raises(ValueError) as excinfo:
        s.label_mask = 'undefined'
    assert str(excinfo.value).startswith('label_mask must be in '
                                         '[None, \'\', \'?\']; '
                                         'got \'undefined\' instead.')
    s.label_mask = '?'
    assert s.label_mask == '?'


def test_repr(A, B):
    """Check __repr__ is correct."""
    assert repr(LineSegment(A, B)) \
        == 'LineSegment(Point A(0; 0), Point B(1; 1))'


def test_equality(A, B, C):
    """Check __eq__ and __ne__ are correct."""
    s = LineSegment(A, B)
    t = LineSegment(s)
    assert s == t
    assert s != 'AB'
    assert not (s == 9)
    u = LineSegment(B, C)
    assert s != u


def test_length(A, B, D):
    """Check length is correct."""
    t = LineSegment(A, D)
    assert t.length == Number(4)
    s = LineSegment(A, B)
    assert s.length.rounded(Decimal('0.0001')) == Number('1.4142')
    s = LineSegment(B, A)
    assert s.length.rounded(Decimal('0.0001')) == Number('1.4142')


def test_slope(A, B, D):
    """Check length is correct."""
    t = LineSegment(A, D)
    assert t.slope == Number(0)
    s = LineSegment(A, B)
    assert s.slope == Number('45')
    s = LineSegment(B, A)
    assert s.slope == Number('225')
    s = LineSegment(A, Point('B', 0, 1))
    assert s.slope == Number('90')


# def test_midpoint(A, B):
#     """Check midpoint is correct."""
#     s = LineSegment(A, B)
#     assert s.midpoint == Point('M', Number('0.5'), Number('0.5'))


def test_drawing_without_linesegment_labels(A, E):
    """Check drawing is correct."""
    ls = LineSegment(A, E)
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,0);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw LineSegment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[left] {A};
\draw (E) node[right] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, E, draw_endpoints=False)
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,0);

% Draw LineSegment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[left] {A};
\draw (E) node[right] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, E, label_endpoints=False)
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,0);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw LineSegment
\draw[thick] (A) -- (E);

% Label Points

\end{tikzpicture}
"""
    ls = LineSegment(A, Point('E', Number(1), Number(1)))
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,1);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw LineSegment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[below left] {A};
\draw (E) node[above right] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, Point('E', Number(0), Number(1)))
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (0,1);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw LineSegment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[below] {A};
\draw (E) node[above] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, Point('E', Number(-1), Number(1)))
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (-1,1);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw LineSegment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[below right] {A};
\draw (E) node[above left] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, Point('E', Number(-1), Number(0)))
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (-1,0);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw LineSegment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[right] {A};
\draw (E) node[left] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, Point('E', Number(-1), Number(-1)))
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (-1,-1);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw LineSegment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[above right] {A};
\draw (E) node[below left] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, Point('E', Number(0), Number(-1)))
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (0,-1);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw LineSegment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[above] {A};
\draw (E) node[below] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, Point('E', Number(1), Number(-1)))
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,-1);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw LineSegment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[above left] {A};
\draw (E) node[below right] {E};
\end{tikzpicture}
"""


def test_drawing_with_linesegment_labels(A, B, E):
    """Check drawing is correct."""
    ls = LineSegment(A, E, label='4 cm')
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,0);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw LineSegment
\draw[thick] (A) -- (E) node[midway, below, sloped] {4 cm};

% Label Points
\draw (A) node[left] {A};
\draw (E) node[right] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, E, label='4 cm', label_position='above')
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,0);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw LineSegment
\draw[thick] (A) -- (E) node[midway, above, sloped] {4 cm};

% Label Points
\draw (A) node[left] {A};
\draw (E) node[right] {E};
\end{tikzpicture}
"""
    ls = LineSegment(E, A, label='4 cm')
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (E) at (1,0);
\coordinate (A) at (0,0);

% Draw Points
\draw (E) node {$\times$};
\draw (A) node {$\times$};

% Draw LineSegment
\draw[thick] (E) -- (A) node[midway, above, sloped] {4 cm};

% Label Points
\draw (E) node[right] {E};
\draw (A) node[left] {A};
\end{tikzpicture}
"""
    ls = LineSegment(E, B, label='4 cm')
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (E) at (1,0);
\coordinate (B) at (1,1);

% Draw Points
\draw (E) node {$\times$};
\draw (B) node {$\times$};

% Draw LineSegment
\draw[thick] (E) -- (B) node[midway, above, sloped] {4 cm};

% Label Points
\draw (E) node[below] {E};
\draw (B) node[above] {B};
\end{tikzpicture}
"""
    ls = LineSegment(A, E, label='4 cm', label_position='clockwise')
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,0);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw LineSegment
\draw[thick] (A) -- (E) node[midway, above, sloped] {4 cm};

% Label Points
\draw (A) node[left] {A};
\draw (E) node[right] {E};
\end{tikzpicture}
"""
    ls = LineSegment(E, A, label='4 cm', label_position='clockwise')
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (E) at (1,0);
\coordinate (A) at (0,0);

% Draw Points
\draw (E) node {$\times$};
\draw (A) node {$\times$};

% Draw LineSegment
\draw[thick] (E) -- (A) node[midway, below, sloped] {4 cm};

% Label Points
\draw (E) node[right] {E};
\draw (A) node[left] {A};
\end{tikzpicture}
"""
