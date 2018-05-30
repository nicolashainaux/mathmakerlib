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

from .tools import is_number, is_integer, is_natural, prime_factors
from .exponented import Exponented
from .number import Sign, Number, move_fracdigits_to, remove_fracdigits_from
from .number import fix_fracdigits
from .unit import Unit, physical_quantity, difference_of_orders_of_magnitude
from .fraction import Fraction
from .clocktime import ClockTime

__all__ = ['is_number', 'is_integer', 'is_natural', 'Exponented', 'Sign',
           'Number', 'move_fracdigits_to', 'remove_fracdigits_from',
           'fix_fracdigits', 'Unit', 'physical_quantity',
           'difference_of_orders_of_magnitude',
           'Fraction', 'prime_factors',
           'ClockTime']
