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

from mathmakerlib import required, config
from mathmakerlib.calculus import Number, Unit
from mathmakerlib.geometry import Point, Bipoint
from mathmakerlib.geometry.angle import AngleDecoration, Angle, AnglesSet
from mathmakerlib.geometry.angle import AVAILABLE_NAMING_MODES


def test_AngleDecoration():
    assert repr(AngleDecoration()) == 'AngleDecoration(variety=single; '\
        'hatchmark=None; label=default; color=None; thickness=thick; '\
        'radius=0.25 cm; eccentricity=2.6)'
    ad = AngleDecoration(radius=Number(1, unit='cm'))
    assert ad.arrow_tips is None
    assert repr(ad) == \
        'AngleDecoration(variety=single; '\
        'hatchmark=None; label=default; color=None; thickness=thick; '\
        'radius=1 cm; eccentricity=1.4)'
    ad.radius = Number(2, unit='cm')
    assert repr(ad) == \
        'AngleDecoration(variety=single; '\
        'hatchmark=None; label=default; color=None; thickness=thick; '\
        'radius=2 cm; eccentricity=1.2)'
    assert AngleDecoration().tikz_attributes() \
        == '[draw, thick, angle radius = 0.25 cm]'
    assert AngleDecoration(color='green', thickness='thin').tikz_attributes() \
        == '[draw, thin, angle radius = 0.25 cm, green]'
    assert AngleDecoration(radius=Number('0.5', unit=Unit('cm'))) \
        .tikz_attributes() == '[draw, thick, angle radius = 0.5 cm]'
    with pytest.raises(ValueError) as excinfo:
        AngleDecoration(radius=Number(2, unit='cm'), gap=None)
    assert str(excinfo.value) == 'Cannot calculate the eccentricity if gap '\
        'is None.'
    with pytest.raises(TypeError) as excinfo:
        AngleDecoration(radius='2 cm')
    assert str(excinfo.value) == 'Expected a number as radius. Got ' \
        '<class \'str\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        AngleDecoration(gap='2 cm')
    assert str(excinfo.value) == 'The gap value must be None or a number. '\
        'Found \'2 cm\' instead (type: <class \'str\'>).'
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
        'must be None or a Number. Found <class \'str\'> instead.'
    with pytest.raises(RuntimeError) as excinfo:
        AngleDecoration().generate_tikz('A', 'B')
    assert str(excinfo.value) == 'Three Points\' names must be provided to '\
        'generate the AngleDecoration. Found 2 arguments instead.'
    with pytest.raises(TypeError) as excinfo:
        AngleDecoration(do_draw='a')
    assert str(excinfo.value) == 'do_draw must be a boolean; '\
        'got <class \'str\'> instead.'


def test_instanciation_errors():
    """Check Angle's instanciation exceptions."""
    pointO = Point(0, 0, 'O')
    pointI = Point(1, 0, 'I')
    pointJ = Point(0, 1, 'J')
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
        Angle(pointO, pointI, pointJ, decoration2='right')
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
    with pytest.raises(ValueError) as excinfo:
        Angle(pointO, pointI, pointJ, label=Number(38, unit=r'\textdegree'),
              decoration=AngleDecoration(label=Number(37,
                                                      unit=r'\textdegree')))
    assert str(excinfo.value) == r"The label has been set twice, as Angle's "\
        r"keyword argument (Number('38 \textdegree')) and as its "\
        r"AngleDecoration's keyword argument (Number('37 \textdegree'))."


def test_instanciation():
    """Check Angle's instanciation."""
    pointO = Point(0, 0, 'O')
    pointI = Point(1, 0, 'I')
    pointJ = Point(0, 1, 'J')
    pointA = Point(1, 1, 'A')
    theta = Angle(pointI, pointO, pointJ, mark_right=True)
    assert repr(theta) == 'Angle(I, O, J)'
    assert theta.measure == Number('90')
    assert isinstance(theta.decoration, AngleDecoration)
    assert theta.decoration.label is None
    assert theta.decoration.variety is None
    assert theta.mark_right
    assert theta.vertex == pointO
    assert theta.points == [pointI, pointO, pointJ]
    theta = Angle(pointA, pointO, pointI, decoration=AngleDecoration())
    assert theta.measure == Number('315')
    assert Angle(pointI, pointO, pointA).measure == Number('45')
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
    assert α.arms[0] == Bipoint(A, X)
    assert α.arms[1] == Bipoint(A, Y)


def test_measures_2D():
    """Check Angle's measure."""
    Ω = Point(0, 0, 'Ω')
    X = Point(12, 2, 'X')
    Y = Point(-6, -1, 'Y')
    α = Angle(X, Ω, Y)
    X = Point(6, 1, 'X')
    Y = Point(-6, -1, 'Y')
    α = Angle(X, Ω, Y)
    assert α.measure.rounded(Number('0.001')) == 180
    β = Angle(X, Ω, Point(1, -6, 'Z'))
    assert β.measure.rounded(Number('0.001')) == Number(270)


def test_measures_3D():
    """Check Angle's measure."""
    Ω = Point(0, 0, 0, 'Ω')
    A = Point(1, 0, 0, 'A')
    B = Point(1, 1, 1, 'B')
    α = Angle(A, Ω, B)
    assert α.measure.rounded(Number('0.001')) == Number(54.736)
    C = Point(-1, -1, -1, 'C')
    β = Angle(B, Ω, C)
    assert β.measure.rounded(Number('0.001')) == Number(180)
    D = Point(0, 1, 1, 'D')
    γ = Angle(A, Ω, D)
    assert γ.measure.rounded(Number('0.001')) == Number(90)


def test_naming():
    """Check Angle's naming."""
    A = Point(0, 0, 'A')
    X = Point(6, 1, 'X')
    Y = Point(3, 5, 'Y')
    α = Angle(X, A, Y)
    assert α.name == r'\angle XAY'
    required.package['stackengine'] = required.package['scalerel'] = False
    config.language = 'fr'
    assert α.name == r'\stackon[-5pt]{XAY}{\vstretch{1.5}{\hstretch{1.6}'\
        '{\widehat{\phantom{\;\;\;\;}}}}}'
    assert required.package['stackengine']
    assert required.package['scalerel']
    required.package['stackengine'] = required.package['scalerel'] = False
    config.language = 'en'
    α.naming_mode = 'from_vertex'
    assert α.name == r'\angle A'
    α.naming_mode = 'from_armspoints'
    with pytest.raises(RuntimeError) as excinfo:
        α.name
    assert str(excinfo.value) == 'The naming mode of this Angle is '\
        '\'from_armspoints\' but the armspoints '\
        'are not defined (empty list).'
    α.armspoints = [('Z', ), ('T', )]
    assert α.name == r'\angle ZAT'
    with pytest.raises(ValueError) as excinfo:
        α.naming_mode = 'undefined'
    assert str(excinfo.value) == 'naming_mode must belong to {}. '\
        'Found \'undefined\' instead.'.format(AVAILABLE_NAMING_MODES)


def test_marked_angles():
    """Check Angle's instanciation."""
    pointO = Point(0, 0, 'O')
    pointI = Point(1, 0, 'I')
    pointJ = Point(0, 1, 'J')
    required.tikz_library['angles'] = False
    theta = Angle(pointI, pointO, pointJ)
    assert theta.tikz_decorations() == ''
    theta.decoration = AngleDecoration(color='red', thickness='ultra thick',
                                       radius=Number(2))
    assert theta.tikz_decorations() \
        == 'pic [draw, ultra thick, angle radius = 2, red] {angle = I--O--J}'
    assert required.tikz_library['angles']
    required.tikz_library['angles'] = False
    theta.mark_right = True
    theta.decoration = AngleDecoration()
    assert theta.label is None
    assert theta.tikz_decorations() == ''
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


def test_drawing_angles_with_labeled_vertex():
    """Check drawing standalone Angles."""
    A = Point(0, 0, 'A')
    X = Point(6, 1, 'X')
    Y = Point(3, 5, 'Y')
    α = Angle(X, A, Y)
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
    Z = Point(-6, -3, 'Z')
    α = Angle(X, A, Z)
    α.label_vertex = True
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Z) at (-6,-3);

% Draw Angle
\draw[thick] (X) -- (A) -- (Z);

% Label Points
\draw (A) node[below] {A};
\end{tikzpicture}
"""


def test_drawing_labeled_angles():
    """Check drawing standalone Angles."""
    A = Point(0, 0, 'A')
    X = Point(6, 1, 'X')
    Y = Point(3, 5, 'Y')
    α = Angle(X, A, Y, label=Number(38, unit=r'\textdegree'))
    required.tikz_library['quotes'] = False
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
    assert required.tikz_library['quotes']
    assert α.label == r'\ang{38}'
    α.decoration = None
    assert α.label == r'\ang{38}'
    assert α.decoration is not None
    assert repr(α.decoration) == r'AngleDecoration(variety=None; '\
        r'hatchmark=None; label=\ang{38}; color=None; thickness=thick; '\
        r'radius=0.25 cm; eccentricity=2.6)'
    α = Angle(X, A, Y,
              decoration=AngleDecoration(label=Number(38, unit=r'\textdegree'),
                                         variety=None)
              )
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
    α = Angle(X, A, Y, label=Number(38, unit=r'\textdegree'),
              decoration=AngleDecoration(radius=Number('0.9', unit='cm')))
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y)
pic ["\ang{38}", angle eccentricity=1.44, draw, thick, """\
r"""angle radius = 0.9 cm] {angle = X--A--Y};

% Label Points

\end{tikzpicture}
"""


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
\coordinate (Y) at (2.4,4);

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
\coordinate (B) at (4.8,0.8);
\coordinate (C) at (2.4,4);

% Draw Angle
\draw[thick] (X1) -- (A) -- (Y1);
% Draw Vertex
\draw (A) node[scale=0.67] {$\times$};
% Draw Arms' Points
\draw (B) node[scale=0.67] {$\times$};
\draw (C) node[scale=0.67] {$\times$};

% Label Points
\draw (A) node[below left] {A};
\draw (B) node[below right] {B};
\draw (C) node[above left] {C};
\end{tikzpicture}
"""
    Point.reset_names()
    Ω = Point(0, 0, 'O')
    A1 = Point('2.5', 0, 'A1')
    D1 = Point(-2, '1.5', 'D1')
    α = Angle(A1, Ω, D1, armspoints=[('C', ), ('E', )],
              label_vertex=True, draw_vertex=True,
              label_armspoints=True, draw_armspoints=True)
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A1) at (2.5,0);
\coordinate (O) at (0,0);
\coordinate (D1) at (-2,1.5);
\coordinate (C) at (2,0);
\coordinate (E) at (-1.6,1.2);

% Draw Angle
\draw[thick] (A1) -- (O) -- (D1);
% Draw Vertex
\draw (O) node[scale=0.67] {$\times$};
% Draw Arms' Points
\draw (C) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Label Points
\draw (O) node[below] {O};
\draw (C) node[below right] {C};
\draw (E) node[below left] {E};
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


def test_drawing_angles_with_arrowtips():
    """Check drawing standalone Angles."""
    A = Point(0, 0, 'A')
    X = Point(6, 1, 'X')
    Y = Point(3, 5, 'Y')
    α = Angle(X, A, Y)
    α.decoration = AngleDecoration(arrow_tips='<->')
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (3,5);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y)
pic [draw, <->, thick, angle radius = 0.25 cm] {angle = X--A--Y};

% Label Points

\end{tikzpicture}
"""


def test_drawing_marked_rightangles():
    """Check drawing standalone Angles."""
    A = Point(0, 0, 'A')
    X = Point(6, 1, 'X')
    Y = Point(-1, 6, 'Y')
    α = Angle(X, A, Y)
    α.decoration = AngleDecoration(radius=Number('0.5', unit='cm'))
    α.mark_right = True
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (X) at (6,1);
\coordinate (A) at (0,0);
\coordinate (Y) at (-1,6);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y);

% Mark right angle
\draw[thick, cm={cos(9.46), sin(9.46), -sin(9.46), cos(9.46), (A)}]"""\
r""" (0.5 cm, 0) -- (0.5 cm, 0.5 cm) -- (0, 0.5 cm);

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
pic [draw, thick, angle radius = 0.5 cm] {angle = X--A--Y}
pic ["\ang{38}", angle eccentricity=1.8, draw, thick, """\
r"""angle radius = 0.58 cm] {angle = X--A--Y};

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
\coordinate (Y) at (2.4,4);

% Draw Angle
\draw[thick] (X1) -- (A) -- (Y1)
pic [draw, thick, angle radius = 0.5 cm, singledash] {angle = X1--A--Y1}
pic ["\ang{38}", angle eccentricity=1.8, draw, thick, """\
r"""angle radius = 0.58 cm, singledash] {angle = X1--A--Y1};
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


def test_drawing_double_decorated_angles():
    P = Point(0, 0, 'P')
    L = Point(0, 2, 'L')
    E = Point('-1.84', '0.8', 'E')
    α = Angle(L, P, E, label_vertex=True, draw_vertex=True,
              label_endpoints=True, draw_endpoints=True,
              label=Number(39, unit=r'\textdegree'))
    α.decoration = AngleDecoration(radius=Number('0.7', unit='cm'),
                                   eccentricity=Number('1.6'))
    α.decoration2 = AngleDecoration(radius=Number('1.6', unit='cm'),
                                    eccentricity=Number('1.3'),
                                    label=Number(42, unit=r'\textdegree'),
                                    color='NavyBlue', do_draw=False,
                                    thickness=None)
    assert α.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (L) at (0,2);
\coordinate (P) at (0,0);
\coordinate (E) at (-1.84,0.8);

% Draw Angle
\draw[thick] (L) -- (P) -- (E)
pic ["\ang{39}", angle eccentricity=1.6, draw, thick, angle """\
r"""radius = 0.7 cm] {angle = L--P--E}
pic ["\ang{42}", angle eccentricity=1.3, angle radius = 1.6 cm, """\
r"""NavyBlue] {angle = L--P--E};
% Draw Vertex
\draw (P) node[scale=0.67] {$\times$};
% Draw End Points
\draw (L) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Label Points
\draw (P) node[below right] {P};
\draw (L) node[above right] {L};
\draw (E) node[below left] {E};
\end{tikzpicture}
"""


def test_AnglesSet_instanciation_errors():
    """Check AnglesSet's instanciation exceptions."""
    pointO = Point(0, 0, 'O')
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
        'the same name in this list: A(0, 0); X1(6, 1); Y1(3, 5); X1(1, 6.5)'


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
\coordinate (Y) at (2.4,4);
\coordinate (Z1) at (1,6.5);
\coordinate (Z) at (0.8,5.2);

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
\coordinate (Y) at (2.4,4);
\coordinate (Z1) at (1,6.5);
\coordinate (Z) at (0.8,5.2);

% Draw Angles
\draw[thick] (X1) -- (A) -- (Y1)
pic ["\ang{38}", angle eccentricity=1.8, draw, thick, """\
r"""angle radius = 0.5 cm, RoyalBlue] {angle = X1--A--Y1};
\draw[thick] (Y1) -- (A) -- (Z1)
pic [draw, thick, angle radius = 0.5 cm, BurntOrange] {angle = Y1--A--Z1}
pic ["\ang{9}", angle eccentricity=1.8, draw, thick, """\
r"""angle radius = 0.58 cm, BurntOrange] {angle = Y1--A--Z1};
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


def test_drawing_AngleSet_same_vertex_and_markright():
    """Check drawing AnglesSets."""
    A = Point(0, 0, 'A')
    X1 = Point(6, 1, 'X1')
    Y1 = Point(-1, 6, 'Y1')
    Z1 = Point(-3, 1, 'Z1')
    α = Angle(X1, A, Y1)
    α.mark_right = True
    β = Angle(Y1, A, Z1)
    S = AnglesSet(α, β)
    assert S.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (X1) at (6,1);
\coordinate (Y1) at (-1,6);
\coordinate (Z1) at (-3,1);

% Draw Angles
\draw[thick] (X1) -- (A) -- (Y1);
\draw[thick] (Y1) -- (A) -- (Z1);
% Mark right Angles
\draw[thick, cm={cos(9.46), sin(9.46), -sin(9.46), cos(9.46), (A)}]"""\
r""" (0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);

% Label Points

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
