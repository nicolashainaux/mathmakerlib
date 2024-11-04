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

# import pytest

from mathmakerlib.calculus import Number
from mathmakerlib.calculus.equations import PythagoreanEquation
from mathmakerlib.geometry import RightTriangle


def test_PythagoreanEquation():
    r = RightTriangle(name='ABC')
    r.setup_labels(labels=[Number(3, unit='cm'),
                           Number(4, unit='cm'),
                           None],
                   masks=[None, None, ' '])
    assert PythagoreanEquation(r).printed == \
        r'\text{CA}^{2}=\text{AB}^{2}+\text{BC}^{2}'
    assert PythagoreanEquation(r).autosolve('hyp') == \
        r"""\[\text{CA}^{2}=\text{AB}^{2}+\text{BC}^{2}\]
\[\text{CA}^{2}=3^{2}+4^{2}\]
\[\text{CA}^{2}=25\]
\[\text{CA}=\sqrt{\mathstrut 25}\text{ because CA is positive.}\]
\[\uline{\text{CA}=\SI{5}{cm}}\]"""
