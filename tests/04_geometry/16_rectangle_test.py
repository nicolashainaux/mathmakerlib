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

from mathmakerlib.calculus import Number, Unit
from mathmakerlib.geometry import Point, Rectangle


def test_default_instanciation():
    """Check Rectangle's instanciation."""
    r = Rectangle()
    assert r.type == 'Rectangle'
    assert r.width == Number(1)
    assert r.length == Number(2)
    assert r.area == Number(2)


def test_instanciation_from_points():
    """Check Rectangle's instanciation."""
    r = Rectangle(Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1))
    assert r.width == 1
    assert r.length == 1


def test_sides_labeling():
    """Check Rectangle's sides' labeling."""
    r = Rectangle(name='TIDY', width=2, length=3)
    with pytest.raises(ValueError) as excinfo:
        r.lbl_area
    assert str(excinfo.value) == 'No width has been set as a Number.'
    r.setup_labels([Number(4, unit='cm'), '15 cm'])
    with pytest.raises(ValueError) as excinfo:
        r.lbl_length
    assert str(excinfo.value) == 'No length has been set as a Number.'
    with pytest.raises(ValueError) as excinfo:
        r.lbl_area
    assert str(excinfo.value) == 'No length has been set as a Number.'
    r.setup_labels([Number(4, unit='cm'), Number(15, unit='cm')])
    assert r.lbl_width.uiprinted == '4 cm'
    assert r.lbl_length.uiprinted == '15 cm'
    assert r.lbl_area == Number(60, unit=Unit('cm', exponent=Number(2)))
    assert r.lbl_area.uiprinted == '60 cm^2'
    assert [s.label_mask for s in r.sides] == [' ', None, None, ' ']
    for s in r.sides:
        s.unlock_label()
    r.sides[3].label = Number(5, unit='cm')
    with pytest.raises(ValueError) as excinfo:
        r.lbl_area
    assert str(excinfo.value) == 'Two different labels have been set '\
        'for the width: Number(\'4 cm\') and Number(\'5 cm\').'
    r.sides[3].label = Number(4, unit='cm')
    r.sides[2].label = Number(12, unit='cm')
    with pytest.raises(ValueError) as excinfo:
        r.lbl_area
    assert str(excinfo.value) == 'Two different labels have been set '\
        'for the length: Number(\'15 cm\') and Number(\'12 cm\').'
    r.sides[0].label = 'undefined'
    r.sides[1].label = 'undefined'
    assert r.lbl_area.uiprinted == '48 cm^2'
    r.sides[0].label = Number(3, unit='cm')
    r.sides[1].label = Number(17, unit='cm')
    r.sides[2].label = 'undefined'
    r.sides[3].label = 'undefined'
    assert r.lbl_area.uiprinted == '51 cm^2'


def test_simple_drawing():
    """Check drawing the Rectangle."""
    r = Rectangle(name='YOGA')
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (Y) at (0,0);
\coordinate (O) at (2,0);
\coordinate (G) at (2,1);
\coordinate (A) at (0,1);

% Draw Rectangle
\draw[thick] (Y)
-- (O)
-- (G)
-- (A)
-- cycle;

% Mark right angles
\draw[thick, cm={cos(0), sin(0), -sin(0), cos(0), (Y)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(90), sin(90), -sin(90), cos(90), (O)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(180), sin(180), -sin(180), cos(180), (G)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(-90), sin(-90), -sin(-90), cos(-90), (A)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);

% Label Points
\draw (Y) node[below left] {Y};
\draw (O) node[below right] {O};
\draw (G) node[above right] {G};
\draw (A) node[above left] {A};
\end{tikzpicture}
"""
    r = Rectangle(start_vertex=Point(-1, -1), name='YOGA')
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (Y) at (-1,-1);
\coordinate (O) at (1,-1);
\coordinate (G) at (1,0);
\coordinate (A) at (-1,0);

% Draw Rectangle
\draw[thick] (Y)
-- (O)
-- (G)
-- (A)
-- cycle;

% Mark right angles
\draw[thick, cm={cos(0), sin(0), -sin(0), cos(0), (Y)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(90), sin(90), -sin(90), cos(90), (O)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(180), sin(180), -sin(180), cos(180), (G)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(-90), sin(-90), -sin(-90), cos(-90), (A)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);

% Label Points
\draw (Y) node[below left] {Y};
\draw (O) node[below right] {O};
\draw (G) node[above right] {G};
\draw (A) node[above left] {A};
\end{tikzpicture}
"""
    r = Rectangle(name='PLUM', rotation_angle=45)
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (P) at (0.646,-0.561);
\coordinate (L) at (2.061,0.854);
\coordinate (U) at (1.354,1.561);
\coordinate (M) at (-0.061,0.146);

% Draw Rectangle
\draw[thick] (P)
-- (L)
-- (U)
-- (M)
-- cycle;

% Mark right angles
\draw[thick, cm={cos(45), sin(45), -sin(45), cos(45), (P)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(135), sin(135), -sin(135), cos(135), (L)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(-135), sin(-135), -sin(-135), cos(-135), (U)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(-45), sin(-45), -sin(-45), cos(-45), (M)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);

% Label Points
\draw (P) node[below] {P};
\draw (L) node[right] {L};
\draw (U) node[above] {U};
\draw (M) node[left] {M};
\end{tikzpicture}
"""
