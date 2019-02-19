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

import pytest
from decimal import Decimal

from mathmakerlib.exceptions import ZeroLengthLineSegment
from mathmakerlib.core.drawable import THICKNESS_VALUES
from mathmakerlib.config import DASHPATTERN_VALUES
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


@pytest.fixture()
def J():
    return Point(0, 1, 'J')


def test_instanciation_errors(A, B):
    """Check LineSegment's instanciation exceptions."""
    with pytest.raises(TypeError) as excinfo:
        LineSegment('A', B)
    assert str(excinfo.value) == 'First argument must be a Point, found '\
        '\'A\' instead.'
    with pytest.raises(TypeError) as excinfo:
        LineSegment(A, 'B')
    assert str(excinfo.value) == 'Second argument must be a Point or a '\
        'Vector, found \'B\' instead.'
    with pytest.raises(TypeError) as excinfo:
        LineSegment(A, B, '4 cm')
    assert str(excinfo.value) == 'Two Points are ' \
        'required to create a LineSegment. Got 3 object(s) instead.'
    with pytest.raises(TypeError) as excinfo:
        LineSegment(A, label='4 cm')
    assert str(excinfo.value) == 'Two Points are ' \
        'required to create a LineSegment. Got 1 object(s) instead.'
    with pytest.raises(ZeroLengthLineSegment) as excinfo:
        LineSegment(B, B, allow_zero_length=False)
    assert str(excinfo.value) == 'Explicitly disallowed creation of a '\
        'zero-length LineSegment.'
    with pytest.raises(ValueError) as excinfo:
        LineSegment(A, B, draw_endpoints='undefined')
    assert str(excinfo.value) == 'draw_endpoints must be True or False; ' \
        'got \'undefined\' instead.'
    with pytest.raises(ValueError) as excinfo:
        LineSegment(A, B, sloped_label='undefined')
    assert str(excinfo.value) == 'sloped_label must be True or False; ' \
        'got \'undefined\' instead.'
    with pytest.raises(ValueError) as excinfo:
        LineSegment(A, B, label_endpoints='undefined')
    assert str(excinfo.value) == 'label_endpoints must be True or False; ' \
        'got \'undefined\' instead.'
    ls = LineSegment(B, B)
    with pytest.raises(ZeroLengthLineSegment) as excinfo:
        ls.slope
    assert str(excinfo.value) == 'Cannot calculate the slope of a '\
        'zero-length LineSegment.'
    with pytest.raises(ZeroLengthLineSegment) as excinfo:
        ls.slope360
    assert str(excinfo.value) == 'Cannot calculate the slope of a '\
        'zero-length LineSegment.'


def test_instanciation(A, B):
    """Check LineSegment's instanciation."""
    s = LineSegment(A, B)
    assert s.thickness == 'thick'
    assert s.label is None
    assert s.endpoints[0] == A
    assert s.endpoints[1] == B
    assert s.Δx == 1
    assert s.Δy == 1
    assert s.Δz == 0


def test_some_setters(A, B):
    """Check thickness and label_mask setters."""
    s = LineSegment(A, B)
    with pytest.raises(ValueError) as excinfo:
        s.thickness = 'undefined'
    assert str(excinfo.value) == 'Incorrect thickness value: \'undefined\'. ' \
        'Available values belong to: {}.'.format(THICKNESS_VALUES)
    with pytest.raises(ValueError) as excinfo:
        s.label_winding = 'undefined'
    assert str(excinfo.value) == "label_winding must be 'clockwise' or " \
        "'anticlockwise'; found 'undefined' instead."
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
    with pytest.raises(TypeError) as excinfo:
        s = LineSegment(A, B, locked_label=1)
    assert str(excinfo.value) == 'Expected bool type for \'locked_label\' '\
        'keyword argument. Found <class \'int\'>.'
    s = LineSegment(A, B, locked_label=True)
    with pytest.raises(TypeError) as excinfo:
        s.label = '4.5 cm'
    assert str(excinfo.value) == 'This LineSegments\' label is locked. '\
        'If you\'re using this LineSegment embedded in another '\
        'object (e.g. a Polygon), please use the setup_labels() method of '\
        'this object. Otherwise, first explicitely unlock the LineSegment.'


def test_dashpattern(A, B):
    """Check dashpattern property."""
    s = LineSegment(A, B)
    assert s.dashpattern == 'solid'
    with pytest.raises(ValueError) as excinfo:
        s.dashpattern = 'undefined'
    assert str(excinfo.value) == 'Incorrect dashpattern value: '\
        '\'undefined\'. Available values belong to: {}.'\
        .format(DASHPATTERN_VALUES)


def test_repr(A, B):
    """Check __repr__ is correct."""
    assert repr(LineSegment(A, B)) \
        == 'LineSegment(Point A(0, 0), Point B(1, 1))'


def test_hash():
    """Check __hash__."""
    assert hash(LineSegment(Point(0, 0, 'A'), Point(1, 1, 'B')))\
        != hash(LineSegment(Point(0, 0, 0, 'A'), Point(1, 1, 1, 'B')))


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


def test_slope(A, B, D, E, J):
    """Check slope is correct."""
    s = LineSegment(A, D)
    assert s.slope360 == Number(0)
    assert s.slope == Number(0)
    s = LineSegment(A, B)
    assert s.slope360 == Number('45')
    assert s.slope == Number('45')
    s = LineSegment(A, Point(0, 1, 'B'))
    assert s.slope360 == Number('90')
    assert s.slope == Number('90')
    s = LineSegment(A, J)
    assert s.slope360 == Number('90')
    assert s.slope == Number('90')
    s = LineSegment(J, A)
    assert s.slope360 == Number('270')
    assert s.slope == Number('-90')
    s = LineSegment(B, A)
    assert s.slope360 == Number('225')
    assert s.slope == Number('-135')


def test_midpoint():
    """Check midpoint is correct."""
    s = LineSegment(Point(0, 0, 'A'), Point(1, 1, 'B'))
    assert s.midpoint() == Point(Number('0.5'), Number('0.5'))


def test_point_at():
    """Check point_at is correct."""
    s = LineSegment(Point(0, 0, 'A'), Point(1, 1, 'B'))
    with pytest.raises(TypeError) as excinfo:
        s.point_at('a')
    assert str(excinfo.value) == 'position must be a number, found ' \
        '<class \'str\'> instead.'
    assert s.point_at(Number('0.5')) == s.midpoint()
    assert s.point_at(Number('0.75')) == Point('0.75', '0.75')
    assert s.point_at(Number(2)) == Point(2, 2)
    assert s.point_at(0) == Point(0, 0)
    assert s.point_at(1) == Point(1, 1)
    assert s.point_at(-2) == Point(-2, -2)
    s = LineSegment(Point(1, 1, 'A'), Point(3, 4, 'B'))
    assert s.point_at(Number('0.8')) == Point('2.6', '3.4')
    assert s.point_at(2) == Point(5, 7)
    assert s.point_at(Number('0.5')) == s.midpoint()


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


def test_draw_dashpattern(A, E):
    """Check drawing is correct."""
    ls = LineSegment(A, E, dashpattern='dashed')
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,0);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick, dashed] (A) -- (E);

% Label Points
\draw (A) node[left] {A};
\draw (E) node[right] {E};
\end{tikzpicture}
"""


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
    ls.label = Number(6, unit='cm')
    assert ls.label == r'\SI{6}{cm}'
    assert ls.label_value == Number(6, unit='cm')
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,0);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E) node[midway, below, sloped] {\SI{6}{cm}};

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
\draw[thick] (E) -- (B) node[midway, below, sloped] {4 cm};

% Label Points
\draw (E) node[below] {E};
\draw (B) node[above] {B};
\end{tikzpicture}
"""
    ls = LineSegment(A, E, label='4 cm', label_winding='clockwise')
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
    ls = LineSegment(E, A, label='4 cm', label_winding='clockwise')
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
                     label_winding='clockwise')
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
    ls = LineSegment(E, A, label='4 cm', label_winding='clockwise',
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
    ls = LineSegment(E, A, label='4 cm', label_winding='clockwise',
                     label_scale='0.67')
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (E) at (1,0);
\coordinate (A) at (0,0);

% Draw Points
\draw (E) node[scale=0.67] {$\times$};
\draw (A) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (E) -- (A) node[midway, below, sloped, scale=0.67] {4 cm};

% Label Points
\draw (E) node[right] {E};
\draw (A) node[left] {A};
\end{tikzpicture}
"""


def test_drawing_with_linesegment_not_sloped_labels():
    """Check drawing is correct."""
    A = Point(0, 0, 'A')
    B = Point(1, 0, 'B')
    ls = LineSegment(A, B, label='4 cm')
    ls.sloped_label = False
    ls.label_position = 'automatic'
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (B) at (1,0);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (B) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (B) node[midway, below] {4 cm};

% Label Points
\draw (A) node[left] {A};
\draw (B) node[right] {B};
\end{tikzpicture}
"""
    B = Point(1, 1, 'B')
    ls = LineSegment(A, B, label='4 cm')
    ls.sloped_label = False
    ls.label_position = 'automatic'
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (B) at (1,1);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (B) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (B) node[midway, below right] {4 cm};

% Label Points
\draw (A) node[below left] {A};
\draw (B) node[above right] {B};
\end{tikzpicture}
"""
    ls.label_position = 'above left'
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (B) at (1,1);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (B) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (B) node[midway, above left] {4 cm};

% Label Points
\draw (A) node[below left] {A};
\draw (B) node[above right] {B};
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
\draw[thick] (A) -- (F) node[midway, sloped, scale=0.5] {//};

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
                        r"""node[midway, sloped, scale=0.5] {//};

% Label Points
\draw (A) node[left] {A};
\draw (F) node[right] {F};
\end{tikzpicture}
""")
