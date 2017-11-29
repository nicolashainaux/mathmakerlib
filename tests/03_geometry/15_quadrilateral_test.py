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

from mathmakerlib.geometry import Point, Quadrilateral


def test_instanciation_errors():
    """Check erros on Quadrilateral's instanciation."""
    with pytest.raises(ValueError) as excinfo:
        Quadrilateral(Point(0, 0), Point(0, 1), Point(1, 1))
    assert str(excinfo.value) == 'Four vertices are required to build a '\
        'Quadrilateral. Found 3 instead.'


def test_instanciation():
    """Check Quadrilateral's instanciation."""
    r = Quadrilateral(Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0))
    assert r.type == 'Quadrilateral'


def test_simple_drawing():
    """Check drawing the Quadrilateral."""
    r = Quadrilateral(Point(0, 0), Point(1, 0), Point(2, 2), Point(0, 3),
                      name='PINK')
    assert r.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (P) at (0,0);
\coordinate (I) at (1,0);
\coordinate (N) at (2,2);
\coordinate (K) at (0,3);

% Draw Quadrilateral
\draw[thick] (P)
-- (I)
-- (N)
-- (K)
-- cycle;

% Label Points
\draw (P) node[below left] {P};
\draw (I) node[below right] {I};
\draw (N) node[right] {N};
\draw (K) node[above left] {K};
\end{tikzpicture}
"""
