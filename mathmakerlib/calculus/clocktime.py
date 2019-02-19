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

from copy import deepcopy

from mathmakerlib import config
from mathmakerlib.calculus import Unit
from mathmakerlib.calculus.tools import is_integer
from mathmakerlib.core.printable import Printable

DEFAULT_CLOCKTIME_CONTEXT = {'h_padding': True, 'min_padding': True,
                             's_padding': True, 'show_0s': True, 'sep': ':',
                             'si_show_0h': True, 'si_show_0min': True,
                             'si_show_0s': True, 'si_only_central': False,
                             'si_zero_as': 's'}


def check_clocktime_context(value):
    if not isinstance(value, dict):
        raise TypeError('context must be a dict. Found {} instead.'
                        .format(type(value)))
    for key in value:
        if key not in DEFAULT_CLOCKTIME_CONTEXT:
            raise KeyError('keys of context must belong to {}; found '
                           '{} instead.'
                           .format(set(DEFAULT_CLOCKTIME_CONTEXT.keys()),
                                   repr(key)))


class ClockTime(Printable):
    """hour:minute:second objects ranging from 00:00:00 to 23:59:59"""

    def __new__(cls, hour=0, minute=0, second=0, context=None):
        if isinstance(hour, ClockTime):
            if context is None:
                context = hour.context
            hour, minute, second = hour.hour, hour.minute, hour.second
        if any(not is_integer(value) for value in [hour, minute, second]):
            raise TypeError('hour, minute and second must be <class \'int\'>. '
                            'Found {}, {} and {} instead.'
                            .format(type(hour), type(minute), type(second)))
        if second < 0:
            minute -= abs(second) // 60 + 1
        if second >= 60:
            minute += second // 60
        second = second % 60
        if minute < 0:
            hour -= abs(minute) // 60 + 1
        if minute >= 60:
            hour += minute // 60
        minute = minute % 60
        hour = hour % 24
        self = super().__new__(cls)
        self._hour, self._minute, self._second = hour, minute, second
        self._context = deepcopy(config.clocktime.CONTEXT)
        if context is not None:
            check_clocktime_context(context)
            self._context.update(context)
        return self

    @property
    def hour(self):
        return self._hour

    @property
    def minute(self):
        return self._minute

    @property
    def second(self):
        return self._second

    @property
    def context(self):
        return self._context

    def __repr__(self):
        return f'ClockTime({self.hour:02}:{self.minute:02}:{self.second:02})'

    def __str__(self):
        return f'{self.hour:02}:{self.minute:02}:{self.second:02}'

    def __eq__(self, other):
        if isinstance(other, ClockTime):
            return (self.hour == other.hour and self.minute == other.minute
                    and self.second == other.second)
        else:
            return False

    def __gt__(self, other):
        return (self.hour, self.minute, self.second) \
            > (other.hour, other.minute, other.second)

    def __lt__(self, other):
        return (self.hour, self.minute, self.second) \
            < (other.hour, other.minute, other.second)

    def __ge__(self, other):
        return (self.hour, self.minute, self.second) \
            >= (other.hour, other.minute, other.second)

    def __le__(self, other):
        return (self.hour, self.minute, self.second) \
            <= (other.hour, other.minute, other.second)

    def __hash__(self):
        return hash(repr(self))

    def __add__(self, other):
        if not isinstance(other, ClockTime):
            raise TypeError('Only a ClockTime can be added to a ClockTime. '
                            'Found {} instead.'.format(type(other)))
        return ClockTime(self.hour + other.hour,
                         self.minute + other.minute,
                         self.second + other.second)

    def __sub__(self, other):
        if not isinstance(other, ClockTime):
            raise TypeError('Only a ClockTime can be subtracted from a '
                            'ClockTime. Found {} instead.'.format(type(other)))
        return ClockTime(self.hour - other.hour,
                         self.minute - other.minute,
                         self.second - other.second)

    # DEFAULT_CLOCKTIME_CONTEXT = {'h_padding': True, 'min_padding': True,
    #                              's_padding': True, 'show_0s': True,
    #                              'sep': ':',
    #                              'si_show_0h': True, 'si_show_0min': True,
    #                              'si_show_0s': True,
    #                              'si_only_central': False,
    #                              'si_zero_as': 's'}
    def imprint(self, start_expr=True, variant='latex'):
        output = []
        zero_h = self.hour == 0
        zero_min = self.minute == 0
        zero_s = self.second == 0
        # /!\ padding is ignored for the first unit to be displayed in the
        # case of 'as_si_units'. E.g. 2 hours will be displayed 2 h, not 02 h
        hours_fmt = '{:02}' if self.context['h_padding'] else '{}'
        minutes_fmt = '{:02}' if self.context['min_padding'] else '{}'
        seconds_fmt = '{:02}' if self.context['s_padding'] else '{}'
        hours = hours_fmt.format(self.hour)
        minutes = minutes_fmt.format(self.minute)
        seconds = seconds_fmt.format(self.second)
        displayed_anything = False
        if self.context['sep'] == 'as_si_units':
            if zero_h and zero_min and zero_s:
                output.append('0')
                output.append(Unit(self.context['si_zero_as']).printed)
            if not zero_h or (zero_h and self.context['si_show_0h']):
                hours = '{}'.format(self.hour)
                output.append(hours)
                output.append(Unit('h').printed)
                displayed_anything = True
            if not zero_min or (zero_min and self.context['si_show_0min']):
                if not displayed_anything:
                    minutes = '{}'.format(self.minute)
                output.append(minutes)
                if not(zero_s and self.context['si_only_central']):
                    output.append(Unit('min').printed)
                displayed_anything = True
            if not zero_s or (zero_s and self.context['si_show_0s']):
                if not displayed_anything:
                    seconds = '{}'.format(self.second)
                output.append(seconds)
                if not(zero_h and self.context['si_only_central']):
                    output.append(Unit('s').printed)
                displayed_anything = True
            output = '~'.join(output)
        else:  # For instance, sep == ':'
            output = [hours, minutes]
            if (zero_s and self.context['show_0s']) or not zero_s:
                output.append(seconds)
            output = self.context['sep'].join(output)
        return output
