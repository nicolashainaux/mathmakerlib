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


def surrounding_keys(keyval, d):
    """
    Return the keys just lower and upper the provided reference value.
    The provided dictionary d is supposed to contain comparable keys only and
    these keys are supposed to be in ascending order.
    keyval is supposed to NOT belong to dictionary d, and to be higher than
    its lowest value, and lower than its highest value
    """
    dkeys = list(d.keys())
    if not len(dkeys) >= 2:
        raise ValueError(f'Expected at least 2 keys, only found {len(dkeys)}')
    if not all(dkeys[i] < dkeys[i + 1] for i in range(len(dkeys) - 1)):
        raise ValueError(f'Expected the keys to be in ascending order, but '
                         f'got these keys: {dkeys}')
    if keyval <= dkeys[0] or keyval >= dkeys[-1] or keyval in d.keys():
        raise ValueError(f'Value expected to be '
                         f'{dkeys[0]} < value < {dkeys[-1]}; '
                         f'and not to be in {list(d.keys())}, '
                         f'but got: {keyval}')

    ref_keys = list(d.keys())
    for k in ref_keys:
        if k < keyval < ref_keys[ref_keys.index(k) + 1]:
            return (k, ref_keys[ref_keys.index(k) + 1])
