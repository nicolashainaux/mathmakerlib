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

from mathmakerlib.calculus import Number
from mathmakerlib.geometry import Point, Triangle, AngleDecoration
from mathmakerlib.constants import LOCALE_US, LOCALE_FR


def test_instanciation_errors():
    """Check errors on Triangle's instanciation."""
    with pytest.raises(ValueError) as excinfo:
        Triangle(Point(0, 0), Point(0, 1))
    assert str(excinfo.value) == 'Three vertices are required to build a '\
        'Triangle. Found 2 instead.'


def test_instanciation():
    """Check Triangle's instanciation."""
    r = Triangle(Point(0, 0), Point(0, 1), Point(1, 1))
    assert r.type == 'Triangle'


def test_simple_drawing():
    """Check drawing the Triangle."""
    r = Triangle(Point(0, 0), Point(1, 0), Point(1, 1), name='BOT')
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (B) at (0,0);
\coordinate (O) at (1,0);
\coordinate (T) at (1,1);

% Draw Triangle
\draw[thick] (B)
-- (O)
-- (T)
-- cycle;

% Label Points
\draw (B) node[below left] {B};
\draw (O) node[below right] {O};
\draw (T) node[above] {T};
\end{tikzpicture}
"""


def test_drawing_with_labeled_sides():
    """Check drawing the Triangle."""
    r = Triangle(Point(0, 0), Point(1, 0), Point(0, 1),
                 name='WAX')
    with pytest.raises(ValueError) as excinfo:
        r.setup_labels(labels=['one', 'two', 'three', 'four'])
    assert str(excinfo.value) == 'All three labels must be setup. Found '\
        '4 values instead.'
    with pytest.raises(ValueError) as excinfo:
        r.setup_labels(masks=[None, None])
    assert str(excinfo.value) == 'All three masks must be setup. Found '\
        '2 values instead.'
    r.setup_labels(labels=['one', 'two', 'three'])
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (W) at (0,0);
\coordinate (A) at (1,0);
\coordinate (X) at (0,1);

% Draw Triangle
\draw[thick] (W)
-- (A) node[midway, below, sloped] {one}
-- (X) node[midway, above, sloped] {two}
-- cycle node[midway, below, sloped] {three};

% Label Points
\draw (W) node[below left] {W};
\draw (A) node[right] {A};
\draw (X) node[above left] {X};
\end{tikzpicture}
"""
    t = Triangle(Point(0, 0), Point(2, 0),
                 Point(Number('0.776'), Number('1.232')),
                 name='BOT', label_vertices=False, thickness='thin')
    t.setup_labels(labels=[Number(4, unit='cm'),
                           Number('3.5', unit='cm'),
                           Number(3, unit='cm')])
    for s in t.sides:
        s.label_scale = '0.9'
    assert t.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (B) at (0,0);
\coordinate (O) at (2,0);
\coordinate (T) at (0.776,1.232);

% Draw Triangle
\draw[thin] (B)
-- (O) node[midway, below, sloped, scale=0.9] {\SI{4}{cm}}
-- (T) node[midway, above, sloped, scale=0.9] {\SI{3.5}{cm}}
-- cycle node[midway, above, sloped, scale=0.9] {\SI{3}{cm}};

% Label Points

\end{tikzpicture}
"""
    t = Triangle(Point(0, 0), Point(2, 0), Point(2, 1),
                 name='BOT', label_vertices=False, thickness='thin')
    t.setup_labels(labels=[Number(9, unit='dam'),
                           Number(8, unit='dam'),
                           Number(4, unit='dam')])
    for s in t.sides:
        s.label_scale = '0.85'
    assert t.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (B) at (0,0);
\coordinate (O) at (2,0);
\coordinate (T) at (2,1);

% Draw Triangle
\draw[thin] (B)
-- (O) node[midway, below, sloped, scale=0.85] {\SI{9}{dam}}
-- (T) node[midway, below, sloped, scale=0.85] {\SI{8}{dam}}
-- cycle node[midway, above, sloped, scale=0.85] {\SI{4}{dam}};

% Label Points

\end{tikzpicture}
"""
    t = Triangle(Point(0, 0), Point('2.236', 0), Point('0.582', '0.98'),
                 name='ABC', label_vertices=False)
    t.setup_labels(labels=[Number(10, unit='hm'),
                           Number(6, unit='hm'),
                           Number(5, unit='hm')])
    for s in t.sides:
        s.label_scale = '0.85'
    t.angles[1].decoration = AngleDecoration()
    t.angles[1].mark_right = True
    locale.setlocale(locale.LC_ALL, LOCALE_FR)
    assert t.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (B) at (2.236,0);
\coordinate (C) at (0.582,0.98);

% Draw Triangle
\draw[thick] (A)
-- (B) node[midway, below, sloped, scale=0.85] {\SI{10}{hm}}
-- (C) node[midway, above, sloped, scale=0.85] {\SI{6}{hm}}
-- cycle node[midway, above, sloped, scale=0.85] {\SI{5}{hm}};

% Mark right angles
\draw[thick, """\
r"""cm={cos(149.35), sin(149.35), -sin(149.35), cos(149.35), (B)}] """\
                      r"""(0.25 cm, 0) -- (0.25 cm, 0.25 cm) -- (0, 0.25 cm);

% Label Points

\end{tikzpicture}
"""
    locale.setlocale(locale.LC_ALL, LOCALE_US)
    t = Triangle(Point(0, '-0.4'), Point(0, '0.4'), Point('2', 0),
                 name='MNO', label_vertices=False, thickness='thin')
    t.setup_labels(labels=[Number(5, unit='hm'),
                           Number(9, unit='hm'),
                           Number(9, unit='hm')],
                   masks=[None, ' ', None])
    for s in t.sides:
        s.label_scale = '0.85'
        s.mark_scale = Number('0.5')
    t.sides[1].mark = t.sides[2].mark = '||'
    assert t.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (M) at (0,-0.4);
\coordinate (N) at (0,0.4);
\coordinate (O) at (2,0);

% Draw Triangle
\draw[thin] (M)
-- (N) node[midway, above, sloped, scale=0.85] {\SI{5}{hm}}
-- (O) node[midway, sloped, scale=0.5] {||}
-- cycle node[midway, below, sloped, scale=0.85] {\SI{9}{hm}} """\
r"""node[midway, sloped, scale=0.5] {||};

% Label Points

\end{tikzpicture}
"""
