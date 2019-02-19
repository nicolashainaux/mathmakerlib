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

import pytest

from mathmakerlib import required
from mathmakerlib.calculus import Number
from mathmakerlib.core.drawable import ARROW_TIPS
from mathmakerlib.core.drawable import HasRadius, HasThickness, HasArrowTips
from mathmakerlib.core.drawable import tikz_options_list, tikz_approx_position
from mathmakerlib.geometry import Point, LineSegment, Angle, AngleDecoration


@pytest.fixture()
def A():
    return Point(0, 0, 'A')


@pytest.fixture()
def E():
    return Point(1, 0, 'E')


def test_tikz_approx_position():
    """Check tikz_approx_position() results."""
    assert tikz_approx_position(-65) == 'below right'


def test_tikz_options_list():
    """Check tikz_options_list()"""
    with pytest.raises(TypeError) as excinfo:
        tikz_options_list('draw')
    assert str(excinfo.value) == 'Expected a Drawable, found <class ' \
        '\'NoneType\'>.'
    assert tikz_options_list([None, None]) == ''
    assert tikz_options_list(['attr1=val1', 'val2']) == '[attr1=val1, val2]'
    assert tikz_options_list(['attr1=val1', None, 'val2']) \
        == '[attr1=val1, val2]'


def test_hasradius():
    """Check abstract class HasRadius"""
    class FakeCircle(HasRadius):
        pass
    o = FakeCircle()
    assert o.radius is None
    o.radius = Number(3, unit='cm')
    assert o.radius.printed == '\\SI{3}{cm}'
    with pytest.raises(TypeError) as excinfo:
        o.radius = '2'
    assert str(excinfo.value) == 'Expected a number as radius. Got '\
        '<class \'str\'> instead.'


def test_hasthickness():
    """Check abstract class HasThickness"""
    class FakeLineSegment(HasThickness):
        pass
    o = FakeLineSegment()
    assert o.thickness is None


def test_hasarrowtips():
    """Check abstract class HasArrowTips"""
    class FakeLineSegment(HasArrowTips):
        pass
    o = FakeLineSegment()
    assert o.arrow_tips is None
    with pytest.raises(ValueError) as excinfo:
        o.arrow_tips = '2'
    assert str(excinfo.value) == 'Incorrect arrow_tips value: \'2\'. '\
        'Available values belong to: {}.'.format(str(ARROW_TIPS))


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
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[left] {A};
\draw (E) node[right] {E};
\end{tikzpicture}
"""
    with pytest.raises(TypeError) as excinfo:
        ls.scale = '2'
    assert str(excinfo.value) == 'The picture\'s scale must be a number.'


def test_colors():
    """Check colors setting and usage."""
    p = Point(0, 0, 'A')
    required.options['xcolor'] = set()
    required.package['xcolor'] = False
    p.color = 'blue'
    assert not required.package['xcolor']
    assert 'dvipsnames' not in required.options['xcolor']
    with pytest.raises(ValueError) as excinfo:
        p.color = 'UndefinedBlueOrange'
    assert str(excinfo.value) == 'Unknown color name: UndefinedBlueOrange. ' \
        'Only colors from xcolor\'s dvipsnames are yet supported.'
    assert not required.package['xcolor']
    assert 'dvipsnames' not in required.options['xcolor']
    p.color = 'Apricot'
    assert required.package['xcolor']
    assert 'dvipsnames' in required.options['xcolor']
    assert p.drawn == r"""
\begin{tikzpicture}
% Declare Point
\coordinate (A) at (0,0);

% Draw Point
\draw[Apricot] (A) node[scale=0.67] {$\times$};

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
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

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
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[left] {A};
\draw (E) node[right] {E};
\end{tikzpicture}
"""


def test_fontsize():
    """Check fontsize is taken into account, if it exists."""
    A = Point(0, 0, 'A')
    X = Point(2, '0.33', 'X')
    Y = Point(1, '1.67', 'Y')
    α = Angle(X, A, Y, label=Number(38, unit=r'\textdegree'),
              label_vertex=True)
    assert α.fontsize is None
    with pytest.raises(ValueError) as excinfo:
        α.fontsize = 'undefined'
    assert str(excinfo.value) == "TikZ font size must be None or belong to "\
        r"['\\tiny', '\\scriptsize', '\\footnotesize', '\\small', "\
        r"'\\normalsize', '\\large', '\\Large', '\\LARGE', '\\huge', "\
        r"'\\Huge']. Found 'undefined' instead."
    assert α.fontsize is None
    α.decoration = AngleDecoration(radius=None,
                                   eccentricity=Number('1.8'))
    α.fontsize = r'\scriptsize'
    assert α.drawn == r"""
\begin{tikzpicture}
% Text font size
\scriptsize
% Declare Points
\coordinate (X) at (2,0.33);
\coordinate (A) at (0,0);
\coordinate (Y) at (1,1.67);

% Draw Angle
\draw[thick] (X) -- (A) -- (Y)
pic ["\ang{38}", angle eccentricity=1.8, draw, thick] {angle = X--A--Y};

% Label Points
\draw (A) node[below left] {A};
\end{tikzpicture}
"""


def test_boundingbox(A, E):
    """Check boundingbox setting and usage."""
    ls = LineSegment(A, E)
    assert ls.boundingbox is None
    with pytest.raises(TypeError) as excinfo:
        ls.boundingbox = [1, 2, 3, 4]
    assert str(excinfo.value) == 'Expected a tuple, found a list instead.'
    with pytest.raises(ValueError) as excinfo:
        ls.boundingbox = (1, 2, 3)
    assert str(excinfo.value) == 'Expected a tuple of 4 elements, found 3 '\
        'elements instead.'
    with pytest.raises(TypeError) as excinfo:
        ls.boundingbox = (1, 2, 3, 'a')
    assert str(excinfo.value) == 'Expected a tuple containing only numbers. '\
        'Found a str instead.'
    ls.boundingbox = (-1, -1, '2', 1)
    assert ls.boundingbox == (-1, -1, 2, 1)
    assert ls.drawn == r"""
\begin{tikzpicture}
% Declare Points
\coordinate (A) at (0,0);
\coordinate (E) at (1,0);

% Draw Points
\draw (A) node[scale=0.67] {$\times$};
\draw (E) node[scale=0.67] {$\times$};

% Draw Line Segment
\draw[thick] (A) -- (E);

% Label Points
\draw (A) node[left] {A};
\draw (E) node[right] {E};

\useasboundingbox (-1,-1) rectangle (2,1);
\end{tikzpicture}
"""
