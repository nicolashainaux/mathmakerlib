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

from copy import deepcopy

from mathmakerlib.core.word import Word
from mathmakerlib.calculus.exponented import Exponented

LENGTH_UNITS = ['km', 'hm', 'dam', 'm', 'dm', 'cm', 'mm', 'µm', 'nm', 'pm']
CAPACITY_UNITS = ['kL', 'hL', 'daL', 'L', 'dL', 'cL', 'mL', 'µL', 'nL', 'pL']
MASS_UNITS = ['kg', 'hg', 'dag', 'g', 'dg', 'cg', 'mg', 'µg', 'ng', 'pg']
PHYSICAL_QUANTITIES = {'length': LENGTH_UNITS,
                       'capacity': CAPACITY_UNITS,
                       'mass': MASS_UNITS}
COMMON_LENGTH_UNITS = LENGTH_UNITS[:-3]
COMMON_CAPACITY_UNITS = CAPACITY_UNITS[1:-3]
COMMON_MASS_UNITS = MASS_UNITS[:-3]
ANGLE_UNITS = ['\\textdegree']
CURRENCY_UNITS = ['€', '\officialeuro',
                  '$', '\\textdollar',
                  '£', '\\textsterling']
CURRENCIES_DICT = {'euro': '\officialeuro',
                   'dollar': '\\textdollar',
                   'sterling': '\\textsterling'}
AVAILABLE_UNITS = LENGTH_UNITS + CAPACITY_UNITS + MASS_UNITS + ANGLE_UNITS\
    + CURRENCY_UNITS
UNIT_KINDS = {'length': COMMON_LENGTH_UNITS,
              'mass': COMMON_MASS_UNITS,
              'capacity': COMMON_CAPACITY_UNITS,
              'currency': CURRENCY_UNITS}


def physical_quantity(u):
    """
    Return the physical quantity matching the given unit.

    :parem u: the unit
    :type u: str or Unit
    """
    for pq in PHYSICAL_QUANTITIES:
        if u in PHYSICAL_QUANTITIES[pq]:
            return pq
    return None


class Unit(Exponented):

    def __init__(self, content, exponent=None):
        if isinstance(content, str):
            Exponented.__init__(self, Word(content),
                                exponent=deepcopy(exponent))
        elif isinstance(content, Unit):
            if exponent is None:
                Exponented.__init__(self, deepcopy(content.content),
                                    exponent=deepcopy(content.exponent))
            else:
                Exponented.__init__(self, deepcopy(content.content),
                                    exponent=deepcopy(exponent))
        else:
            raise TypeError('content must be a str or a Unit. Got {} instead.'
                            .format(str(type(content))))

    def __repr__(self):
        return super().__repr__().replace('Exponented', 'Unit')

    def __eq__(self, other):
        if not isinstance(other, Unit):
            return False
        else:
            return (self.content == other.content
                    and self.exponent == other.exponent)

    def __ne__(self, other):
        if not isinstance(other, Unit):
            return True
        else:
            return not (self.content == other.content
                        and self.exponent == other.exponent)
