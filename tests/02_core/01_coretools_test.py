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

from mathmakerlib.core import surrounding_keys, parse_layout_descriptor


def test_surrounding_keys_errors():
    with pytest.raises(ValueError) as excinfo:
        surrounding_keys(1, {})
    assert str(excinfo.value) == 'Expected at least 2 keys, only found 0'
    with pytest.raises(ValueError) as excinfo:
        surrounding_keys(1, {'a': 4})
    assert str(excinfo.value) == 'Expected at least 2 keys, only found 1'
    with pytest.raises(ValueError) as excinfo:
        surrounding_keys(1, {3: 'a', 2: 'b'})
    assert str(excinfo.value) == 'Expected the keys to be in ascending order,'\
        ' but got these keys: [3, 2]'
    d = {1: 'a', 5: 'b', 10: 'c'}
    with pytest.raises(ValueError) as excinfo:
        surrounding_keys(0, d)
    assert str(excinfo.value) == 'Value expected to be 1 < value < 10; and '\
        'not to be in [1, 5, 10], but got: 0'
    with pytest.raises(ValueError) as excinfo:
        surrounding_keys(1, d)
    assert str(excinfo.value) == 'Value expected to be 1 < value < 10; and '\
        'not to be in [1, 5, 10], but got: 1'
    with pytest.raises(ValueError) as excinfo:
        surrounding_keys(5, d)
    assert str(excinfo.value) == 'Value expected to be 1 < value < 10; and '\
        'not to be in [1, 5, 10], but got: 5'
    with pytest.raises(ValueError) as excinfo:
        surrounding_keys(10, d)
    assert str(excinfo.value) == 'Value expected to be 1 < value < 10; and '\
        'not to be in [1, 5, 10], but got: 10'
    with pytest.raises(ValueError) as excinfo:
        surrounding_keys(12, d)
    assert str(excinfo.value) == 'Value expected to be 1 < value < 10; and '\
        'not to be in [1, 5, 10], but got: 12'


def test_surrounding_keys():
    d = {1: 'a', 5: 'b', 10: 'c'}
    assert surrounding_keys(2, d) == (1, 5)


def test_parse_layout_descriptor():
    """Test parse_layout_descriptor() in several cases."""
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor(4)
    assert str(excinfo.value) == 'Cannot find the separator "×" in '\
        'string "4".'
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2×3', sep=[1])
    assert str(excinfo.value) == 'Cannot find the separator "[1]" in '\
        'string "2×3".'
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2×3', sep=1)
    assert str(excinfo.value) == 'Cannot find the separator "1" in '\
        'string "2×3".'
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2×3', min_row='a')
    assert 'invalid literal' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2×3', min_col='a')
    assert 'invalid literal' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2×')
    assert str(excinfo.value) == 'The layout descriptor is expected to '\
        'contain two values separated by "×"'
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2x3')
    assert str(excinfo.value) == 'Cannot find the separator "×" in '\
        'string "2x3".'
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2;')
    assert str(excinfo.value) == 'Cannot find the separator "×" in '\
        'string "2;".'
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2×3', sep=['x'])
    assert str(excinfo.value) == 'Cannot find the separator "[\'x\']" in '\
        'string "2×3".'
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('2×3', sep=['x', '×'])
    assert str(excinfo.value) == 'Cannot find the separator "[\'x\', \'×\']" '\
        'in string "2×3".'
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('a×3')
    assert 'invalid literal' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('3×a')
    assert 'invalid literal' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('?×3')
    assert 'invalid literal' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('0×3', min_row=1)
    assert 'nrow must be greater than 1' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        parse_layout_descriptor('4×0', min_col=1)
    assert 'ncol must be greater than 1' in str(excinfo.value)

    assert parse_layout_descriptor('2×3', special_row_chars=4) == (2, 3)
    assert parse_layout_descriptor('?×0', special_row_chars=['?'],
                                   min_row=1) == ('?', 0)
    assert parse_layout_descriptor('4×5') == (4, 5)
    assert parse_layout_descriptor('6×7', special_row_chars=['?']) == (6, 7)
    assert parse_layout_descriptor('2×3', min_row=-2) == (2, 3)
    assert parse_layout_descriptor('2×3', min_col=-2) == (2, 3)
