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
from decimal import Decimal

from mathmakerlib import required
from mathmakerlib.core.word import Word
from mathmakerlib.calculus.exponented import Exponented

LENGTH_UNITS = ['km', 'hm', 'dam', 'm', 'dm', 'cm', 'mm', 'µm', 'nm', 'pm']
CAPACITY_UNITS = ['kL', 'hL', 'daL', 'L', 'dL', 'cL', 'mL', 'µL', 'nL', 'pL']
MASS_UNITS = ['t', 'kg', 'hg', 'dag', 'g', 'dg', 'cg', 'mg', 'µg', 'ng', 'pg']
VOLUME_CAPACITY_MATCH = ['m', '', '', 'dm', '', '', 'cm', '', '', 'mm']
COMMON_LENGTH_UNITS = LENGTH_UNITS[:-3]
COMMON_CAPACITY_UNITS = CAPACITY_UNITS[1:-3]
COMMON_MASS_UNITS = MASS_UNITS[:-3]
ANGLE_UNITS = ['\\textdegree']
CURRENCY_UNITS = ['€', r'\officialeuro',
                  '$', r'\textdollar',
                  '£', r'\textsterling']
CURRENCIES_DICT = {'euro': r'\officialeuro',
                   'dollar': r'\textdollar',
                   'sterling': r'\textsterling'}
AVAILABLE_UNITS = LENGTH_UNITS + CAPACITY_UNITS + MASS_UNITS + ANGLE_UNITS\
    + CURRENCY_UNITS
UNIT_KINDS = {'length': COMMON_LENGTH_UNITS,
              'mass': COMMON_MASS_UNITS,
              'capacity': COMMON_CAPACITY_UNITS,
              'currency': CURRENCY_UNITS}
PHYSICAL_QUANTITIES = {'length': LENGTH_UNITS,
                       'area': LENGTH_UNITS,
                       'volume': LENGTH_UNITS,
                       'capacity': CAPACITY_UNITS,
                       'mass': MASS_UNITS,
                       'currency': CURRENCY_UNITS,
                       'angle': ANGLE_UNITS}


def physical_quantity(u):
    """
    Return the physical quantity matching the given unit.

    :param u: the unit
    :type u: str or Unit
    """
    e = 1
    if isinstance(u, Unit):
        e = u.exponent
        u = str(u.content)
    for pq in PHYSICAL_QUANTITIES:
        if u in PHYSICAL_QUANTITIES[pq]:
            if pq == 'length':
                if e == 2:
                    return 'area'
                elif e == 3:
                    return 'volume'
            return pq
    return None


def difference_of_orders_of_magnitude(unit1, unit2):
    """
    Return the required power of 10 to multiply unit1 by, to get unit2.

    :param unit1: the first unit
    :type unit1: str or Unit
    :param unit2: the second unit (to get from unit1)
    :type unit2: str or Unit
    :rtype: decimal.Decimal
    """
    if isinstance(unit1, str):
        unit1 = Unit(unit1)
    if isinstance(unit2, str):
        unit2 = Unit(unit2)
    phq1 = physical_quantity(unit1)
    phq2 = physical_quantity(unit2)
    if phq1 == phq2:
        dimension = unit1.exponent
        if dimension is None:
            dimension = 1
        magnitude_diff = (PHYSICAL_QUANTITIES[phq2].index(unit2.content)
                          - PHYSICAL_QUANTITIES[phq1].index(unit1.content))\
            * dimension
    elif phq1 == 'volume' and phq2 == 'capacity':
        magnitude_diff = PHYSICAL_QUANTITIES[phq2].index(unit2.content)\
            - VOLUME_CAPACITY_MATCH.index(unit1.content)
    elif phq1 == 'capacity' and phq2 == 'volume':
        magnitude_diff = VOLUME_CAPACITY_MATCH.index(unit2.content)\
            - PHYSICAL_QUANTITIES[phq1].index(unit1.content)
    else:
        raise TypeError('Cannot give the difference of orders of magnitude '
                        'between two units that do not belong to the same '
                        'physical quantity ({} and {}).'
                        .format(unit1, unit2))
    return 10 ** (Decimal(str(magnitude_diff)))


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

    def imprint(self, start_expr=True, variant='latex', standalone=True):
        if standalone and variant == 'latex':
            required.package['siunitx'] = True
            if self.content in ['€', r'\officialeuro']:
                required.package['eurosym'] = True
            return r'\si{' + super().imprint(start_expr=start_expr) + '}'
        else:
            return super().imprint(start_expr=start_expr, variant=variant)
