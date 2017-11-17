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

from mathmakerlib import requires_pkg
from mathmakerlib.geometry import Point, LineSegment


@pytest.fixture()
def A():
    return Point(0, 0, 'A')


@pytest.fixture()
def E():
    return Point(1, 0, 'E')


def test_scale(A, E):
    """Check drawing is correct."""
    ls = LineSegment(A, E)
    assert ls.scale == 1
    ls.scale = 2
    assert ls.scale == 2
    assert ls.drawn == r"""
\begin{tikzpicture}[scale=2]
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,0);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[left] {A};
\draw (E) node[right] {E};
\end{tikzpicture}
"""
    with pytest.raises(TypeError) as excinfo:
        ls.scale = '2'
    assert str(excinfo.value) == 'The scale must be a number.'


def test_colors():
    """Check colors setting and usage."""
    p = Point(0, 0, 'A')
    requires_pkg.xcolor_options = []
    requires_pkg.xcolor = False
    p.color = 'blue'
    assert not requires_pkg.xcolor
    assert 'dvipsnames' not in requires_pkg.xcolor_options
    with pytest.raises(ValueError) as excinfo:
        p.color = 'UndefinedBlueOrange'
    assert str(excinfo.value) == 'Unknown color name: UndefinedBlueOrange. ' \
        'Only colors from xcolor\'s dvipsnames are yet supported.'
    assert not requires_pkg.xcolor
    assert 'dvipsnames' not in requires_pkg.xcolor_options
    p.color = 'Apricot'
    assert requires_pkg.xcolor
    assert 'dvipsnames' in requires_pkg.xcolor_options
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Point
\coordinate (A) at (0,0);

% Draw Point
\draw[Apricot] (A) node {$\times$};

% Label Point
\draw (A) node[below] {A};
\end{tikzpicture}
"""


def test_baseline(A, E):
    """Check baseline setting and usage."""
    ls = LineSegment(A, E)
    assert ls.baseline is None
    ls.baseline = '4pt'
    assert ls.baseline == '4pt'
    assert ls.drawn == r"""
\begin{tikzpicture}[baseline=4pt]
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,0);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[left] {A};
\draw (E) node[right] {E};
\end{tikzpicture}
"""
    ls.scale = 2
    assert ls.drawn == r"""
\begin{tikzpicture}[baseline=4pt, scale=2]
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,0);

% Draw Points
\draw (A) node {$\times$};
\draw (E) node {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[left] {A};
\draw (E) node[right] {E};
\end{tikzpicture}
"""
