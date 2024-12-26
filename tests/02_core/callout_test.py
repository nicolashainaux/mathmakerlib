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
from mathmakerlib.core import Callout
from mathmakerlib.core.callout import _average_triple
from mathmakerlib.core.callout import callout_positioning


def test_callout_instanciation_error():
    with pytest.raises(ValueError) as excinfo:
        Callout('Some text', 2, 35, absolute_pointer='A',
                relative_pointer=(1, 1))
    assert str(excinfo.value) == 'Exactly one among absolute_pointer and '\
        'relative_pointer must be None. Instead, got "A" and "(1, 1)".'


def test_callout_generate_tikz_with_relative_pointer():
    co = Callout('Some text', 2, 35, style=None, relative_pointer=(-1, -1))
    assert co.generate_tikz() == \
        r'\node[callout relative pointer={(-1,-1)}] at (35:2) {Some text};'
    assert required.package['tikz']
    assert required.tikz_library['shapes.geometric']
    assert required.tikz_library['shapes.callouts']
    assert required.tikz_library['arrows.meta']
    assert required.tikz_library['positioning']
    assert not required.callout_style['callout_style1']


def test_callout_generate_tikz_with_absolute_pointer():
    co = Callout('Some text', 2, 35, style=None, absolute_pointer='A')
    assert co.generate_tikz() == \
        r'\node[callout absolute pointer=(A)] at (35:2) {Some text};'


def test_callout_generate_tikz():
    co = Callout(r'\textcolor{CornflowerBlue}{n°1 : \dots\dots} '
                 r'\vrule width 0pt height 0.4cm',
                 4, 14, absolute_pointer='A', shorten='2cm',
                 color='BurntOrange', thickness='thin',
                 fillcolor='OliveGreen!20')
    assert co.generate_tikz() == \
        r'\node[callout absolute pointer=(A), callout_style1, callout '\
        r'pointer shorten=2cm, draw=BurntOrange, thin, fill=OliveGreen!20] '\
        r'at (14:4) {\textcolor{CornflowerBlue}{n°1 : \dots\dots} \vrule '\
        r'width 0pt height 0.4cm};'
    assert required.callout_style['callout_style1']

    co = Callout(r'\textcolor{CornflowerBlue}{n°1 : \dots\dots} '
                 r'\vrule width 0pt height 0.4cm',
                 4, 14, absolute_pointer='A', shorten='2cm', thickness='thick',
                 fillcolor='OliveGreen!20')
    assert co.generate_tikz() == \
        r'\node[callout absolute pointer=(A), callout_style1, callout '\
        r'pointer shorten=2cm, draw, thick, fill=OliveGreen!20] '\
        r'at (14:4) {\textcolor{CornflowerBlue}{n°1 : \dots\dots} \vrule '\
        r'width 0pt height 0.4cm};'

    co = Callout(r'n°2 : \dots\dots\dots \vrule width 0pt height 0.5cm',
                 '2.4', 60, absolute_pointer='B', shorten='0.9cm',
                 fillcolor='CornflowerBlue!20')
    assert co.generate_tikz() == \
        r'\node[callout absolute pointer=(B), callout_style1, '\
        r'callout pointer shorten=0.9cm, fill=CornflowerBlue!20] at (60:2.4) '\
        r'{n°2 : \dots\dots\dots \vrule width 0pt height 0.5cm};'


def test_average_triple():
    with pytest.raises(ValueError) as excinfo:
        _average_triple(5)
    assert str(excinfo.value) == 'Value expected to be 5 < value < 80; and '\
        'not to be in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 80], '\
        'but got: 5'
    assert _average_triple(28) == (Number('1.952'), Number('1.1'),
                                   Number('0.683'))


def test_callout_positioning():
    # tests only for the default arms_lengths == 6 cm;
    # values might need to be adjusted for other arms_lengths.
    assert callout_positioning(5) == (1, Number('7.75'), Number('5.75'))
    assert callout_positioning(40) == (3, Number('5.2'), Number('2.7'))
    assert callout_positioning(60) == (7, 4, Number('1.5'))
    assert callout_positioning(80) == (7, 3, 1)
    assert callout_positioning(120) == (7, 3, 1)
    assert callout_positioning(28) == (Number('1.952'), Number('6.6'),
                                       Number('4.1'))
    assert callout_positioning(70) == (7, Number('3.5'), Number('1.25'))
