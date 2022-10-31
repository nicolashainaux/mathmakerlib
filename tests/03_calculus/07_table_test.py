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
from mathmakerlib.calculus import Table


def test_instanciation_errors():
    with pytest.raises(ValueError) as excinfo:
        Table([1])
    assert str(excinfo.value) == \
        'Only tables of 2, 3 or 4 columns may be created so far; but got '\
        '1 couple(s).'
    with pytest.raises(TypeError):
        Table([1, 2])
    with pytest.raises(ValueError) as excinfo:
        Table([(1, ), (2, )])
    assert str(excinfo.value) == \
        'Only couples may be provided to build a table, '\
        'got one tuple, at least, of length != 2'


def test_instanciation():
    t2 = Table([(1, 2), (3, 4)])
    t3 = Table([(1, 2), (3, 4), (5, 6)])
    t4 = Table([(1, 2), (3, 4), (5, 6), (7, 8)])
    assert t2.size == 2
    assert t3.size == 3
    assert t4.size == 4
    assert t2.xoffset == '2.5'
    assert t3.xoffset == '4'
    assert t4.xoffset == '5.5'
    assert 'XVAL3' in t4.template
    assert 'XVAL3' not in t3.template
    assert t2.bubble == ''
    assert t3.bubble == ''
    assert t4.bubble == ''


def test_bubble():
    t2 = Table([(1, 2), (3, 4)], bubble_value='?')
    assert '×?' in t2.bubble
    t3 = Table([(1, 2), (3, 4), (5, 6)], bubble_operator='+', bubble_value='4',
               bubble_color='OliveGreen')
    assert r'\textcolor{OliveGreen}{+4}' in t3.bubble


def test_imprint(mocker):
    m = mocker.patch('mathmakerlib.calculus.Table.bubble',
                     new_callable=mocker.PropertyMock)
    m.side_effect = ['SOME_CONTENT']
    required.package['tikz'] = False
    t4 = Table([('v1', 'v2'), ('v3', 'v4'), ('v5', 'v6'), ('v7', 'v8')],
               bubble_value='?')
    output = t4.printed
    assert required.package['tikz']
    assert 'v1' in output
    assert 'v2' in output
    assert 'v3' in output
    assert 'v4' in output
    assert 'v5' in output
    assert 'v6' in output
    assert 'v7' in output
    assert 'v8' in output
    assert 'SOME_CONTENT' in output
    assert 'baseline' not in output
    m.side_effect = ['SOME_CONTENT']
    required.package['tikz'] = False
    t4 = Table([('v1', 'v2'), ('v3', 'v4'), ('v5', 'v6'), ('v7', 'v8')],
               bubble_value='?', compact=True, baseline=3)
    output = t4.printed
    assert required.package['tikz']
    assert 'v1' in output
    assert 'v2' in output
    assert 'v3' in output
    assert 'v4' in output
    assert 'v5' in output
    assert 'v6' in output
    assert 'v7' in output
    assert 'v8' in output
    assert 'SOME_CONTENT' in output
    assert 'baseline=3pt' in output
