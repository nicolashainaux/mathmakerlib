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

from mathmakerlib import config
from mathmakerlib.calculus.clocktime import DEFAULT_CLOCKTIME_CONTEXT
from mathmakerlib.calculus import ClockTime
from mathmakerlib.calculus.clocktime import check_clocktime_context


@pytest.fixture()
def ct(): return ClockTime(15, 24, 16)


def test_config_global_context():
    """Check setting up the global clocktime context"""
    config.clocktime.CONTEXT = DEFAULT_CLOCKTIME_CONTEXT


def test_check_context_typeerror():
    """Check check_clocktime_context()"""
    with pytest.raises(TypeError) as excinfo:
        check_clocktime_context(('h', 'min', 's'))
    assert str(excinfo.value) == 'context must be a dict. '\
        'Found <class \'tuple\'> instead.'


def test_check_context_keyerror():
    """Check check_clocktime_context()"""
    with pytest.raises(KeyError) as excinfo:
        check_clocktime_context({'hour': 3})
    assert str(excinfo.value) == '"keys of context must belong to {}; found '\
        '\'hour\' instead."'.format(set(DEFAULT_CLOCKTIME_CONTEXT.keys()))


def test_instanciation_error():
    """Check the ClockTime class initialization"""
    with pytest.raises(TypeError) as excinfo:
        ClockTime(15.2, 24, 16)
    assert str(excinfo.value) == 'hour, minute and second must be '\
        '<class \'int\'>. Found <class \'float\'>, <class \'int\'> and '\
        '<class \'int\'> instead.'


def test_str(ct):
    """Check the ClockTime class initialization"""
    assert str(ct) == '15:24:16'


def test_instanciation_from_another_clocktime(ct):
    """Check the ClockTime class initialization"""
    ct2 = ClockTime(ct)
    assert str(ct2) == '15:24:16'


def test_hash(ct):
    """Check the ClockTime class initialization"""
    hash(ct)


def test_context(ct):
    """Check the ClockTime class initialization"""
    assert ct.context == DEFAULT_CLOCKTIME_CONTEXT


def test_negative_second_instanciation():
    """Check the ClockTime class initialization"""
    t = ClockTime(15, 24, -16)
    assert str(t) == '15:23:44'


def test_negative_minute_and_second_instanciation():
    """Check the ClockTime class initialization"""
    t = ClockTime(15, -24, -16)
    assert str(t) == '14:35:44'


def test_negative_instanciation():
    """Check the ClockTime class initialization"""
    t = ClockTime(-15, -24, -16)
    assert str(t) == '08:35:44'


def test_leading_zeros():
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
    ct = ClockTime(15, 24, 16, context={'sep': 'as_si_units'})
    assert ct.printed == r'15~\si{h}~24~\si{min}~16~\si{s}'


def test_0h_not_printed_in_si_units():
    """Check ClockTime imprint()"""
    ct = ClockTime(0, 24, 0,
                   context={'sep': 'as_si_units', 'si_show_0h': False,
                            'si_show_0min': False, 'si_show_0s': False})
    assert ct.printed == r'24~\si{min}'


def test_0h_24min_30s_printed():
    """Check ClockTime imprint()"""
    ct = ClockTime(0, 24, 30)
    assert ct.printed == '00:24:30'
    ct = ClockTime(0, 24, 30, context={'h_padding': False})
    assert ct.printed == '0:24:30'


def test_24min_30s_printed():
    """Check ClockTime imprint()"""
    ct = ClockTime(0, 24, 30,
                   context={'sep': 'as_si_units', 'si_only_central': True,
                            'si_show_0h': False})
    assert ct.printed == r'24~\si{min}~30'


def test_30s_printed():
    """Check ClockTime imprint()"""
    ct = ClockTime(0, 0, 30,
                   context={'sep': 'as_si_units', 'si_show_0h': False,
                            'si_show_0min': False, 'si_show_0s': False})
    assert ct.printed == r'30~\si{s}'


def test_0min_printed():
    """Check ClockTime imprint()"""
    ct = ClockTime(0, 0, 0,
                   context={'sep': 'as_si_units', 'si_zero_as': 'min',
                            'si_show_0h': False, 'si_show_0min': False,
                            'si_show_0s': False})
    assert ct.printed == r'0~\si{min}'


def test_4min_printed():
    """Check ClockTime imprint()"""
    ct = ClockTime(0, 4, 0,
                   context={'sep': 'as_si_units', 'si_show_0h': False,
                            'si_show_0min': False, 'si_show_0s': False})
    assert ct.printed == r'4~\si{min}'


def test_1h_04min_printed():
    """Check ClockTime imprint()"""
    ct = ClockTime(1, 4, 0,
                   context={'sep': 'as_si_units', 'si_only_central': True,
                            'si_show_0s': False})
    assert ct.printed == r'1~\si{h}~04'
