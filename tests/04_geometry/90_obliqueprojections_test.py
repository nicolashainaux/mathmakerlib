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

from mathmakerlib.geometry import RightCuboid, ObliqueProjection


def test_instanciation_errors():
    """Check errors when instanciating a new ObliqueProjection."""
    with pytest.raises(TypeError) as excinfo:
        ObliqueProjection(k='a')
    assert str(excinfo.value) == 'Ratio k must be a Number. Found '\
        '\'a\' instead.'
    with pytest.raises(TypeError) as excinfo:
        ObliqueProjection(α='a')
    assert str(excinfo.value) == 'Angle α must be a Number. Found '\
        '\'a\' instead.'
    with pytest.raises(TypeError) as excinfo:
        ObliqueProjection('a')
    assert str(excinfo.value) == 'object3D must be a Polyhedron, found '\
        '\'a\' instead.'


def test_regular_right_cuboid():
    """Check a regular projection of a right cuboid is correct."""
    rc = RightCuboid(dimensions=(4, 3, 2), name='FLAVORED')
    assert ObliqueProjection(rc, label_vertices=True).drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (F) at (0,0);
\coordinate (L) at (4,0);
\coordinate (A) at (4,3);
\coordinate (V) at (0,3);
\coordinate (O) at (0.948,0.948);
\coordinate (R) at (4.948,0.948);
\coordinate (E) at (4.948,3.948);
\coordinate (D) at (0.948,3.948);

% Draw Oblique Projection of RightCuboid
\draw[thick] (F) -- (L);
\draw[thick] (L) -- (A);
\draw[thick] (A) -- (V);
\draw[thick] (V) -- (F);
\draw[thick] (L) -- (R);
\draw[thick, dashed] (R) -- (O);
\draw[thick, dashed] (O) -- (F);
\draw[thick] (A) -- (E);
\draw[thick] (E) -- (R);
\draw[thick] (V) -- (D);
\draw[thick] (D) -- (E);
\draw[thick, dashed] (O) -- (D);


% Label Points
\draw (F) node[below left] {F};
\draw (L) node[below right] {L};
\draw (A) node[above left] {A};
\draw (V) node[left] {V};
\draw (O) node[left] {O};
\draw (R) node[right] {R};
\draw (E) node[above right] {E};
\draw (D) node[above left] {D};
\end{tikzpicture}
"""
