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

from mathmakerlib.calculus import Number
from mathmakerlib.geometry import XAxis


def test_instanciation():
    a = XAxis(2, 4, subdivisions=3)
    assert a._sg_abscissae == [Number(0.67), Number(1.33), 2,
                               Number(2.67), Number(3.33), 4,
                               Number(4.67), Number(5.33), 6,
                               Number(6.67), Number(7.33)]
    assert a._mg_abscissae == [2, 4, 6]
    assert a._mg_labels == ['2', '3', '4']
    assert a.template_fmt == \
        {'__LENGTH__': '8',
         '__SG_ABSCISSAE__': '{0.67,1.33,2,2.67,3.33,4,4.67,5.33,6,6.67,7.33}',
         '__MG_ABSCISSAE_TEXTS__': r'{2/\text{2},4/\text{3},6/\text{4}}',
         '__POINTS_DRAWN__': ''
         }
    assert a.drawn == r"""\begin{tikzpicture}

\draw[-latex, thick] (0,0) -- (8,0);

% subgraduations
\foreach \x in {0.67,1.33,2,2.67,3.33,4,4.67,5.33,6,6.67,7.33} {
\draw (\x,0.09cm) -- (\x,-0.09cm);
}

% major graduations
\foreach \x/\xtext in {2/\text{2},4/\text{3},6/\text{4}} {
\draw[thick] (\x,0.12cm) -- (\x,-0.12cm) node[below] {$\xtext\strut$};
}

\end{tikzpicture}
"""
