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

from mathmakerlib.core.drawable import THICKNESS_VALUES
from mathmakerlib.calculus import Number
from mathmakerlib.geometry import Point, LineSegment


@pytest.fixture()
def A():
    return Point(0, 0, 'A')


@pytest.fixture()
def B():
    return Point(1, 1, 'B')


@pytest.fixture()
def C():
    return Point(2, 2, 'C')


@pytest.fixture()
def D():
    return Point(4, 0, 'D')


@pytest.fixture()
def E():
    return Point(1, 0, 'E')


@pytest.fixture()
def F():
    return Point(4, 0, 'F')


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
    with pytest.raises(TypeError) as excinfo:
        LineSegment(A, B, '4 cm')
    assert str(excinfo.value) == 'Two Points are ' \
        'required to create a LineSegment. Got 3 object(s) instead.'
    with pytest.raises(TypeError) as excinfo:
        LineSegment(A, label='4 cm')
    assert str(excinfo.value) == 'Two Points are ' \
        'required to create a LineSegment. Got 1 object(s) instead.'
    with pytest.raises(ValueError) as excinfo:
        LineSegment(B, B)
    assert str(excinfo.value) == 'Cannot instantiate any PointsPair if both ' \
        'endpoints have the same coordinates: (1; 1).'
    with pytest.raises(ValueError) as excinfo:
        LineSegment(A, B, draw_endpoints='undefined')
    assert str(excinfo.value) == 'draw_endpoints must be True or False; ' \
        'got \'undefined\' instead.'
    with pytest.raises(ValueError) as excinfo:
        LineSegment(A, B, label_endpoints='undefined')
    assert str(excinfo.value) == 'label_endpoints must be True or False; ' \
        'got \'undefined\' instead.'


def test_instanciation(A, B):
    """Check LineSegment's instanciation."""
    s = LineSegment(A, B)
    assert s.thickness == 'thick'
    assert s.label is None
    assert s.endpoints[0] == A
    assert s.endpoints[1] == B


def test_some_setters(A, B):
    """Check thickness and label_mask setters."""
    s = LineSegment(A, B)
    with pytest.raises(ValueError) as excinfo:
        s.thickness = 'undefined'
    assert str(excinfo.value) == 'Incorrect thickness value: \'undefined\'. ' \
        'Available values belong to: {}.'.format(THICKNESS_VALUES)
    with pytest.raises(ValueError) as excinfo:
        s.label_mask = 'undefined'
    assert str(excinfo.value).startswith('label_mask must be in '
                                         '[None, \' \', \'?\']; '
                                         'got \'undefined\' instead.')
    s.label_mask = '?'
    assert s.label_mask == '?'
    with pytest.raises(TypeError) as excinfo:
        s.mark_scale = 'undefined'
    assert str(excinfo.value).startswith('The LineSegment\'s mark\'s scale '
                                         'must be a number.')


def test_repr(A, B):
    """Check __repr__ is correct."""
    assert repr(LineSegment(A, B)) \
        == 'LineSegment(Point A(0; 0), Point B(1; 1))'


def test_equality(A, B, C):
    """Check __eq__ and __ne__ are correct."""
    s = LineSegment(A, B)
    t = LineSegment(A, B)
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
    s = LineSegment(A, Point(0, 1, 'B'))
    assert s.slope == Number('90')


def test_midpoint():
    """Check midpoint is correct."""
    Point.reset_names()
    s = LineSegment(Point(0, 0, 'A'), Point(1, 1, 'B'))
    assert s.midpoint() == Point(Number('0.5'), Number('0.5'), 'C')
    s = LineSegment(Point(0, 0, 'A'), Point(1, 1, 'B'))
    assert s.midpoint(name='M') == Point(Number('0.5'), Number('0.5'), 'M')


def test_dividing_points_errors(A, B):
    """Check LineSegment's instanciation exceptions."""
    AB = LineSegment(Point(0, 0, 'A'), Point(5, 0, 'B'))
    with pytest.raises(TypeError) as excinfo:
        AB.dividing_points(n=7.5)
    assert str(excinfo.value) == 'n must be an integer'


def test_dividing_points():
    """Check Points dividing LineSegment."""
    AB = LineSegment(Point(0, 0, 'A'), Point(5, 0, 'B'))
    p = AB.dividing_points(n=4)
    assert p == [Point(Number('1.25'), 0, 'a1'),
                 Point(Number('2.5'), 0, 'a2'),
                 Point(Number('3.75'), 0, 'a3')]
    AB = LineSegment(Point(0, 0, 'A'), Point(0, 5, 'B'))
    p = AB.dividing_points(n=4)
    assert p == [Point(0, Number('1.25'), 'a1'),
                 Point(0, Number('2.5'), 'a2'),
                 Point(0, Number('3.75'), 'a3')]
    AB = LineSegment(Point(0, 0, 'A'), Point(5, 5, 'B'))
    p = AB.dividing_points(n=4)
    assert p == [Point(Number('1.25'), Number('1.25'), 'a1'),
                 Point(Number('2.5'), Number('2.5'), 'a2'),
                 Point(Number('3.75'), Number('3.75'), 'a3')]
    p = AB.dividing_points(n=1)
    assert p == []
    with pytest.raises(TypeError):
        p = AB.dividing_points(n='4')
    with pytest.raises(ValueError):
        p = AB.dividing_points(n=0)


def test_drawing_without_linesegment_labels(A, E):
    """Check drawing is correct."""
    ls = LineSegment(A, E)
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,0);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[left] {A};
\draw (E) node[right] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, E, color='Apricot')
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,0);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick, Apricot] (A) -- (E);

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

% Draw Line Segment
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
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E);

% Label Points

\end{tikzpicture}
"""
    ls = LineSegment(A, Point(Number(1), Number(1), 'E'))
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,1);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[below left] {A};
\draw (E) node[above right] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, Point(Number(0), Number(1), 'E'))
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (0,1);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[below] {A};
\draw (E) node[above] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, Point(Number(-1), Number(1), 'E'))
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (-1,1);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[below right] {A};
\draw (E) node[above left] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, Point(Number(-1), Number(0), 'E'))
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (-1,0);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[right] {A};
\draw (E) node[left] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, Point(Number(-1), Number(-1), 'E'))
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (-1,-1);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[above right] {A};
\draw (E) node[below left] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, Point(Number(0), Number(-1), 'E'))
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (0,-1);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[above] {A};
\draw (E) node[below] {E};
\end{tikzpicture}
"""
    ls = LineSegment(A, Point(Number(1), Number(-1), 'E'))
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,-1);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
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
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
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
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
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
\draw (E) node[scale=0.67] {$\times$};
\draw (A) node[scale=0.67] {$\times$};

% Draw Line Segment
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
\draw (E) node[scale=0.67] {$\times$};
\draw (B) node[scale=0.67] {$\times$};

% Draw Line Segment
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
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
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
\draw (E) node[scale=0.67] {$\times$};
\draw (A) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (E) -- (A) node[midway, below, sloped] {4 cm};

% Label Points
\draw (E) node[right] {E};
\draw (A) node[left] {A};
\end{tikzpicture}
"""
    ls = LineSegment(E, A, label='4 cm', thickness=None,
                     label_position='clockwise')
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (E) at (1,0);
\coordinate (A) at (0,0);

% Draw Points
\draw (E) node[scale=0.67] {$\times$};
\draw (A) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw (E) -- (A) node[midway, below, sloped] {4 cm};

% Label Points
\draw (E) node[right] {E};
\draw (A) node[left] {A};
\end{tikzpicture}
"""
    ls = LineSegment(E, A, label='4 cm', label_position='clockwise',
                     label_mask='?')
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (E) at (1,0);
\coordinate (A) at (0,0);

% Draw Points
\draw (E) node[scale=0.67] {$\times$};
\draw (A) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (E) -- (A) node[midway, below, sloped] {?};

% Label Points
\draw (E) node[right] {E};
\draw (A) node[left] {A};
\end{tikzpicture}
"""


def test_drawing_marked_linesegment(A, F):
    """Check drawing is correct."""
    ls = LineSegment(A, F, mark='//')
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (F) at (4,0);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (F) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (F) node[midway, sloped, scale=0.67] {//};

% Label Points
\draw (A) node[left] {A};
\draw (F) node[right] {F};
\end{tikzpicture}
"""
    ls.label = '4 cm'
    assert ls.drawn == (r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (F) at (4,0);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (F) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (F) node[midway, below, sloped] {4 cm} """
                        r"""node[midway, sloped, scale=0.67] {//};

% Label Points
\draw (A) node[left] {A};
\draw (F) node[right] {F};
\end{tikzpicture}
""")
