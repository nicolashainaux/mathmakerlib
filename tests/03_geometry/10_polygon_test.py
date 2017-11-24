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

from mathmakerlib import required
from mathmakerlib.calculus import Number  # , Unit
from mathmakerlib.geometry import Point, Polygon, AngleMark


@pytest.fixture()
def pointO():
    return Point(0, 0, 'O')


@pytest.fixture()
def pointI():
    return Point(1, 0, 'I')


@pytest.fixture()
def pointJ():
    return Point(0, 1, 'J')


@pytest.fixture()
def pointA():
    return Point(4, 0, 'A')


@pytest.fixture()
def pointB():
    return Point(3, 2, 'B')


@pytest.fixture()
def pointC():
    return Point(1, 3, 'C')


def test_instanciation_errors(pointO, pointI, pointJ):
    """Check Polygon's instanciation exceptions."""
    with pytest.raises(ValueError) as excinfo:
        Polygon(pointO, pointI)
    assert str(excinfo.value) == 'At least three Points are required to be ' \
        'able to build a Polygon. Got only 2 positional arguments, though.'
    with pytest.raises(TypeError) as excinfo:
        Polygon(pointO, pointI, pointJ, rotation_angle='alpha')
    assert str(excinfo.value) == 'Expected a number as rotation angle, got '\
        'a <class \'str\'> instead.'
    with pytest.raises(ValueError) as excinfo:
        Polygon(pointO, pointI, pointJ, name='ABCD')
    assert str(excinfo.value) == 'The number of provided vertices (3) ' \
        'does not match the number of Points\' names (4).'
    with pytest.raises(TypeError) as excinfo:
        Polygon(pointO, pointI, 3, name='ABCD')
    assert str(excinfo.value) == 'Only Points must be provided in order to ' \
        'build a Polygon. Got a <class \'int\'> as positional argument #2.'
    with pytest.raises(TypeError) as excinfo:
        Polygon(pointO, pointI, pointJ, draw_vertices=1)
    assert str(excinfo.value) == 'draw_vertices must be a boolean; ' \
        'got <class \'int\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Polygon(pointO, pointI, pointJ, label_vertices=0)
    assert str(excinfo.value) == 'label_vertices must be a boolean; ' \
        'got <class \'int\'> instead.'


def test_instanciation(pointO, pointA, pointB, pointC):
    """Check Polygon's instanciation."""
    p = Polygon(pointO, pointA, pointB, pointC)
    assert p.thickness == 'thick'
    assert p.color is None
    assert not p.draw_vertices
    assert p.label_vertices
    assert p.type == 'Quadrilateral'
    assert p.name == 'OABC'
    assert repr(p) == 'Quadrilateral OABC'
    assert p.isobarycenter().same_as(Point(2, Number('1.25')))
    p = Polygon(pointO, pointA, pointB, pointC, name='YOGA')
    assert p.name == 'YOGA'
    assert p.vertices[0].label_position == 'below left'
    assert p.vertices[1].label_position == 'below right'
    assert p.vertices[2].label_position == 'above right'
    assert p.vertices[3].label_position == 'above left'


def test_simple_drawing(pointO, pointA, pointB, pointC):
    """Check drawing the Polygon."""
    p = Polygon(pointO, pointA, pointB, pointC)
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Polygon
\draw[thick] (O)
-- (A)
-- (B)
-- (C)
-- cycle;

% Label Points
\draw (O) node[below left] {O};
\draw (A) node[below right] {A};
\draw (B) node[above right] {B};
\draw (C) node[above left] {C};
\end{tikzpicture}
"""
    p.color = 'red'
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Polygon
\draw[thick, red] (O)
-- (A)
-- (B)
-- (C)
-- cycle;

% Label Points
\draw (O) node[below left] {O};
\draw (A) node[below right] {A};
\draw (B) node[above right] {B};
\draw (C) node[above left] {C};
\end{tikzpicture}
"""
    p.color = None
    p.draw_vertices = True
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Vertices
\draw (O) node[scale=0.67] {$\times$};
\draw (A) node[scale=0.67] {$\times$};
\draw (B) node[scale=0.67] {$\times$};
\draw (C) node[scale=0.67] {$\times$};

% Draw Polygon
\draw[thick] (O)
-- (A)
-- (B)
-- (C)
-- cycle;

% Label Points
\draw (O) node[below left] {O};
\draw (A) node[below right] {A};
\draw (B) node[above right] {B};
\draw (C) node[above left] {C};
\end{tikzpicture}
"""
    p.draw_vertices = False
    p.label_vertices = False
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Polygon
\draw[thick] (O)
-- (A)
-- (B)
-- (C)
-- cycle;

% Label Points

\end{tikzpicture}
"""


def test_drawing_with_labeled_sides(pointO, pointA, pointB, pointC):
    """Check drawing the Polygon."""
    p = Polygon(pointO, pointA, pointB, pointC)
    p.label_vertices = False
    p.sides[1].label = '3 cm'
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Polygon
\draw[thick] (O)
-- (A)
-- (B) node[midway, above, sloped] {3 cm}
-- (C)
-- cycle;

% Label Points

\end{tikzpicture}
"""
    p.sides[0].label = '? cm'
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Polygon
\draw[thick] (O)
-- (A) node[midway, below, sloped] {? cm}
-- (B) node[midway, above, sloped] {3 cm}
-- (C)
-- cycle;

% Label Points

\end{tikzpicture}
"""
    p.sides[3].label = '5 cm'
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Polygon
\draw[thick] (O)
-- (A) node[midway, below, sloped] {? cm}
-- (B) node[midway, above, sloped] {3 cm}
-- (C)
-- cycle node[midway, above, sloped] {5 cm};

% Label Points

\end{tikzpicture}
"""


def test_drawing_with_marked_sides(pointO, pointA, pointB, pointC):
    """Check drawing a Polygon having some marked sides."""
    p = Polygon(pointO, pointA, pointB, pointC)
    p.sides[0].mark = '//'
    p.label_vertices = False
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Polygon
\draw[thick] (O)
-- (A) node[midway, sloped, scale=0.67] {//}
-- (B)
-- (C)
-- cycle;

% Label Points

\end{tikzpicture}
"""
    p.sides[3].mark = '//'
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Polygon
\draw[thick] (O)
-- (A) node[midway, sloped, scale=0.67] {//}
-- (B)
-- (C)
-- cycle node[midway, sloped, scale=0.67] {//};

% Label Points

\end{tikzpicture}
"""


def test_drawing_with_marked_angles(pointO, pointA, pointB, pointC, pointJ):
    """Check drawing a Polygon having some marked angles."""
    p = Polygon(pointO, pointA, pointB, pointC)
    p.label_vertices = False
    p.angles[1].mark = AngleMark()
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Polygon
\draw[thick] (O)
-- (A)
-- (B)
-- (C)
-- cycle
pic [draw, thick, angle radius = 0.25 cm] {angle = B--A--O};

% Label Points

\end{tikzpicture}
"""
    p.angles[2].mark = AngleMark(color='red', thickness='thin',
                                 radius=Number(8, unit='mm'))
    assert p.drawn == \
        r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Polygon
\draw[thick] (O)
-- (A)
-- (B)
-- (C)
-- cycle
pic [draw, thick, angle radius = 0.25 cm] {angle = B--A--O}
pic [draw, red, thin, angle radius = 8 mm] {angle = C--B--A};

% Label Points

\end{tikzpicture}
"""
    required.tikz_library['angles'] = False
    required.hack['rightangle_mark'] = False
    p = Polygon(pointO, pointA, pointB, pointJ)
    p.label_vertices = False
    p.angles[0].mark = AngleMark()
    p.angles[0].mark_right = True
    assert p.drawn == \
        r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (J) at (0,1);

% Draw Polygon
\draw[thick] (O)
-- (A)
-- (B)
-- (J)
-- cycle
pic [draw, thick, angle radius = 0.25 cm] {squared angle = A--O--J};

% Label Points

\end{tikzpicture}
"""
    assert required.tikz_library['angles']
    assert required.hack['rightangle_mark']
