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
from mathmakerlib.calculus import Number, Unit
from mathmakerlib.geometry import Point, PointsPair
from mathmakerlib.geometry.angle import AngleDecoration, Angle, AnglesSet


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
    return Point(1, 1, 'A')


def test_AngleDecoration():
    assert repr(AngleDecoration()) == 'AngleDecoration(variety=single; '\
        'hatchmark=None; label=default; color=None; thickness=thick; '\
        'radius=0.25 cm; eccentricity=2.6)'
    assert repr(AngleDecoration(radius=Number(1, unit='cm'))) == \
        'AngleDecoration(variety=single; '\
        'hatchmark=None; label=default; color=None; thickness=thick; '\
        'radius=1 cm; eccentricity=1.4)'
    assert AngleDecoration().tikz_attributes() \
        == '[draw, thick, angle radius = 0.25 cm]'
    assert AngleDecoration(color='green', thickness='thin').tikz_attributes() \
        == '[draw, thin, angle radius = 0.25 cm, green]'
    assert AngleDecoration(radius=Number('0.5', unit=Unit('cm'))) \
        .tikz_attributes() == '[draw, thick, angle radius = 0.5 cm]'
    with pytest.raises(TypeError) as excinfo:
        AngleDecoration(radius='2 cm')
    assert str(excinfo.value) == 'Expected a number as radius. Got ' \
        '<class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        AngleDecoration().tikz_attributes(radius_coeff='a')
    assert str(excinfo.value) == 'radius_coeff must be a number, '\
        'found <class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        AngleDecoration(hatchmark='unknown')
    assert str(excinfo.value) == 'AngleDecoration\'s hatchmark can be None, '\
        '\'singledash\', \'doubledash\' or \'tripledash\'. ' \
        'Found \'unknown\' instead (type: <class \'str\'>).'
    with pytest.raises(TypeError) as excinfo:
        AngleDecoration(eccentricity='a')
    assert str(excinfo.value) == 'The eccentricity of an AngleDecoration '\
        'must be a Number. Found <class \'str\'> instead.'
    with pytest.raises(RuntimeError) as excinfo:
        AngleDecoration().generate_tikz('A', 'B')
    assert str(excinfo.value) == 'Three Points\' names must be provided to '\
        'generate the AngleDecoration. Found 2 arguments instead.'


def test_instanciation_errors(pointO, pointI, pointJ):
    """Check Angle's instanciation exceptions."""
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI)
    assert str(excinfo.value) == '__init__() missing 1 required positional ' \
        'argument: \'point_or_measure\''
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, 'J')
    assert str(excinfo.value) == 'Three Points, or two Points and the ' \
        'measure of the angle are required to build an Angle. ' \
        'Found instead: <class \'mathmakerlib.geometry.point.Point\'>, ' \
        '<class \'mathmakerlib.geometry.point.Point\'> and ' \
        '<class \'str\'>.'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, pointJ, mark_right=1)
    assert str(excinfo.value) == '\'mark_right\' must be a boolean'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, pointJ, decoration='right')
    assert str(excinfo.value) == 'An angle decoration must be None or belong '\
        'to the AngleDecoration class. Got <class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, pointJ,
              decoration=AngleDecoration(variety='unknown'))
    assert str(excinfo.value) == 'AngleDecoration\'s variety can be None, ' \
        '\'single\', \'double\' or \'triple\'. Found \'unknown\' instead '\
        '(type: <class \'str\'>).'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, pointJ, draw_vertex='a')
    assert str(excinfo.value) == 'draw_vertex must be a boolean; ' \
        'got <class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, pointJ, label_vertex='a')
    assert str(excinfo.value) == 'label_vertex must be a boolean; ' \
        'got <class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, pointJ, draw_endpoints='a')
    assert str(excinfo.value) == 'draw_endpoints must be a boolean; ' \
        'got <class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, pointJ, label_endpoints='a')
    assert str(excinfo.value) == 'label_endpoints must be a boolean; ' \
        'got <class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, pointJ, draw_armspoints='a')
    assert str(excinfo.value) == 'draw_armspoints must be a boolean; ' \
        'got <class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, pointJ, label_armspoints='a')
    assert str(excinfo.value) == 'label_armspoints must be a boolean; ' \
        'got <class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, pointJ, armspoints='X')
    assert str(excinfo.value) == 'A list must be provided to setup ' \
        'armspoints. Found <class \'str\'> instead.'
    with pytest.raises(ValueError) as excinfo:
        Angle(pointO, pointI, pointJ, armspoints=['1', '2', '3'])
    assert str(excinfo.value) == 'More values are provided (3) then ' \
        'available arms (2).'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, pointJ, armspoints=['1', '2'])
    assert str(excinfo.value) == 'Each arm\'s point must be defined by a ' \
        'tuple. Found <class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Angle(pointO, pointI, pointJ, armspoints=[('1', '2', '3'), ('2', )])
    assert str(excinfo.value) == 'Each arm\'s point must be defined by a ' \
        'tuple of 1 or 2 elements. Found 3 elements instead.'


def test_instanciation(pointO, pointI, pointJ, pointA):
    """Check Angle's instanciation."""
    theta = Angle(pointI, pointO, pointJ, mark_right=True)
    assert theta.measure == Number('90')
    assert isinstance(theta.decoration, AngleDecoration)
    assert theta.decoration.label is None
    assert theta.decoration.variety is None
    assert theta.mark_right
    assert theta.vertex == pointO
    assert theta.points == [pointI, pointO, pointJ]
    theta = Angle(pointA, pointO, pointI, decoration=AngleDecoration())
    assert theta.measure == Number('45')
    assert not theta.mark_right
    assert theta.vertex == pointO
    assert theta.points == [pointA, pointO, pointI]
    theta = Angle(pointI, pointO, 60)
    assert theta.vertex == pointO
    assert theta.points[2] == Point('0.5', '0.866', 'I\'')
    A = Point(0, 0, 'A')
    X = Point(6, 1, 'X')
    Y = Point(3, 5, 'Y')
    α = Angle(X, A, Y)
    assert α.winding == 'anticlockwise'
    assert α.arms[0].same_as(PointsPair(A, X))
    assert α.arms[1].same_as(PointsPair(A, Y))


def test_marked_angles(pointO, pointI, pointJ, pointA):
    """Check Angle's instanciation."""
    required.tikz_library['angles'] = False
    theta = Angle(pointI, pointO, pointJ)
    assert theta.tikz_decoration() == ''
    theta.decoration = AngleDecoration(color='red', thickness='ultra thick',
                                       radius=Number(2))
    assert theta.tikz_decoration() \
        == 'pic [draw, ultra thick, angle radius = 2, red] {angle = I--O--J}'
    assert required.tikz_library['angles']
    required.tikz_library['angles'] = False
    theta.mark_right = True
    theta.decoration = AngleDecoration()
    assert theta.label is None
    assert theta.tikz_decoration() == ''
    assert not required.tikz_library['angles']
    assert theta.tikz_rightangle_mark() == \
        '\draw[thick, cm={cos(0), sin(0), -sin(0), cos(0), (O)}]' \
        ' (0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);'
    assert theta.tikz_rightangle_mark(winding='clockwise') == \
        '\draw[thick, cm={cos(0), sin(0), -sin(0), cos(0), (O)}]' \
        ' (0.25 cm, 0) -- (0.25 cm, -0.25 cm) -- (0, -0.25 cm);'
    with pytest.raises(ValueError) as excinfo:
        theta.tikz_rightangle_mark(winding=None)
    assert str(excinfo.value) == 'Expect \'clockwise\' or \'anticlockwise\'. '\
        'Found \'None\' instead.'


def test_drawing_angles():
    """Check drawing standalone Angles."""
    A = Point(0, 0, 'A')
    X = Point(6, 1, 'X')
    Y = Point(3, 5, 'Y')
    α = Angle(X, A, Y)
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y);

% Label Points

\end{tikzpicture}
"""
    α.label_vertex = True
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y);

% Label Points
\draw (A) node[below left] {A};
\end{tikzpicture}
"""
    α.label_endpoints = True
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y);

% Label Points
\draw (A) node[below left] {A};
\draw (X) node[below right] {X};
\draw (Y) node[above left] {Y};
\end{tikzpicture}
"""
    α.draw_vertex = True
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y);
% Draw Vertex
\draw (A) node[scale=0.67] {$\times$};

% Label Points
\draw (A) node[below left] {A};
\draw (X) node[below right] {X};
\draw (Y) node[above left] {Y};
\end{tikzpicture}
"""
    α.draw_endpoints = True
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y);
% Draw Vertex
\draw (A) node[scale=0.67] {$\times$};
% Draw End Points
\draw (X) node[scale=0.67] {$\times$};
\draw (Y) node[scale=0.67] {$\times$};

% Label Points
\draw (A) node[below left] {A};
\draw (X) node[below right] {X};
\draw (Y) node[above left] {Y};
\end{tikzpicture}
"""
    α.draw_armspoints = True
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y);
% Draw Vertex
\draw (A) node[scale=0.67] {$\times$};
% Draw End Points
\draw (X) node[scale=0.67] {$\times$};
\draw (Y) node[scale=0.67] {$\times$};

% Label Points
\draw (A) node[below left] {A};
\draw (X) node[below right] {X};
\draw (Y) node[above left] {Y};
\end{tikzpicture}
"""


def test_drawing_labeled_angles():
    """Check drawing standalone Angles."""
    A = Point(0, 0, 'A')
    X = Point(6, 1, 'X')
    Y = Point(3, 5, 'Y')
    α = Angle(X, A, Y, label=Number(38, unit=r'\textdegree'))
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y)
pic ["\ang{38}", angle eccentricity=2.6] {angle = X--A--Y};

% Label Points

\end{tikzpicture}
"""
    assert α.label == r'\ang{38}'
    α.decoration = None
    assert α.label == r'\ang{38}'
    assert α.decoration is not None
    assert repr(α.decoration) == r'AngleDecoration(variety=None; '\
        r'hatchmark=None; label=\ang{38}; color=None; thickness=thick; '\
        r'radius=0.25 cm; eccentricity=2.6)'


def test_drawing_angles_with_armspoints():
    """Check drawing standalone Angles."""
    A = Point(0, 0, 'A')
    X1 = Point(6, 1, 'X1')
    Y1 = Point(3, 5, 'Y1')
    α = Angle(X1, A, Y1, armspoints=[('X', ), ('Y', )],
              label_vertex=True, draw_vertex=True)
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X1) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y1) at (3,5);
\coordinate (X) at (4.8,0.8);
\coordinate (Y) at (2.4,4.0);

% Draw Angle
\draw[thick] (X1) -- (A) -- (Y1);
% Draw Vertex
\draw (A) node[scale=0.67] {$\times$};
% Draw Arms' Points
\draw (X) node[scale=0.67] {$\times$};
\draw (Y) node[scale=0.67] {$\times$};

% Label Points
\draw (A) node[below left] {A};
\draw (X) node[below right] {X};
\draw (Y) node[above left] {Y};
\end{tikzpicture}
"""
    Point.reset_names()
    A = Point(0, 0, 'A')
    X1 = Point(6, 1, 'X1')
    Y1 = Point(3, 5, 'Y1')
    α = Angle(X1, A, Y1, armspoints=[('X', ), ('Y', )],
              label_vertex=True, draw_vertex=True)
    α.armspoints = [('', ), (None, )]
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X1) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y1) at (3,5);
\coordinate (E) at (4.8,0.8);
\coordinate (F) at (2.4,4.0);

% Draw Angle
\draw[thick] (X1) -- (A) -- (Y1);
% Draw Vertex
\draw (A) node[scale=0.67] {$\times$};
% Draw Arms' Points
\draw (E) node[scale=0.67] {$\times$};
\draw (F) node[scale=0.67] {$\times$};

% Label Points
\draw (A) node[below left] {A};
\draw (E) node[below right] {E};
\draw (F) node[above left] {F};
\end{tikzpicture}
"""


def test_drawing_marked_angles():
    """Check drawing standalone Angles."""
    A = Point(0, 0, 'A')
    X = Point(6, 1, 'X')
    Y = Point(3, 5, 'Y')
    α = Angle(X, A, Y)
    α.decoration = AngleDecoration(radius=Number('0.5', unit='cm'))
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y)
pic [draw, thick, angle radius = 0.5 cm] {angle = X--A--Y};

% Label Points

\end{tikzpicture}
"""
    α.decoration.variety = 'double'
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y)
pic [draw, thick, angle radius = 0.5 cm] {angle = X--A--Y}
pic [draw, thick, angle radius = 0.58 cm] {angle = X--A--Y};

% Label Points

\end{tikzpicture}
"""
    α.decoration.variety = 'triple'
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y)
pic [draw, thick, angle radius = 0.5 cm] {angle = X--A--Y}
pic [draw, thick, angle radius = 0.58 cm] {angle = X--A--Y}
pic [draw, thick, angle radius = 0.66 cm] {angle = X--A--Y};

% Label Points

\end{tikzpicture}
"""
    α.decoration.variety = 'single'
    α.decoration.hatchmark = 'singledash'
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y)
pic [draw, thick, angle radius = 0.5 cm, singledash] {angle = X--A--Y};

% Label Points

\end{tikzpicture}
"""
    assert required.tikz_library['decorations.markings']
    assert required.tikzset['singledash_hatchmark']
    assert not required.tikzset['doubledash_hatchmark']
    assert not required.tikzset['tripledash_hatchmark']
    required.tikz_library['decorations.markings'] = False
    required.tikzset['singledash_hatchmark'] = False
    α.decoration.hatchmark = 'doubledash'
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y)
pic [draw, thick, angle radius = 0.5 cm, doubledash] {angle = X--A--Y};

% Label Points

\end{tikzpicture}
"""
    assert required.tikz_library['decorations.markings']
    assert not required.tikzset['singledash_hatchmark']
    assert required.tikzset['doubledash_hatchmark']
    assert not required.tikzset['tripledash_hatchmark']
    required.tikz_library['decorations.markings'] = False
    required.tikzset['doubledash_hatchmark'] = False
    α.decoration.hatchmark = 'tripledash'
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y)
pic [draw, thick, angle radius = 0.5 cm, tripledash] {angle = X--A--Y};

% Label Points

\end{tikzpicture}
"""
    assert required.tikz_library['decorations.markings']
    assert not required.tikzset['singledash_hatchmark']
    assert not required.tikzset['doubledash_hatchmark']
    assert required.tikzset['tripledash_hatchmark']
    α.decoration.variety = 'triple'
    α.decoration.hatchmark = 'doubledash'
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y)
pic [draw, thick, angle radius = 0.5 cm, doubledash] {angle = X--A--Y}
pic [draw, thick, angle radius = 0.58 cm, doubledash] {angle = X--A--Y}
pic [draw, thick, angle radius = 0.66 cm, doubledash] {angle = X--A--Y};

% Label Points

\end{tikzpicture}
"""


def test_drawing_marked_labeled_angles():
    """Check drawing standalone Angles."""
    A = Point(0, 0, 'A')
    X = Point(6, 1, 'X')
    Y = Point(3, 5, 'Y')
    α = Angle(X, A, Y, label=Number(38, unit=r'\textdegree'))
    α.decoration = AngleDecoration(radius=Number('0.5', unit='cm'))
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y)
pic ["\ang{38}", angle eccentricity=1.8, draw, thick, """\
r"""angle radius = 0.5 cm] {angle = X--A--Y};

% Label Points

\end{tikzpicture}
"""
    α.decoration.variety = 'double'
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y)
pic ["\ang{38}", angle eccentricity=1.8, draw, thick, """\
r"""angle radius = 0.5 cm] {angle = X--A--Y}
pic [draw, thick, angle radius = 0.58 cm] {angle = X--A--Y};

% Label Points

\end{tikzpicture}
"""
    A = Point(0, 0, 'A')
    X1 = Point(6, 1, 'X1')
    Y1 = Point(3, 5, 'Y1')
    α = Angle(X1, A, Y1, armspoints=[('X', ), ('Y', )],
              label_vertex=True, draw_vertex=True,
              label=Number(38, unit=r'\textdegree'))
    α.decoration = AngleDecoration(radius=Number('0.5', unit='cm'),
                                   variety='double',
                                   hatchmark='singledash')
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X1) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y1) at (3,5);
\coordinate (X) at (4.8,0.8);
\coordinate (Y) at (2.4,4.0);

% Draw Angle
\draw[thick] (X1) -- (A) -- (Y1)
pic ["\ang{38}", angle eccentricity=1.8, draw, thick, """\
r"""angle radius = 0.5 cm, singledash] {angle = X1--A--Y1}
pic [draw, thick, angle radius = 0.58 cm, singledash] {angle = X1--A--Y1};
% Draw Vertex
\draw (A) node[scale=0.67] {$\times$};
% Draw Arms' Points
\draw (X) node[scale=0.67] {$\times$};
\draw (Y) node[scale=0.67] {$\times$};

% Label Points
\draw (A) node[below left] {A};
\draw (X) node[below right] {X};
\draw (Y) node[above left] {Y};
\end{tikzpicture}
"""


def test_AnglesSet_instanciation_errors(pointO, pointI, pointJ):
    """Check AnglesSet's instanciation exceptions."""
    with pytest.raises(TypeError) as excinfo:
        AnglesSet(pointO)
    assert str(excinfo.value) == 'Any element of an AnglesSet must be an ' \
        'Angle. Found <class \'mathmakerlib.geometry.point.Point\'> instead.'


def test_AnglesSet_instanciation():
    """Check AnglesSets instanciation."""
    A = Point(0, 0, 'A')
    X1 = Point(6, 1, 'X1')
    Y1 = Point(3, 5, 'Y1')
    Z1 = Point(1, '6.5', 'X1')
    α = Angle(X1, A, Y1)
    β = Angle(Y1, A, Z1)
    S = AnglesSet(α, β)
    assert S._tikz_draw_options() == []


def test_drawing_AnglesSets_errors():
    """Check errors when drawing AnglesSets."""
    A = Point(0, 0, 'A')
    X1 = Point(6, 1, 'X1')
    Y1 = Point(3, 5, 'Y1')
    Z1 = Point(1, '6.5', 'X1')
    α = Angle(X1, A, Y1)
    β = Angle(Y1, A, Z1)
    S = AnglesSet(α, β)
    with pytest.raises(RuntimeError) as excinfo:
        S.drawn
    assert str(excinfo.value) == 'Two different Points have been provided ' \
        'the same name in this list: A(0; 0); X1(6; 1); Y1(3; 5); X1(1; 6.5)'


def test_drawing_AnglesSets_of_same_vertex():
    """Check drawing AnglesSets."""
    A = Point(0, 0, 'A')
    X1 = Point(6, 1, 'X1')
    Y1 = Point(3, 5, 'Y1')
    Z1 = Point(1, '6.5', 'Z1')
    α = Angle(X1, A, Y1)
    β = Angle(Y1, A, Z1)
    S = AnglesSet(α, β)
    assert S.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (X1) at (6,1);
\coordinate (Y1) at (3,5);
\coordinate (Z1) at (1,6.5);

% Draw Angles
\draw[thick] (X1) -- (A) -- (Y1);
\draw[thick] (Y1) -- (A) -- (Z1);

% Label Points

\end{tikzpicture}
"""
    α.armspoints = [('X', ), ('Y', )]
    α.label_vertex = True
    α.draw_vertex = True
    β.armspoints = [('Y', ), ('Z', )]
    assert S.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (X1) at (6,1);
\coordinate (Y1) at (3,5);
\coordinate (X) at (4.8,0.8);
\coordinate (Y) at (2.4,4.0);
\coordinate (Z1) at (1,6.5);
\coordinate (Z) at (0.8,5.20);

% Draw Angles
\draw[thick] (X1) -- (A) -- (Y1);
\draw[thick] (Y1) -- (A) -- (Z1);
% Draw Vertex
\draw (A) node[scale=0.67] {$\times$};
% Draw Arms' Points
\draw (X) node[scale=0.67] {$\times$};
\draw (Y) node[scale=0.67] {$\times$};
\draw (Z) node[scale=0.67] {$\times$};

% Label Points
\draw (A) node[below] {A};
\draw (X) node[below right] {X};
\draw (Y) node[above left] {Y};
\draw (Z) node[above left] {Z};
\end{tikzpicture}
"""
    Point.reset_names()
    A = Point(0, 0, 'A')
    X1 = Point(6, 1, 'X1')
    Y1 = Point(3, 5, 'Y1')
    Z1 = Point(1, '6.5', 'Z1')
    α = Angle(X1, A, Y1, armspoints=[('X', ), ('Y', )],
              label_vertex=True, draw_vertex=True,
              decoration=AngleDecoration(color='RoyalBlue',
                                         radius=Number('0.5', unit='cm')),
              label=Number(38, unit=r'\textdegree'))
    β = Angle(Y1, A, Z1, armspoints=[('Y', ), ('Z', )],
              decoration=AngleDecoration(color='BurntOrange', variety='double',
                                         radius=Number('0.5', unit='cm')),
              label=Number(9, unit=r'\textdegree'))
    γ = Angle(X1, A, Z1, label='?',
              decoration=AngleDecoration(color='BrickRed',
                                         radius=Number('2', unit='cm'),
                                         eccentricity=Number('1.15')))
    S = AnglesSet(α, β, γ)
    assert S.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (X1) at (6,1);
\coordinate (Y1) at (3,5);
\coordinate (X) at (4.8,0.8);
\coordinate (Y) at (2.4,4.0);
\coordinate (Z1) at (1,6.5);
\coordinate (Z) at (0.8,5.20);

% Draw Angles
\draw[thick] (X1) -- (A) -- (Y1)
pic ["\ang{38}", angle eccentricity=1.8, draw, thick, """\
r"""angle radius = 0.5 cm, RoyalBlue] {angle = X1--A--Y1};
\draw[thick] (Y1) -- (A) -- (Z1)
pic ["\ang{9}", angle eccentricity=1.8, draw, thick, """\
r"""angle radius = 0.5 cm, BurntOrange] {angle = Y1--A--Z1}
pic [draw, thick, angle radius = 0.58 cm, BurntOrange] {angle = Y1--A--Z1};
\draw[thick] (X1) -- (A) -- (Z1)
pic ["?", angle eccentricity=1.15, draw, thick, """\
r"""angle radius = 2 cm, BrickRed] {angle = X1--A--Z1};
% Draw Vertex
\draw (A) node[scale=0.67] {$\times$};
% Draw Arms' Points
\draw (X) node[scale=0.67] {$\times$};
\draw (Y) node[scale=0.67] {$\times$};
\draw (Z) node[scale=0.67] {$\times$};

% Label Points
\draw (A) node[below left] {A};
\draw (X) node[below right] {X};
\draw (Y) node[above left] {Y};
\draw (Z) node[above left] {Z};
\end{tikzpicture}
"""


def test_drawing_scattered_AnglesSets():
    """Check drawing AnglesSets."""
    A = Point(0, 0, 'A')
    X1 = Point(6, 1, 'X1')
    Y1 = Point(3, 5, 'Y1')
    U = Point(-1, 1, 'U')
    W1 = Point(-2, 3, 'W1')
    Z1 = Point(1, '6.5', 'Z1')
    α = Angle(X1, A, Y1, draw_vertex=True, draw_endpoints=True,
              label_endpoints=True)
    β = Angle(W1, U, Z1, draw_vertex=True, draw_endpoints=True,
              label_endpoints=True)
    S = AnglesSet(α, β)
    assert S.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (X1) at (6,1);
\coordinate (Y1) at (3,5);
\coordinate (U) at (-1,1);
\coordinate (W1) at (-2,3);
\coordinate (Z1) at (1,6.5);

% Draw Angles
\draw[thick] (X1) -- (A) -- (Y1);
\draw[thick] (W1) -- (U) -- (Z1);
% Draw Vertices
\draw (A) node[scale=0.67] {$\times$};
\draw (U) node[scale=0.67] {$\times$};
% Draw End Points
\draw (X1) node[scale=0.67] {$\times$};
\draw (Y1) node[scale=0.67] {$\times$};
\draw (W1) node[scale=0.67] {$\times$};
\draw (Z1) node[scale=0.67] {$\times$};

% Label Points
\draw (X1) node[below right] {X1};
\draw (Y1) node[above left] {Y1};
\draw (W1) node[left] {W1};
\draw (Z1) node[right] {Z1};
\end{tikzpicture}
"""
