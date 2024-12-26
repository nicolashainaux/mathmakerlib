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

from decimal import Decimal

from sympy.ntheory import primefactors


def is_number(n):
    """Check if n is a number."""
    return isinstance(n, (float, int, Decimal))


def is_integer(n):
    """Check if number n is an integer."""
    if isinstance(n, int):
        return True
    elif isinstance(n, float):
        return n.is_integer()
    elif isinstance(n, Decimal):
        return n % 1 == 0
    else:
        raise TypeError('Expected a number, either float, int or Decimal,'
                        'got {} instead.'.format(str(type(n))))


def is_natural(n):
    """Check if number n is a natural number."""
    return is_integer(n) and n >= 0


def prime_factors(n):
    """
    Return all the prime factors of a positive integer

    Taken from https://stackoverflow.com/a/412942/3926735.
    """
    try:
        n = int(n)
    except ValueError:
        raise TypeError('The argument must be an integer.')
    factors = []
    d = 2
    while n > 1:
        while n % d == 0:
            factors.append(d)
            n //= d
        d = d + 1
        if d * d > n:
            if n > 1:
                factors.append(n)
            break
    return factors


# TODO: this is a bit redundant with the previous method
def prime_decomposition(nn):
    """
    Return the prime decomposition of self (natural numbers only).
    """
    primes_list = primefactors(nn)
    decomposition = list()
    for p in primes_list:
        i = 0
        while not (nn % p):
            i += 1
            nn = nn / p
        decomposition.append((p, i))
    return decomposition


def weighted_average(value1, value2, mass1, mass2, rounding_rank=3):
    return round((value1 * mass1 + value2 * mass2) / (mass1 + mass2),
                 rounding_rank)
