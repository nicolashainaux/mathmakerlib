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

import locale
import pytest

from mathmakerlib import required, config
from mathmakerlib.calculus import Number
from mathmakerlib.geometry import Point, Polygon, AngleDecoration
from mathmakerlib.geometry import shoelace_formula
from mathmakerlib.constants import LOCALE_US, LOCALE_FR


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


def test_shoelace_formula():
    """Check shoelace formula results."""
    assert shoelace_formula(Point(0, 0), Point(2, 0), Point(2, 1)) == 1
    assert shoelace_formula(Point(-3, 0), Point(-1, 0), Point(-1, 1)) == 1
    assert shoelace_formula(Point(3, 4), Point(5, 11), Point(12, 8),
                            Point(9, 5), Point(5, 6)) == -30


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
    with pytest.raises(TypeError) as excinfo:
        Polygon(pointO, pointI, pointJ, do_cycle=0)
    assert str(excinfo.value) == 'do_cycle must be a boolean; ' \
        'got <class \'int\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Polygon(pointO, pointI, pointJ, sloped_sides_labels=0)
    assert str(excinfo.value) == 'sloped_sides_labels must be a boolean; ' \
        'got <class \'int\'> instead.'


def test_instanciation(pointO, pointA, pointB, pointC):
    """Check Polygon's instanciation."""
    p = Polygon(pointO, pointA, pointB, pointC)
    assert p.thickness == 'thick'
    assert p.color is None
    assert not p.draw_vertices
    assert p.label_vertices
    assert p.sloped_sides_labels
    assert p.type == 'Quadrilateral'
    assert p.name == 'OABC'
    assert repr(p) == 'Quadrilateral OABC'
    pointA.label = 'U'
    p = Polygon(pointO, pointA, pointB, pointC, name='YOGA')
    assert p.name == 'YOGA'
    assert p.vertices[0].label == 'Y'
    assert p.vertices[1].label == 'U'
    assert p.vertices[2].label == 'G'
    assert p.vertices[3].label == 'A'
    assert p.vertices[0].label_position == 'below left'
    assert p.vertices[1].label_position == 'below right'
    assert p.vertices[2].label_position == 'above right'
    assert p.vertices[3].label_position == 'above left'
    q = Polygon(pointO, Point(0, 1), Point(Number('1.96'), Number('0.29')),
                Point(Number('2.78'), Number('0.86')),
                Point(Number('3.41'), Number('1.64')),
                Point(Number('3.77'), Number('2.57')),
                Point(Number('3.85'), Number('3.57')),
                Point(Number('3.62'), Number('4.54')),
                Point(Number('3.12'), Number('5.41')),
                Point(Number('2.39'), Number('6.09')),
                Point(Number('1.49'), Number('6.52')),
                Point(Number('0.5'), Number('6.67')),
                Point(Number('-0.49'), Number('6.52')),
                Point(Number('-1.39'), Number('6.09')),
                Point(Number('-2.12'), Number('5.41')),
                Point(Number('-2.62'), Number('4.54')),
                Point(Number('-2.85'), Number('3.57')),
                Point(Number('-2.77'), Number('2.57')),
                Point(Number('-2.41'), Number('1.64')),
                Point(Number('-1.78'), Number('0.86')),
                Point(Number('-0.96'), Number('0.29')))
    assert q.type == '21-sided Polygon'
    q = Polygon(pointO, Point(4, 0), Point(4, 2), Point(0, 2),
                rotation_angle=90)
    assert q.vertices[0] == Point(3, -1)
    assert q.vertices[1] == Point(3, 3)
    assert q.vertices[2] == Point(1, 3)
    assert q.vertices[3] == Point(1, -1)


def test_isobarycenter2D(pointO, pointA, pointB, pointC):
    """Check isobarycenter for 2D Polygons."""
    p = Polygon(pointO, pointA, pointB, pointC)
    assert p.isobarycenter() == Point(2, Number('1.25'))


def test_isobarycenter3D():
    """Check isobarycenter for 3D Polygons."""
    p = Polygon(Point(0, 0, 0), Point(0, 1, 0),
                Point(0, 1, 1), Point(0, 0, 1))
    assert p.isobarycenter() == Point(0, 0.5, 0.5)


def test_equality(pointO, pointA, pointB, pointC):
    p = Polygon(pointO, pointA, pointB, pointC)
    q = Polygon(pointA, pointB, pointC, pointO)
    assert p == q
    q = Polygon(pointC, pointA, pointB, pointO)
    assert p != q
    q = Polygon(pointC, pointB, pointA, pointO)
    assert p == q


def test_sides_labeling(pointO, pointA, pointB, pointC):
    """Check Polygon's sides' labeling."""
    p = Polygon(pointO, pointA, pointB, pointC)
    with pytest.raises(ValueError) as excinfo:
        p.setup_labels(['', '', ''])
    assert str(excinfo.value) == 'The number of labels (3) should be equal ' \
        'to the number of line segments (4).'
    p.setup_labels([Number(7, unit='cm'), Number(5, unit='cm'),
                    Number(6, unit='cm'), Number(4, unit='cm')])
    assert all(s.label_mask is None for s in p.sides)
    with pytest.raises(ValueError) as excinfo:
        p.setup_labels([Number(7, unit='cm'), Number(5, unit='cm'),
                        Number(6, unit='cm'), Number(4, unit='cm')],
                       masks=['', ''])
    assert str(excinfo.value) == 'The number of label masks (2) should be '\
        'equal to the number of line segments (4).'
    with pytest.raises(ValueError) as excinfo:
        p.setup_labels()
    assert str(excinfo.value) == 'There must be at least either labels or '\
        'masks to setup. Both are undefined (None).'


def test_perimeter(pointO, pointA, pointB, pointC):
    """Check Polygon's sides' labeling."""
    p = Polygon(pointO, pointA, pointB, pointC)
    assert p.perimeter.rounded(Number('0.01')) == Number('11.63')


def test_lbl_perimeter(pointO, pointA, pointB, pointC):
    """Check Polygon's sides' labeling."""
    p = Polygon(pointO, pointA, pointB, pointC)
    with pytest.raises(RuntimeError) as excinfo:
        p.lbl_perimeter
    assert str(excinfo.value) == 'All labels must have been set as Numbers ' \
        'in order to calculate the perimeter from labels.'
    p.setup_labels([Number(7, unit='cm'), Number(5, unit='cm'),
                    Number(6, unit='cm'), Number(4, unit='cm')],
                   masks=[None, None, '?', ' '])
    assert p.lbl_perimeter == Number(22, unit='cm')


def test_winding(pointO, pointA, pointB, pointC, pointI, pointJ):
    """Check the Polygon's winding."""
    config.polygons.DEFAULT_WINDING = 'clockwise'
    with pytest.warns(UserWarning) as record:
        p = Polygon(pointO, pointI, pointJ)
    assert len(record) == 1
    assert str(record[0].message) == 'Changed the order of Points to comply '\
        'with forced winding (clockwise) for Triangle JIO.'
    assert p.winding == 'clockwise'
    q = Polygon(pointO, pointJ, pointI)
    assert q.winding == 'clockwise'
    config.polygons.DEFAULT_WINDING = 'anticlockwise'
    with pytest.warns(UserWarning) as record:
        q = Polygon(pointO, pointJ, pointI)
    assert len(record) == 1
    assert q.winding == 'anticlockwise'
    config.polygons.DEFAULT_WINDING = None
    p = Polygon(pointO, pointI, pointJ)
    assert p.winding == 'anticlockwise'
    q = Polygon(pointO, pointJ, pointI)
    assert q.winding == 'clockwise'
    with pytest.raises(AttributeError) as excinfo:
        q.winding = 'clockwise'
    assert str(excinfo.value) == 'Cannot reset the winding of a Polygon.'
    with pytest.raises(AttributeError) as excinfo:
        q.winding = 'counterclockwise'
    assert str(excinfo.value) == 'Cannot reset the winding of a Polygon.'
    with pytest.raises(ValueError) as excinfo:
        Polygon(pointO, pointJ, pointI, winding='counterclockwise')
    assert str(excinfo.value) == 'Expect \'clockwise\' or '\
        '\'anticlockwise\'. Found \'counterclockwise\' instead.'
    config.polygons.ENABLE_MISMATCH_WINDING_WARNING = False
    with pytest.warns(None) as record:
        p = Polygon(pointO, pointA, pointB, pointC, name='PLUM',
                    winding='clockwise')
    assert len(record) == 0
    config.polygons.ENABLE_MISMATCH_WINDING_WARNING = True
    p.setup_labels(['one', 'two', 'three', 'four'])
    p.setup_marks(['|', '||', '|||', '||||'])
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (P) at (1,3);
\coordinate (L) at (3,2);
\coordinate (U) at (4,0);
\coordinate (M) at (0,0);

% Draw Quadrilateral
\draw[thick] (P)
-- (L) node[midway, above, sloped] {three} """\
r"""node[midway, sloped, scale=0.5] {|||}
-- (U) node[midway, above, sloped] {two} node[midway, sloped, scale=0.5] {||}
-- (M) node[midway, below, sloped] {one} node[midway, sloped, scale=0.5] {|}
-- cycle node[midway, above, sloped] """\
r"""{four} node[midway, sloped, scale=0.5] {||||};

% Label Points
\draw (P) node[above left] {P};
\draw (L) node[above right] {L};
\draw (U) node[below right] {U};
\draw (M) node[below left] {M};
\end{tikzpicture}
"""


def test_simple_drawing(pointO, pointA, pointB, pointC):
    """Check drawing the Polygon."""
    p = Polygon(pointO, pointA, pointB, pointC, name='PLUM')
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (P) at (0,0);
\coordinate (L) at (4,0);
\coordinate (U) at (3,2);
\coordinate (M) at (1,3);

% Draw Quadrilateral
\draw[thick] (P)
-- (L)
-- (U)
-- (M)
-- cycle;

% Label Points
\draw (P) node[below left] {P};
\draw (L) node[below right] {L};
\draw (U) node[above right] {U};
\draw (M) node[above left] {M};
\end{tikzpicture}
"""
    p = Polygon(pointO, pointA, pointB, pointC)
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Quadrilateral
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

% Draw Quadrilateral
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

% Draw Quadrilateral
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

% Draw Quadrilateral
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
    p.sides[1].unlock_label()
    p.sides[1].label = '3 cm'
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Quadrilateral
\draw[thick] (O)
-- (A)
-- (B) node[midway, above, sloped] {3 cm}
-- (C)
-- cycle;

% Label Points

\end{tikzpicture}
"""
    p.sides[0].unlock_label()
    p.sides[0].label = '? cm'
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Quadrilateral
\draw[thick] (O)
-- (A) node[midway, below, sloped] {? cm}
-- (B) node[midway, above, sloped] {3 cm}
-- (C)
-- cycle;

% Label Points

\end{tikzpicture}
"""
    p.sides[3].unlock_label()
    p.sides[3].label = '5 cm'
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Quadrilateral
\draw[thick] (O)
-- (A) node[midway, below, sloped] {? cm}
-- (B) node[midway, above, sloped] {3 cm}
-- (C)
-- cycle node[midway, above, sloped] {5 cm};

% Label Points

\end{tikzpicture}
"""
    p.setup_labels([Number(7, unit='cm'), Number(5, unit='cm'),
                    Number(6, unit='cm'), Number(4, unit='cm')])
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Quadrilateral
\draw[thick] (O)
-- (A) node[midway, below, sloped] {\SI{7}{cm}}
-- (B) node[midway, above, sloped] {\SI{5}{cm}}
-- (C) node[midway, above, sloped] {\SI{6}{cm}}
-- cycle node[midway, above, sloped] {\SI{4}{cm}};

% Label Points

\end{tikzpicture}
"""
    p.setup_labels(masks=[None, None, '?', ' '])
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Quadrilateral
\draw[thick] (O)
-- (A) node[midway, below, sloped] {\SI{7}{cm}}
-- (B) node[midway, above, sloped] {\SI{5}{cm}}
-- (C) node[midway, above, sloped] {?}
-- cycle;

% Label Points

\end{tikzpicture}
"""
    p = Polygon(pointC, pointB, pointA, pointO)
    p.label_vertices = False
    p.setup_labels([Number(7, unit='cm'), Number(5, unit='cm'),
                    Number(6, unit='cm'), Number(4, unit='cm')])
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (C) at (1,3);
\coordinate (B) at (3,2);
\coordinate (A) at (4,0);
\coordinate (O) at (0,0);

% Draw Quadrilateral
\draw[thick] (C)
-- (B) node[midway, above, sloped] {\SI{7}{cm}}
-- (A) node[midway, above, sloped] {\SI{5}{cm}}
-- (O) node[midway, below, sloped] {\SI{6}{cm}}
-- cycle node[midway, above, sloped] {\SI{4}{cm}};

% Label Points

\end{tikzpicture}
"""
    p.setup_labels([Number('7.5', unit='cm'), None, None, None])
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (C) at (1,3);
\coordinate (B) at (3,2);
\coordinate (A) at (4,0);
\coordinate (O) at (0,0);

% Draw Quadrilateral
\draw[thick] (C)
-- (B) node[midway, above, sloped] {\SI{7.5}{cm}}
-- (A)
-- (O)
-- cycle;

% Label Points

\end{tikzpicture}
"""
    locale.setlocale(locale.LC_ALL, LOCALE_FR)
    p.setup_labels([Number('7.5', unit='cm'), None, None, None])
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (C) at (1,3);
\coordinate (B) at (3,2);
\coordinate (A) at (4,0);
\coordinate (O) at (0,0);

% Draw Quadrilateral
\draw[thick] (C)
-- (B) node[midway, above, sloped] {\SI{7,5}{cm}}
-- (A)
-- (O)
-- cycle;

% Label Points

\end{tikzpicture}
"""
    locale.setlocale(locale.LC_ALL, LOCALE_US)
    p.sloped_sides_labels = False
    p.setup_labels([Number('7.5'), None, None, None])
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (C) at (1,3);
\coordinate (B) at (3,2);
\coordinate (A) at (4,0);
\coordinate (O) at (0,0);

% Draw Quadrilateral
\draw[thick] (C)
-- (B) node[midway, above right] {7.5}
-- (A)
-- (O)
-- cycle;

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

% Draw Quadrilateral
\draw[thick] (O)
-- (A) node[midway, sloped, scale=0.5] {//}
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

% Draw Quadrilateral
\draw[thick] (O)
-- (A) node[midway, sloped, scale=0.5] {//}
-- (B)
-- (C)
-- cycle node[midway, sloped, scale=0.5] {//};

% Label Points

\end{tikzpicture}
"""
    p.setup_marks(['|', '||', 'O', '|||'])
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Quadrilateral
\draw[thick] (O)
-- (A) node[midway, sloped, scale=0.5] {|}
-- (B) node[midway, sloped, scale=0.5] {||}
-- (C) node[midway, sloped, scale=0.5] {O}
-- cycle node[midway, sloped, scale=0.5] {|||};

% Label Points

\end{tikzpicture}
"""
    p.do_cycle = False
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Quadrilateral
\draw[thick] (O)
-- (A) node[midway, sloped, scale=0.5] {|}
-- (B) node[midway, sloped, scale=0.5] {||}
-- (C) node[midway, sloped, scale=0.5] {O}
-- (O) node[midway, sloped, scale=0.5] {|||} -- cycle;

% Label Points

\end{tikzpicture}
"""


def test_drawing_with_marked_angles(pointO, pointA, pointB, pointC, pointJ):
    """Check drawing a Polygon having some marked angles."""
    p = Polygon(pointO, pointA, pointB, pointC)
    p.label_vertices = False
    p.angles[1].decoration = AngleDecoration()
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Quadrilateral
\draw[thick] (O)
-- (A)
-- (B)
-- (C)
-- cycle
pic [draw, thick, angle radius = 0.25 cm] {angle = B--A--O};

% Label Points

\end{tikzpicture}
"""
    p.angles[2].decoration = AngleDecoration(color='red', thickness='thin',
                                             radius=Number(8, unit='mm'))
    assert p.drawn == \
        r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (C) at (1,3);

% Draw Quadrilateral
\draw[thick] (O)
-- (A)
-- (B)
-- (C)
-- cycle
pic [draw, thick, angle radius = 0.25 cm] {angle = B--A--O}
pic [draw, thin, angle radius = 8 mm, red] {angle = C--B--A};

% Label Points

\end{tikzpicture}
"""
    required.tikz_library['angles'] = False
    p = Polygon(pointO, pointA, pointB, pointJ)
    p.label_vertices = False
    p.angles[0].decoration = AngleDecoration()
    p.angles[0].mark_right = True
    assert p.drawn == \
        r"""
\begin{tikzpicture}
% Declare Points
\coordinate (O) at (0,0);
\coordinate (A) at (4,0);
\coordinate (B) at (3,2);
\coordinate (J) at (0,1);

% Draw Quadrilateral
\draw[thick] (O)
-- (A)
-- (B)
-- (J)
-- cycle;

% Mark right angles
\draw[thick, cm={cos(0), sin(0), -sin(0), cos(0), (O)}] """\
        r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);

% Label Points

\end{tikzpicture}
"""
    assert not required.tikz_library['angles']
