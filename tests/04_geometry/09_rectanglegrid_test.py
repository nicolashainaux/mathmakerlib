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

import random

from mathmakerlib.geometry import RectangleGrid

# To ensure reproducible tests when startvertex='random'
random.seed(42)


def test_example_1():
    r = RectangleGrid(layout='6×4', fill='3×2', startvertex='topleft')
    expected = r"""\begin{tikzpicture}
  \draw[fill=lightgray] (0, 6) rectangle (2, 3);
  \draw[step=1cm] (0, 0) grid (4, 6);
\end{tikzpicture}"""
    assert r.draw() == expected


def test_example_2():
    r = RectangleGrid(layout='6×4', fill='2×3', startvertex='bottomright')
    assert r._get_complement_rectangle_coordinates() is None
    expected = r"""\begin{tikzpicture}
  \draw[fill=lightgray] (4, 0) rectangle (1, 2);
  \draw[step=1cm] (0, 0) grid (4, 6);
\end{tikzpicture}"""
    assert r.draw() == expected


def test_example_3():
    r = RectangleGrid(layout='10×10', fill='3×5', startvertex='topleft')
    expected = r"""\begin{tikzpicture}
  \draw[fill=lightgray] (0, 10) rectangle (5, 7);
  \draw[step=1cm] (0, 0) grid (10, 10);
\end{tikzpicture}"""
    assert r.draw() == expected


def test_example_4():
    r = RectangleGrid(layout='10×10', fill='4×6', startvertex='topright')
    expected = r"""\begin{tikzpicture}
  \draw[fill=lightgray] (10, 10) rectangle (4, 6);
  \draw[step=1cm] (0, 0) grid (10, 10);
\end{tikzpicture}"""
    assert r.draw() == expected


def test_example_5():
    r = RectangleGrid(layout='10×10', fill='6×4', startvertex='bottomright')
    expected = r"""\begin{tikzpicture}
  \draw[fill=lightgray] (10, 0) rectangle (6, 6);
  \draw[step=1cm] (0, 0) grid (10, 10);
\end{tikzpicture}"""
    assert r.draw() == expected


def test_example_6():
    r = RectangleGrid(layout='10×10', fill='7×8', startvertex='bottomleft')
    expected = r"""\begin{tikzpicture}
  \draw[fill=lightgray] (0, 0) rectangle (8, 7);
  \draw[step=1cm] (0, 0) grid (10, 10);
\end{tikzpicture}"""
    assert r.draw() == expected


def test_example_7():
    r = RectangleGrid(layout='5×7', fill='9×9', startvertex='bottomleft')
    expected = r"""\begin{tikzpicture}
  \draw[fill=lightgray] (0, 0) rectangle (7, 5);
  \draw[step=1cm] (0, 0) grid (7, 5);
\end{tikzpicture}"""
    assert r.draw() == expected


def test_example_8a():
    r = RectangleGrid(layout='3×8', fill='4×5', startvertex='bottomleft')
    expected = r"""\begin{tikzpicture}
  \draw[fill=lightgray] (0, 0) rectangle (8, 3);
  \draw[fill=white] (8, 3) rectangle (6, 1);
  \draw[step=1cm] (0, 0) grid (8, 3);
\end{tikzpicture}"""
    assert r.draw() == expected


def test_example_8b():
    r = RectangleGrid(layout='3×8', fill='4×5', startvertex='bottomright')
    expected = r"""\begin{tikzpicture}
  \draw[fill=lightgray] (0, 0) rectangle (8, 3);
  \draw[fill=white] (0, 3) rectangle (2, 1);
  \draw[step=1cm] (0, 0) grid (8, 3);
\end{tikzpicture}"""
    assert r.draw() == expected


def test_example_8c():
    r = RectangleGrid(layout='3×8', fill='4×5', startvertex='topright')
    expected = r"""\begin{tikzpicture}
  \draw[fill=lightgray] (0, 0) rectangle (8, 3);
  \draw[fill=white] (0, 0) rectangle (2, 2);
  \draw[step=1cm] (0, 0) grid (8, 3);
\end{tikzpicture}"""
    assert r.draw() == expected


def test_example_8d():
    r = RectangleGrid(layout='3×8', fill='4×5', startvertex='topleft')
    expected = r"""\begin{tikzpicture}
  \draw[fill=lightgray] (0, 0) rectangle (8, 3);
  \draw[fill=white] (8, 0) rectangle (6, 2);
  \draw[step=1cm] (0, 0) grid (8, 3);
\end{tikzpicture}"""
    assert r.draw() == expected


def test_example_9():
    r = RectangleGrid(layout='3×8', fill='9×2', startvertex='topleft')
    expected = r"""\begin{tikzpicture}
  \draw[fill=lightgray] (0, 3) rectangle (6, 0);
  \draw[step=1cm] (0, 0) grid (8, 3);
\end{tikzpicture}"""
    assert r.draw() == expected


def test_no_fill():
    r = RectangleGrid(layout='3×4', fill='0×0', startvertex='topleft')
    expected = r"""\begin{tikzpicture}
  \draw[step=1cm] (0, 0) grid (4, 3);
\end{tikzpicture}"""
    assert r.draw() == expected
    assert r._get_filled_rectangle_coordinates() == (0, 0, 0, 0)


def test_random_startvertex():
    # With the seed set, ‘random’ should give a predictable choice
    r = RectangleGrid(layout='5×5', fill='2×2', startvertex='random')
    # Just check that it doesn't raise any errors
    r.draw()


def test_different_fillcolor():
    r = RectangleGrid(layout='3×3', fill='2×2', fillcolor='red',
                      startvertex='topleft')
    expected = r"""\begin{tikzpicture}
  \draw[fill=red] (0, 3) rectangle (2, 1);
  \draw[step=1cm] (0, 0) grid (3, 3);
\end{tikzpicture}"""
    assert r.draw() == expected


def test_swapped_dimensions():
    # Test where the original dimensions don't work, but they do once they've
    # been exchanged
    r = RectangleGrid(layout='3×8', fill='4×2', startvertex='bottomleft')
    expected = r"""\begin{tikzpicture}
  \draw[fill=lightgray] (0, 0) rectangle (4, 2);
  \draw[step=1cm] (0, 0) grid (8, 3);
\end{tikzpicture}"""
    assert r.draw() == expected


def test_disabled_methods():
    r = RectangleGrid(layout='6×4', fill='3×2', startvertex='topleft')
    assert r._tikz_draw_options() is None
    assert r.tikz_declarations() is None
    assert r.tikz_draw() is None
    assert r.tikz_drawing_comment() is None
    assert r.tikz_label() == ''
    assert r.tikz_points_labels() is None
