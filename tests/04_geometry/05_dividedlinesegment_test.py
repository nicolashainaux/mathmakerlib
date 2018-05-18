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

from mathmakerlib.geometry import Point, DividedLineSegment


def test_instanciation_errors():
    """Check DividedLineSegment's instanciation exceptions."""
    A = Point(0, 0, 'A')
    B = Point(10, 0, 'B')
    with pytest.raises(TypeError) as excinfo:
        DividedLineSegment(A, B)
    assert str(excinfo.value) == 'n must be an integer >= 1, got None instead.'
    with pytest.raises(TypeError) as excinfo:
        DividedLineSegment(A, B, n=3, fill=4)
    assert str(excinfo.value) == 'fill must be an 1 <= integer <= self.n == ' \
        '3, got 4 instead.'


def test_instanciation():
    """Check LineSegment's instanciation."""
    A = Point(0, 0, 'A')
    B = Point(10, 0, 'B')
    s = DividedLineSegment(A, B, n=5, fill=3)
    assert s.thickness == 'ultra thick'
    assert s.label is None
    assert s.label_mask is None
    assert s.endpoints[0].shape == '|'
    assert s.endpoints[1].shape == '|'


def test_repr():
    """Check __repr__ is correct."""
    A = Point(0, 0, 'A')
    B = Point(10, 0, 'B')
    assert repr(DividedLineSegment(A, B, n=4, fill=3)) \
        == 'DividedLineSegment(Point A(0, 0), Point B(10, 0), 3/4, LimeGreen)'


def test_drawing():
    """Check drawing is correct."""
    A = Point(0, 0, 'A')
    B = Point(10, 0, 'B')
    ls = DividedLineSegment(A, B, n=5, fill=3, fillcolor='pink')
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (B) at (10,0);
\coordinate (a3) at (6,0);

% Draw Divided Line Segment
\draw[ultra thick] (A) -- (B);
\draw[ultra thick, pink] (A) -- (a3);
\draw[ultra thick, opacity=0] (A) -- (B) """\
r"""node[opacity=1, pos=0, sloped] {|} """\
                       r"""node[opacity=1, pos=0.2, sloped] {|} """\
                       r"""node[opacity=1, pos=0.4, sloped] {|} """\
                       r"""node[opacity=1, pos=0.6, sloped] {|} """\
                       r"""node[opacity=1, pos=0.8, sloped] {|} """\
                       r"""node[opacity=1, pos=1, sloped] {|};

% Label Points

\end{tikzpicture}
"""
