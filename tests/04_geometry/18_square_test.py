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


from mathmakerlib import config
from mathmakerlib.calculus import Number
from mathmakerlib.geometry import Square


def test_instanciation():
    """Check Square's instanciation."""
    s = Square()
    assert s.type == 'Square'
    assert s.width == s.length == s.side_length == Number(1)
    assert s.area == Number(1)


def test_lbl_area():
    """Check Square's sides' labeling."""
    r = Square(name='DUCK', side_length=3)
    r.setup_labels([Number('1.5', unit='cm')])
    assert r.lbl_area.uiprinted == '2.25 cm^2'


def test_simple_drawing():
    """Check drawing the Square."""
    r = Square(name='GEMS')
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (G) at (0,0);
\coordinate (E) at (1,0);
\coordinate (M) at (1,1);
\coordinate (S) at (0,1);

% Draw Square
\draw[thick] (G)
-- (E) node[midway, sloped, scale=0.5] {||}
-- (M) node[midway, sloped, scale=0.5] {||}
-- (S) node[midway, sloped, scale=0.5] {||}
-- cycle node[midway, sloped, scale=0.5] {||};

% Mark right angles
\draw[thick, cm={cos(0), sin(0), -sin(0), cos(0), (G)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(90), sin(90), -sin(90), cos(90), (E)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(180), sin(180), -sin(180), cos(180), (M)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(-90), sin(-90), -sin(-90), cos(-90), (S)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);

% Label Points
\draw (G) node[below left] {G};
\draw (E) node[below right] {E};
\draw (M) node[above right] {M};
\draw (S) node[above left] {S};
\end{tikzpicture}
"""
    r.setup_labels([Number(5, unit='cm')], masks=[None, None, None, None])
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (G) at (0,0);
\coordinate (E) at (1,0);
\coordinate (M) at (1,1);
\coordinate (S) at (0,1);

% Draw Square
\draw[thick] (G)
-- (E) node[midway, below, sloped] {\SI{5}{cm}}"""\
r""" node[midway, sloped, scale=0.5] {||}
-- (M) node[midway, below, sloped] {\SI{5}{cm}}"""\
r""" node[midway, sloped, scale=0.5] {||}
-- (S) node[midway, above, sloped] {\SI{5}{cm}}"""\
r""" node[midway, sloped, scale=0.5] {||}
-- cycle node[midway, below, sloped] {\SI{5}{cm}}"""\
r""" node[midway, sloped, scale=0.5] {||};

% Mark right angles
\draw[thick, cm={cos(0), sin(0), -sin(0), cos(0), (G)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(90), sin(90), -sin(90), cos(90), (E)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(180), sin(180), -sin(180), cos(180), (M)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);
\draw[thick, cm={cos(-90), sin(-90), -sin(-90), cos(-90), (S)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);

% Label Points
\draw (G) node[below left] {G};
\draw (E) node[below right] {E};
\draw (M) node[above right] {M};
\draw (S) node[above left] {S};
\end{tikzpicture}
"""
    config.polygons.ENABLE_MISMATCH_WINDING_WARNING = False
    r = Square(name='GEMS', winding='clockwise')
    config.polygons.ENABLE_MISMATCH_WINDING_WARNING = True
    r.setup_labels([Number(5, unit='cm')], masks=[None, None, None, None])
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (G) at (0,1);
\coordinate (E) at (1,1);
\coordinate (M) at (1,0);
\coordinate (S) at (0,0);

% Draw Square
\draw[thick] (G)
-- (E) node[midway, above, sloped] {\SI{5}{cm}}"""\
r""" node[midway, sloped, scale=0.5] {||}
-- (M) node[midway, above, sloped] {\SI{5}{cm}}"""\
r""" node[midway, sloped, scale=0.5] {||}
-- (S) node[midway, below, sloped] {\SI{5}{cm}}"""\
r""" node[midway, sloped, scale=0.5] {||}
-- cycle node[midway, above, sloped] {\SI{5}{cm}}"""\
r""" node[midway, sloped, scale=0.5] {||};

% Mark right angles
\draw[thick, cm={cos(0), sin(0), -sin(0), cos(0), (G)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, -0.25 cm) -- (0, -0.25 cm);
\draw[thick, cm={cos(-90), sin(-90), -sin(-90), cos(-90), (E)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, -0.25 cm) -- (0, -0.25 cm);
\draw[thick, cm={cos(180), sin(180), -sin(180), cos(180), (M)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, -0.25 cm) -- (0, -0.25 cm);
\draw[thick, cm={cos(90), sin(90), -sin(90), cos(90), (S)}] """\
r"""(0.25 cm, 0) -- (0.25 cm, -0.25 cm) -- (0, -0.25 cm);

% Label Points
\draw (G) node[above left] {G};
\draw (E) node[above right] {E};
\draw (M) node[below right] {M};
\draw (S) node[below left] {S};
\end{tikzpicture}
"""
