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

from mathmakerlib import config
from mathmakerlib.geometry import RightCuboid, ObliqueProjection


@pytest.fixture()
def rc(): return RightCuboid(dimensions=(4, 3, 2), name='FLAVORED')


def test_instanciation_ratio_error(rc):
    """Check errors when instanciating a new ObliqueProjection."""
    with pytest.raises(TypeError) as excinfo:
        ObliqueProjection(k='a')
    assert str(excinfo.value) == 'Ratio k must be a number. Found '\
        '\'a\' instead.'


def test_instanciation_angle_error(rc):
    """Check errors when instanciating a new ObliqueProjection."""
    with pytest.raises(TypeError) as excinfo:
        ObliqueProjection(α='a')
    assert str(excinfo.value) == 'Angle α must be a number. Found '\
        '\'a\' instead.'


def test_instanciation_object3D_error(rc):
    """Check errors when instanciating a new ObliqueProjection."""
    with pytest.raises(TypeError) as excinfo:
        ObliqueProjection('a')
    assert str(excinfo.value) == 'object3D must be a Polyhedron, found '\
        '\'a\' instead.'


def test_instanciation_direction_error(rc):
    with pytest.raises(ValueError) as excinfo:
        ObliqueProjection(rc, direction='undefined')
    assert str(excinfo.value) == 'Allowed values for direction argument are '\
        '{}. Found \'undefined\' instead.'.format(config.DIRECTION_VALUES)


def test_label_vertices_error(rc):
    op = ObliqueProjection(rc)
    with pytest.raises(TypeError) as excinfo:
        op.label_vertices = 'true'
    assert str(excinfo.value) == 'label_vertices must be a boolean; '\
        'found <class \'str\'> instead.'


def test_draw_vertices_error(rc):
    op = ObliqueProjection(rc)
    with pytest.raises(TypeError) as excinfo:
        op.draw_vertices = 'true'
    assert str(excinfo.value) == 'draw_vertices must be a boolean; '\
        'found <class \'str\'> instead.'


def test_topright_projection(rc):
    """Check the default projection of a right cuboid is correct."""
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


def test_topleft_projection(rc):
    """Check top-left projection of a right cuboid is correct."""
    assert ObliqueProjection(rc, label_vertices=True,
                             direction='top-left').drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (F) at (0,0);
\coordinate (L) at (4,0);
\coordinate (A) at (4,3);
\coordinate (V) at (0,3);
\coordinate (O) at (-0.948,0.948);
\coordinate (R) at (3.052,0.948);
\coordinate (E) at (3.052,3.948);
\coordinate (D) at (-0.948,3.948);

% Draw Oblique Projection of RightCuboid
\draw[thick] (F) -- (L);
\draw[thick] (L) -- (A);
\draw[thick] (A) -- (V);
\draw[thick] (V) -- (F);
\draw[thick, dashed] (L) -- (R);
\draw[thick, dashed] (R) -- (O);
\draw[thick] (O) -- (F);
\draw[thick] (A) -- (E);
\draw[thick, dashed] (E) -- (R);
\draw[thick] (V) -- (D);
\draw[thick] (D) -- (E);
\draw[thick] (O) -- (D);


% Label Points
\draw (F) node[below] {F};
\draw (L) node[below right] {L};
\draw (A) node[above right] {A};
\draw (V) node[above] {V};
\draw (O) node[below left] {O};
\draw (R) node[below] {R};
\draw (E) node[above] {E};
\draw (D) node[above left] {D};
\end{tikzpicture}
"""


def test_bottomleft_projection(rc):
    """Check bottom-left projection of a right cuboid is correct."""
    assert ObliqueProjection(rc, label_vertices=True,
                             direction='bottom-left').drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (F) at (0,0);
\coordinate (L) at (4,0);
\coordinate (A) at (4,3);
\coordinate (V) at (0,3);
\coordinate (O) at (-0.948,-0.948);
\coordinate (R) at (3.052,-0.948);
\coordinate (E) at (3.052,2.052);
\coordinate (D) at (-0.948,2.052);

% Draw Oblique Projection of RightCuboid
\draw[thick] (F) -- (L);
\draw[thick] (L) -- (A);
\draw[thick] (A) -- (V);
\draw[thick] (V) -- (F);
\draw[thick] (L) -- (R);
\draw[thick] (R) -- (O);
\draw[thick] (O) -- (F);
\draw[thick, dashed] (A) -- (E);
\draw[thick, dashed] (E) -- (R);
\draw[thick] (V) -- (D);
\draw[thick, dashed] (D) -- (E);
\draw[thick] (O) -- (D);


% Label Points
\draw (F) node[left] {F};
\draw (L) node[right] {L};
\draw (A) node[above right] {A};
\draw (V) node[above left] {V};
\draw (O) node[below left] {O};
\draw (R) node[below right] {R};
\draw (E) node[above left] {E};
\draw (D) node[left] {D};
\end{tikzpicture}
"""


def test_bottomright_projection(rc):
    """Check bottom-right projection of a right cuboid is correct."""
    assert ObliqueProjection(rc, label_vertices=True,
                             direction='bottom-right').drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (F) at (0,0);
\coordinate (L) at (4,0);
\coordinate (A) at (4,3);
\coordinate (V) at (0,3);
\coordinate (O) at (0.948,-0.948);
\coordinate (R) at (4.948,-0.948);
\coordinate (E) at (4.948,2.052);
\coordinate (D) at (0.948,2.052);

% Draw Oblique Projection of RightCuboid
\draw[thick] (F) -- (L);
\draw[thick] (L) -- (A);
\draw[thick] (A) -- (V);
\draw[thick] (V) -- (F);
\draw[thick] (L) -- (R);
\draw[thick] (R) -- (O);
\draw[thick] (O) -- (F);
\draw[thick] (A) -- (E);
\draw[thick] (E) -- (R);
\draw[thick, dashed] (V) -- (D);
\draw[thick, dashed] (D) -- (E);
\draw[thick, dashed] (O) -- (D);


% Label Points
\draw (F) node[below left] {F};
\draw (L) node[below] {L};
\draw (A) node[above] {A};
\draw (V) node[above left] {V};
\draw (O) node[below] {O};
\draw (R) node[below right] {R};
\draw (E) node[above right] {E};
\draw (D) node[above] {D};
\end{tikzpicture}
"""


def test_topright_edges_labeling(rc):
    """Check edges' labeling for a top-right projection."""
    rc.setup_labels((4, 7, 25))
    assert ObliqueProjection(rc).drawn == r"""
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
\draw[thick] (F) -- (L) node[midway, below] {4};
\draw[thick] (L) -- (A);
\draw[thick] (A) -- (V);
\draw[thick] (V) -- (F);
\draw[thick] (L) -- (R) node[midway, below right] {7};
\draw[thick, dashed] (R) -- (O);
\draw[thick, dashed] (O) -- (F);
\draw[thick] (A) -- (E);
\draw[thick] (E) -- (R) node[midway, right] {25};
\draw[thick] (V) -- (D);
\draw[thick] (D) -- (E);
\draw[thick, dashed] (O) -- (D);


% Label Points

\end{tikzpicture}
"""


def test_topleft_edges_labeling(rc):
    """Check edges' labeling for a top-left projection."""
    rc.setup_labels((4, 7, 25))
    assert ObliqueProjection(rc, direction='top-left').drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (F) at (0,0);
\coordinate (L) at (4,0);
\coordinate (A) at (4,3);
\coordinate (V) at (0,3);
\coordinate (O) at (-0.948,0.948);
\coordinate (R) at (3.052,0.948);
\coordinate (E) at (3.052,3.948);
\coordinate (D) at (-0.948,3.948);

% Draw Oblique Projection of RightCuboid
\draw[thick] (F) -- (L) node[midway, below] {4};
\draw[thick] (L) -- (A);
\draw[thick] (A) -- (V);
\draw[thick] (V) -- (F);
\draw[thick, dashed] (L) -- (R);
\draw[thick, dashed] (R) -- (O);
\draw[thick] (O) -- (F) node[midway, below left] {7};
\draw[thick] (A) -- (E);
\draw[thick, dashed] (E) -- (R);
\draw[thick] (V) -- (D);
\draw[thick] (D) -- (E);
\draw[thick] (O) -- (D) node[midway, left] {25};


% Label Points

\end{tikzpicture}
"""


def test_bottomleft_edges_labeling(rc):
    """Check edges' labeling for a bottom-left projection."""
    rc.setup_labels((4, 7, 25))
    assert ObliqueProjection(rc, direction='bottom-left').drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (F) at (0,0);
\coordinate (L) at (4,0);
\coordinate (A) at (4,3);
\coordinate (V) at (0,3);
\coordinate (O) at (-0.948,-0.948);
\coordinate (R) at (3.052,-0.948);
\coordinate (E) at (3.052,2.052);
\coordinate (D) at (-0.948,2.052);

% Draw Oblique Projection of RightCuboid
\draw[thick] (F) -- (L);
\draw[thick] (L) -- (A);
\draw[thick] (A) -- (V) node[midway, above] {4};
\draw[thick] (V) -- (F);
\draw[thick] (L) -- (R);
\draw[thick] (R) -- (O);
\draw[thick] (O) -- (F);
\draw[thick, dashed] (A) -- (E);
\draw[thick, dashed] (E) -- (R);
\draw[thick] (V) -- (D) node[midway, above left] {7};
\draw[thick, dashed] (D) -- (E);
\draw[thick] (O) -- (D) node[midway, left] {25};


% Label Points

\end{tikzpicture}
"""


def test_bottomright_edges_labeling(rc):
    """Check edges' labeling for a bottom-right projection."""
    rc.setup_labels((4, 7, 25))
    assert ObliqueProjection(rc, direction='bottom-right').drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (F) at (0,0);
\coordinate (L) at (4,0);
\coordinate (A) at (4,3);
\coordinate (V) at (0,3);
\coordinate (O) at (0.948,-0.948);
\coordinate (R) at (4.948,-0.948);
\coordinate (E) at (4.948,2.052);
\coordinate (D) at (0.948,2.052);

% Draw Oblique Projection of RightCuboid
\draw[thick] (F) -- (L);
\draw[thick] (L) -- (A);
\draw[thick] (A) -- (V) node[midway, above] {4};
\draw[thick] (V) -- (F);
\draw[thick] (L) -- (R);
\draw[thick] (R) -- (O);
\draw[thick] (O) -- (F);
\draw[thick] (A) -- (E) node[midway, above right] {7};
\draw[thick] (E) -- (R) node[midway, right] {25};
\draw[thick, dashed] (V) -- (D);
\draw[thick, dashed] (D) -- (E);
\draw[thick, dashed] (O) -- (D);


% Label Points

\end{tikzpicture}
"""


def test_drawn_vertices(rc):
    """Check the default projection of a right cuboid is correct."""
    assert ObliqueProjection(rc, draw_vertices=True).drawn == r"""
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

% Draw Vertices
\draw (F) node[scale=0.67] {$\times$};
\draw (L) node[scale=0.67] {$\times$};
\draw (A) node[scale=0.67] {$\times$};
\draw (V) node[scale=0.67] {$\times$};
\draw (O) node[scale=0.67] {$\times$};
\draw (R) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};
\draw (D) node[scale=0.67] {$\times$};

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

\end{tikzpicture}
"""


def test_draw_thick_and_blue(rc):
    """Check the default projection of a right cuboid is correct."""
    assert ObliqueProjection(rc, color='RoyalBlue',
                             thickness='very thick').drawn == r"""
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
\draw[very thick, RoyalBlue] (F) -- (L);
\draw[very thick, RoyalBlue] (L) -- (A);
\draw[very thick, RoyalBlue] (A) -- (V);
\draw[very thick, RoyalBlue] (V) -- (F);
\draw[very thick, RoyalBlue] (L) -- (R);
\draw[very thick, RoyalBlue, dashed] (R) -- (O);
\draw[very thick, RoyalBlue, dashed] (O) -- (F);
\draw[very thick, RoyalBlue] (A) -- (E);
\draw[very thick, RoyalBlue] (E) -- (R);
\draw[very thick, RoyalBlue] (V) -- (D);
\draw[very thick, RoyalBlue] (D) -- (E);
\draw[very thick, RoyalBlue, dashed] (O) -- (D);


% Label Points

\end{tikzpicture}
"""
