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

from abc import ABCMeta, abstractmethod

from mathmakerlib.calculus.number import Number
from mathmakerlib.core.drawable import Drawable


class Equilateral(Drawable, metaclass=ABCMeta):

    def __init__(self, mark_equal_sides=True, use_mark='||'):
        if mark_equal_sides:
            for s in self.sides:
                s.mark = use_mark

    @property
    @abstractmethod
    def sides(self):
        """The sides of the object."""

    @property
    def lbl_side_length(self):
        collected_values = []
        for s in self.sides:
            if isinstance(s.label_value, Number):
                collected_values.append(s.label_value)
        if not collected_values:
            raise ValueError('Found no side labeled as a Number.')
        ref = collected_values[0]
        for v in collected_values:
            if v != ref:
                raise ValueError('Found different values for the sides: {} '
                                 'and {}.'.format(repr(ref), repr(v)))
        return ref

    @property
    def default_masks(self):
        return [' ' for _ in range(len(self.sides) - 1)] + [None]
