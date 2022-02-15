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

from mathmakerlib.calculus import Number, Fraction
from mathmakerlib.geometry import XAxis
from mathmakerlib.constants import LOCALE_US, LOCALE_FR


def test_instanciation():
    a = XAxis(2, 4, subdivisions=3)
    assert a._sg_abscissae == [Number(0.67), Number(1.33), 2,
                               Number(2.67), Number(3.33), 4,
                               Number(4.67), Number(5.33), 6,
                               Number(6.67), Number(7.33)]
    assert a._mg_abscissae == [2, 4, 6]
    assert a._mg_labels == ['2', '3', '4']
    assert a.template_fmt['__TIKZ_PICTURE_OPTIONS__'] == ''
    a.baseline = '-4pt'
    assert a.template_fmt == \
        {'__TIKZ_PICTURE_OPTIONS__': '[baseline=-4pt]',
         '__LENGTH__': '8',
         '__SG_ABSCISSAE__': '{0.67,1.33,2,2.67,3.33,4,4.67,5.33,6,6.67,7.33}',
         '__MG_ABSCISSAE_TEXTS__': r'{2/2,4/3,6/4}',
         '__POINTS_DRAWN__': ''
         }
    # TODO: replace the *.drawn tests by integration tests checking the
    # produced code is compilable. But still check the template_fmt produced
    # in different cases: floats provided as abscissae, comma in mg_labels
    # (see c object test, below), Fractions provided (see object b...) etc.
    assert a.drawn == r"""\begin{tikzpicture}[baseline=-4pt]

\draw[-latex, thick] (0,0) -- (8,0);

% subgraduations
\foreach \x in {0.67,1.33,2,2.67,3.33,4,4.67,5.33,6,6.67,7.33} {
\draw (\x,0.09cm) -- (\x,-0.09cm);
}

% major graduations
\foreach \x/\xtext in {2/2,4/3,6/4} {
\draw[thick] (\x,0.12cm) -- (\x,-0.12cm) node[below] {$\xtext\strut$};
}

\end{tikzpicture}
"""
    b = XAxis(0, 1, subdivisions=7, points_def=[(Fraction(2, 7), 'A'),
                                                (Fraction(5, 7), 'Z')])
    assert b._mg_abscissae == [Number('0'), Number('5.6')]
    assert b._mg_labels == ['0', '1']
    assert b.drawn == r"""\begin{tikzpicture}

\draw[-latex, thick] (0,0) -- (8,0);

% subgraduations
\foreach \x in {0.8,1.6,2.4,3.2,4,4.8,5.6,6.4,7.2} {
\draw (\x,0.09cm) -- (\x,-0.09cm);
}

% major graduations
\foreach \x/\xtext in {0/0,5.6/1} {
\draw[thick] (\x,0.12cm) -- (\x,-0.12cm) node[below] {$\xtext\strut$};
}
\draw[thick] (1.6,0) node {$\times$} node[above] {A};
\draw[thick] (4,0) node {$\times$} node[above] {Z};
\end{tikzpicture}
"""
    locale.setlocale(locale.LC_ALL, LOCALE_FR)
    c = XAxis(0.1, 0.3, step=0.1, subdivisions=5,
              points_def=[(0.14, 'A'), (0.28, 'Z')])
    assert c._mg_labels == ['0,1', '0,2', '0,3']
    assert c.drawn == r"""\begin{tikzpicture}

\draw[-latex, thick] (0,0) -- (8,0);

% subgraduations
\foreach \x in {0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5} {
\draw (\x,0.09cm) -- (\x,-0.09cm);
}

% major graduations
\foreach \x/\xtext in {1.5/{0,1},4/{0,2},6.5/{0,3}} {
\draw[thick] (\x,0.12cm) -- (\x,-0.12cm) node[below] {$\xtext\strut$};
}
\draw[thick] (2.5,0) node {$\times$} node[above] {A};
\draw[thick] (6,0) node {$\times$} node[above] {Z};
\end{tikzpicture}
"""
    locale.setlocale(locale.LC_ALL, LOCALE_US)
