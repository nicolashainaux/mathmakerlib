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


def parse_layout_descriptor(ld, sep='×x', special_row_chars='',
                            min_row=0, min_col=0):
    """
    Parse a "layout" string, e.g. '3×4'. Return number of rows, number of cols.

    :param d: the "layout" string
    :type d: str
    :param sep: a list of accepted characters as separators. Defaults to '×x'
    :type sep: any iterable
    :param special_row_chars: a list of special characters allowed instead of
                              natural numbers. Defaults to ''
    :type special_row_chars: any iterable
    :param min_row: a minimal value that the number of rows must respect. It is
                    not checked if nrow is a special char
    :type min_row: positive int
    :param min_col: a minimal value that the number of columns must respect
    :type min_col: positive int
    :rtype: tuple
    """
    ld = str(ld)
    seplist = [str(c) for c in sep]
    special_row_chars = [str(c) for c in special_row_chars]

    for s in seplist:
        if s in ld:
            sep = str(s)
            break
    else:  # no break
        raise ValueError(
            f'The string "{ld}" does not contain any of the expected '
            f'separators: {seplist}')

    min_row, min_col = int(min_row), int(min_col)

    nrow_ncol = ld.split(sep=sep)

    nrow_ncol = [value for value in nrow_ncol if value]
    if not len(nrow_ncol) == 2:
        raise ValueError(f'The layout descriptor is expected to '
                         f'contain two values separated by "{sep}"')

    nrow, ncol = nrow_ncol
    if nrow not in special_row_chars:
        nrow = int(nrow)
        if nrow < min_row:
            raise ValueError('nrow must be greater than ' + str(min_row))
    if ncol not in special_row_chars:
        ncol = int(ncol)
        if ncol < min_col:
            raise ValueError('ncol must be greater than ' + str(min_col))
    return nrow, ncol
