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
from mathmakerlib.core import Callout


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
