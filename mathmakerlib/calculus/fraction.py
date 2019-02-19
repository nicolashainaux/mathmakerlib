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

"""Fractions."""

from math import gcd

from mathmakerlib.calculus.number import Sign, Number
from mathmakerlib.calculus.tools import is_number, is_integer
from mathmakerlib.calculus.tools import prime_factors
from mathmakerlib.core.signed import Signed
from mathmakerlib.core.printable import Printable
from mathmakerlib.core.evaluable import Evaluable
from mathmakerlib.exceptions import StopFractionReduction


class Fraction(Signed, Printable, Evaluable):
    """Fractions."""

    # To keep Fraction immutable, use __new__ not __init__
    def __new__(cls, sign=None, numerator=None, denominator=None,
                from_decimal=None):
        """
        Fraction(5, 8) is equivalent to Fraction('+', 5, 8).
        """
        if from_decimal is not None:
            f = Number(10) ** max(1, from_decimal.fracdigits_nb())
            sign = Sign(from_decimal)
            numerator = (f * from_decimal).standardized()
            denominator = f.standardized()
        elif sign in ['+', '-']:
            if not (is_number(numerator) and is_number(denominator)):
                raise TypeError('Numerator and denominator must be numbers. '
                                'Got {} and {} instead.'
                                .format(type(numerator), type(denominator)))
            if not(is_integer(numerator) and is_integer(denominator)):
                raise TypeError('Numerator and denominator must be integers. '
                                'Got {} and {} instead.'
                                .format(numerator, denominator))
        else:
            if not (is_number(sign) and is_number(numerator)):
                raise TypeError('Numerator and denominator must be numbers. '
                                'Got {} and {} instead.'
                                .format(type(sign), type(numerator)))
            elif not (is_integer(sign) and is_integer(numerator)):
                raise TypeError('Numerator and denominator must be integers. '
                                'Got {} and {} instead.'
                                .format(sign, numerator))
            denominator = numerator
            numerator = sign
            sign = '+'
        # some initialization
        self = object.__new__(cls)
        self._sign = Sign(sign)
        self._numerator = Number(numerator)
        self._denominator = Number(denominator)
        return self

    def __hash__(self):
        return hash(str(self.sign) + str(self.numerator)
                    + str(self.denominator))

    def __eq__(self, other):
        if not isinstance(other, Fraction):
            return False
        return (self.sign == other.sign and self.numerator == other.numerator
                and self.denominator == other.denominator)

    def __ne__(self, other):
        if not isinstance(other, Fraction):
            return True
        return (self.sign != other.sign or self.numerator != other.numerator
                or self.denominator != other.denominator)

    def __lt__(self, other):
        return self.evaluate().__lt__(other)

    def __gt__(self, other):
        return self.evaluate().__gt__(other)

    def __le__(self, other):
        return self.evaluate().__le__(other)

    def __ge__(self, other):
        return self.evaluate().__ge__(other)

    def __repr__(self):
        if self.sign == '+':
            return 'Fraction({}, {})'.format(self.numerator, self.denominator)
        return 'Fraction(\'{}\', {}, {})'.format(self.sign, self.numerator,
                                                 self.denominator)

    @property
    def sign(self):
        return self._sign

    @property
    def numerator(self):
        """Numerator of the Fraction."""
        return self._numerator

    @property
    def denominator(self):
        """Denominator of the Fraction."""
        return self._denominator

    def imprint(self, start_expr=True, variant='latex'):
        s = self.sign
        if s == '+' and start_expr:
            s = ''
        if variant == 'latex':
            return r'{}\dfrac{}{}' \
                .format(s, '{' + str(self.numerator) + '}',
                        '{' + str(self.denominator) + '}')
        elif variant == 'user_input':
            return '{}{}/{}'.format(s, self.numerator, self.denominator)

    def evaluate(self, **kwargs):
        return self.sign.evaluate() \
            * self.numerator.evaluate() / self.denominator.evaluate()

    def is_reducible(self):
        """True if the Fraction is reducible."""
        return gcd(int(self.numerator), int(self.denominator)) > 1

    def reduced(self):
        """Completely reduced Fraction (may return an integer number)."""
        g = gcd(int(self.numerator), int(self.denominator))
        return Fraction(self.sign, self.numerator / g, self.denominator / g)

    def reduced_by(self, n):
        """Return Fraction reduced by n (possibly return a Number)."""
        if not is_number(n):
            raise TypeError('A Fraction can be reduced only by an integer, '
                            'got {} instead.'.format(type(n)))
        if not is_integer(n):
            raise TypeError('A Fraction can be reduced only by an integer, '
                            'got {} instead.'.format(n))
        if not is_integer(self.numerator / n):
            raise ValueError('Cannot divide {} by {} and get an integer.'
                             .format(self.numerator, n))
        if not is_integer(self.denominator / n):
            raise ValueError('Cannot divide {} by {} and get an integer.'
                             .format(self.denominator, n))
        n = abs(n)
        if self.denominator / n == 1:
            return self.sign * self.numerator / n
        if self.denominator / n == -1:
            return Sign('-') * self.sign * self.numerator / n
        return Fraction(self.sign, self.numerator / n, self.denominator / n)

    def reduce(self):
        """
        Return the minimally reduced next Fraction (or Number).

        An exception will be raised if the Fraction is not reducible.
        """
        if not self.is_reducible():
            raise StopFractionReduction(self)
        # lowest prime common divisor
        lpcd = prime_factors(gcd(int(self.numerator),
                                 int(self.denominator)))[0]
        if self.denominator / lpcd == 1:
            return self.sign * self.numerator / lpcd
        return Fraction(self.sign,
                        self.numerator / lpcd, self.denominator / lpcd)
