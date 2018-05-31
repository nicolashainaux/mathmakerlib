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

from mathmakerlib import mmlib_setup
from mathmakerlib.calculus.clocktime import DEFAULT_CLOCKTIME_CONTEXT
from mathmakerlib.calculus import ClockTime
from mathmakerlib.calculus.clocktime import check_clocktime_context


@pytest.fixture()
def ct(): return ClockTime(15, 24, 16)


def test_setup_global_clocktime_context():
    """Check setting up the global clocktime context"""
    mmlib_setup.clocktime.context = DEFAULT_CLOCKTIME_CONTEXT


def test_check_clocktime_context_typeerror():
    """Check check_clocktime_context()"""
    with pytest.raises(TypeError) as excinfo:
        check_clocktime_context(('h', 'min', 's'))
    assert str(excinfo.value) == 'context must be a dict. '\
        'Found <class \'tuple\'> instead.'


def test_check_clocktime_context_keyerror():
    """Check check_clocktime_context()"""
    with pytest.raises(KeyError) as excinfo:
        check_clocktime_context({'hour': 3})
    assert str(excinfo.value) == '"keys of context must belong to {}; found '\
        '\'hour\' instead."'.format(set(DEFAULT_CLOCKTIME_CONTEXT.keys()))


def test_clocktime_instanciation_error(ct):
    """Check the ClockTime class initialization"""
    with pytest.raises(TypeError) as excinfo:
        ClockTime(15.2, 24, 16)
    assert str(excinfo.value) == 'hour, minute and second must be '\
        '<class \'int\'>. Found <class \'float\'>, <class \'int\'> and '\
        '<class \'int\'> instead.'


def test_clocktime_str(ct):
    """Check the ClockTime class initialization"""
    assert str(ct) == '15:24:16'


def test_clocktime_hash(ct):
    """Check the ClockTime class initialization"""
    hash(ct)


def test_clocktime_context(ct):
    """Check the ClockTime class initialization"""
    assert ct.context == DEFAULT_CLOCKTIME_CONTEXT


def test_negative_second_clocktime_instanciation():
    """Check the ClockTime class initialization"""
    t = ClockTime(15, 24, -16)
    assert str(t) == '15:23:44'


def test_negative_minute_and_second_clocktime_instanciation():
    """Check the ClockTime class initialization"""
    t = ClockTime(15, -24, -16)
    assert str(t) == '14:35:44'


def test_negative_clocktime_instanciation():
    """Check the ClockTime class initialization"""
    t = ClockTime(-15, -24, -16)
    assert str(t) == '08:35:44'


def test_clocktime_leading_zeros():
    """Check leading zeros"""
    assert str(ClockTime(1, 2, 9)) == '01:02:09'


def test_repr():
    """Check ClockTime __repr__()"""
    assert repr(ClockTime(23, 6, 3)) == 'ClockTime(23:06:03)'


def test_inequality():
    """Check ClockTime __eq__()"""
    assert ClockTime(23, 6, 3) != 'ClockTime(23:06:03)'


def test_equality():
    """Check ClockTime __eq__()"""
    t1 = ClockTime(23, 6, 3)
    t2 = ClockTime(23, 6, 3)
    assert t1 == t2


def test_greater_than():
    """Check ClockTime __gt__()"""
    t1 = ClockTime(23, 6, 3)
    t2 = ClockTime(23, 6, 4)
    assert t2 > t1


def test_lower_than():
    """Check ClockTime __lt__()"""
    t1 = ClockTime(23, 6, 3)
    t2 = ClockTime(23, 6, 4)
    assert t1 < t2


def test_greater_or_equal():
    """Check ClockTime __ge__()"""
    t1 = ClockTime(23, 6, 3)
    t2 = ClockTime(23, 6, 4)
    assert t2 >= t1


def test_lower_or_equal():
    """Check ClockTime __le__()"""
    t1 = ClockTime(23, 6, 3)
    t2 = ClockTime(23, 6, 4)
    assert t1 <= t2


def test_addition_error():
    """Check ClockTime __add__()"""
    with pytest.raises(TypeError) as excinfo:
        ClockTime(6, 39, 25) + (3, 50, 44)
    assert str(excinfo.value) == 'Only a ClockTime can be added to a '\
        'ClockTime. Found <class \'tuple\'> instead.'


def test_regular_addition():
    """Check ClockTime __add__()"""
    assert ClockTime(6, 39, 25) + ClockTime(0, 11, 12) \
        == ClockTime(6, 50, 37)


def test_addition():
    """Check ClockTime __add__()"""
    assert ClockTime(6, 39, 25) + ClockTime(3, 50, 44) \
        == ClockTime(10, 30, 9)


def test_exceeding_day_addition():
    """Check ClockTime __add__()"""
    assert ClockTime(21, 30, 0) + ClockTime(5, 20, 40) \
        == ClockTime(2, 50, 40)


def test_subtraction_error():
    """Check ClockTime __sub__()"""
    with pytest.raises(TypeError) as excinfo:
        ClockTime(6, 39, 25) - (3, 50, 44)
    assert str(excinfo.value) == 'Only a ClockTime can be subtracted from a '\
        'ClockTime. Found <class \'tuple\'> instead.'


def test_regular_subtraction():
    """Check ClockTime __sub__()"""
    assert ClockTime(6, 39, 25) - ClockTime(0, 11, 12) \
        == ClockTime(6, 28, 13)


def test_subtraction():
    """Check ClockTime __sub__()"""
    assert ClockTime(6, 39, 25) - ClockTime(2, 41, 26) \
        == ClockTime(3, 57, 59)


def test_exceeding_day_subtraction():
    """Check ClockTime __sub__()"""
    assert ClockTime(5, 20, 40) - ClockTime(21, 30, 0) \
        == ClockTime(7, 50, 40)


def test_clocktime_printed(ct):
    """Check ClockTime imprint()"""
    assert ct.printed == '15:24:16'


def test_custom_context_clocktime_printed():
    """Check ClockTime imprint()"""
    ct = ClockTime(15, 24, 16, context={'h': 'h ', 'min': '', 's': '',
                                        'display_h': True, 'display_min': True,
                                        'display_s': False})
    assert ct.printed == '15h 24'
