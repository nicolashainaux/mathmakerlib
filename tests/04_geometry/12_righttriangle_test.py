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

from mathmakerlib.calculus import Number
from mathmakerlib.geometry import Point, LineSegment, RightTriangle


def test_instanciation():
    """Check RightTriangle's instanciation."""
    r = RightTriangle()
    assert r.type == 'RightTriangle'
    assert r.hypotenuse == LineSegment(Point(2, 1), Point(0, 0))
    assert r.right_angle.mark_right
    assert r.right_angle.vertex == Point(2, 0)


def test_simple_drawing():
    """Check drawing the RightTriangle."""
    r = RightTriangle(name='ICY')
    assert r.winding == 'anticlockwise'
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (I) at (0,0);
\coordinate (C) at (2,0);
\coordinate (Y) at (2,1);

% Draw RightTriangle
\draw[thick] (I)
-- (C)
-- (Y)
-- cycle;

% Mark right angles
\draw[thick, cm={cos(90), sin(90), -sin(90), cos(90), (C)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);

% Label Points
\draw (I) node[left] {I};
\draw (C) node[below right] {C};
\draw (Y) node[above right] {Y};
\end{tikzpicture}
"""
    r = RightTriangle(start_vertex=Point(-3, 4), name='ICY')
    assert r.winding == 'anticlockwise'
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (I) at (-3,4);
\coordinate (C) at (-1,4);
\coordinate (Y) at (-1,5);

% Draw RightTriangle
\draw[thick] (I)
-- (C)
-- (Y)
-- cycle;

% Mark right angles
\draw[thick, cm={cos(90), sin(90), -sin(90), cos(90), (C)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);

% Label Points
\draw (I) node[left] {I};
\draw (C) node[below right] {C};
\draw (Y) node[above right] {Y};
\end{tikzpicture}
"""
    r = RightTriangle(start_vertex=Point(-3, 4), name='ICY',
                      winding='clockwise')
    r.setup_labels([Number(3, unit='cm'),
                    Number(4, unit='cm'),
                    Number(5, unit='cm')])
    assert r.winding == 'clockwise'
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (I) at (-1,5);
\coordinate (C) at (-1,4);
\coordinate (Y) at (-3,4);

% Draw RightTriangle
\draw[thick] (I)
-- (C) node[midway, above, sloped] {\SI{3}{cm}}
-- (Y) node[midway, below, sloped] {\SI{4}{cm}}
-- cycle node[midway, above, sloped] {\SI{5}{cm}};

% Mark right angles
\draw[thick, cm={cos(180), sin(180), -sin(180), cos(180), (C)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, -0.25 cm) -- (0, -0.25 cm);

% Label Points
\draw (I) node[above right] {I};
\draw (C) node[below right] {C};
\draw (Y) node[left] {Y};
\end{tikzpicture}
"""
