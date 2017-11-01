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

import copy
import locale
import random
import warnings
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP

from mathmakerlib.core.signed import Signed
from mathmakerlib.core.printable import Printable
from mathmakerlib.core.evaluable import Evaluable
from mathmakerlib.calculus.unit import Unit


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


class Sign(Printable, Evaluable):

    def __init__(self, o):
        self._sign = '+'
        self.sign = o

    def __repr__(self):
        return 'Sign({})'.format(self.sign)

    def __eq__(self, other):
        if isinstance(other, Sign):
            return self.sign == other.sign
        elif other in ['+', '-']:
            return self.sign == other
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, Sign):
            return self.sign != other.sign
        elif other in ['+', '-']:
            return self.sign != other
        else:
            return True

    def imprint(self, start_expr=True, variant='latex'):
        return self.sign

    @property
    def sign(self):
        return self._sign

    @sign.setter
    def sign(self, o):
        if o is '+' or o is '-':
            self._sign = o
        elif isinstance(o, Sign):
            self._sign = o._sign
        elif isinstance(o, Number):
            if o >= 0:
                self._sign = '+'
            else:
                self._sign = '-'
        else:
            raise ValueError('o must be \'+\', \'-\' or a Number.')

    def __mul__(self, o):
        if isinstance(o, Sign):
            if self.sign == o.sign:
                return Sign('+')
            else:
                return Sign('-')
        elif isinstance(o, Number):
            if self.sign == '+':
                return o
            else:
                return -o
        else:
            raise TypeError('Cannot multiply a Sign by a {}.'
                            .format(str(type(o))))

    def __rmul__(self, o):
        return self.__mul__(o)

    def evaluate(self, **kwargs):
        if self.sign == '+':
            return Number(1)
        else:
            return Number(-1)


class Number(Decimal, Signed, Printable, Evaluable):
    """Extend Decimal with a bunch of useful methods."""

    # To keep immutability of Decimal, use __new__ not __init__
    def __new__(cls, value='0', context=None, unit=None):
        if isinstance(value, Sign):
            value = value.evaluate()
        if isinstance(value, Number) and unit is None:
            unit = copy.deepcopy(value.unit)
        self = super().__new__(cls, value=value, context=context)
        self._unit = None
        self.unit = unit
        return self

    def __eq__(self, other):
        if self.unit is None:
            return Decimal(self) == other
        else:
            if not isinstance(other, Number):
                return False
            else:
                return (Decimal(self) == Decimal(other)
                        and self.unit == other.unit)

    def __ne__(self, other):
        if self.unit is None:
            return Decimal(self) != other
        else:
            if not isinstance(other, Number):
                return True
            else:
                return not (Decimal(self) == Decimal(other)
                            and self.unit == other.unit)

    def __add__(self, other, context=None):
        if isinstance(other, Sign):
            raise TypeError('Cannot add a Sign and a Number')
        if not isinstance(other, Number):
            other = Number(other)
        if self.unit == other.unit:
            return Number(Decimal(self).__add__(other), unit=self.unit)
        else:
            if hasattr(other, 'unit') and other.unit is not None:
                other_unit = other.unit.printed
            else:
                other_unit = str(None)
            raise ValueError('Cannot add two Numbers having different '
                             'Units ({} and {}).'
                             .format(self.unit.printed,
                                     other_unit))

    def __radd__(self, other, context=None):
        return self.__add__(other, context=context)

    def __sub__(self, other, context=None):
        if isinstance(other, Sign):
            raise TypeError('Cannot subtract a Sign and a Number')
        if not isinstance(other, Number):
            other = Number(other)
        if self.unit == other.unit:
            return Number(Decimal(self).__sub__(other), unit=self.unit)
        else:
            if hasattr(other, 'unit') and other.unit is not None:
                other_unit = other.unit.printed
            else:
                other_unit = str(None)
            raise ValueError('Cannot subtract two Numbers having different '
                             'Units ({} and {}).'
                             .format(self.unit.printed,
                                     other_unit))

    def __rsub__(self, other, context=None):
        return -self.__sub__(other, context=context)

    def __mul__(self, other, context=None):
        if isinstance(other, Sign):
            other = other.evaluate()
        other = Number(other)
        u = None
        if self.unit is None:
            u = copy.deepcopy(other.unit)
        elif other.unit is None:
            u = copy.deepcopy(self.unit)
        elif self.unit.content == other.unit.content:
            if self.unit.exponent is None:
                se = Number(1)
            else:
                se = Number(self.unit.exponent)
            if other.unit.exponent is None:
                oe = Number(1)
            else:
                oe = Number(other.unit.exponent)
            u = Unit(self.unit.content, exponent=se + oe)
        else:
            if self.unit.exponent is None or self.unit.exponent == Number(1):
                u = Unit(self.unit.content + '.' + other.unit.content,
                         exponent=other.unit.exponent)
            elif (other.unit.exponent is None
                  or other.unit.exponent == Number(1)):
                u = Unit(other.unit.content + '.' + self.unit.content,
                         exponent=self.unit.exponent)
            else:
                raise NotImplementedError('Cannot yet handle a '
                                          'multiplication of {} by {}.'
                                          .format(repr(self), repr(other)))
        return Number(Decimal(self).__mul__(other),
                      unit=u)

    def __rmul__(self, other, context=None):
        return self.__mul__(other, context=context)

    def __truediv__(self, other, context=None):
        if isinstance(other, Sign):
            other = other.evaluate()
        other = Number(other)
        u = None
        if self.unit is None and other.unit is None:
            u = None
        elif self.unit is None:
            u = copy.deepcopy(other.unit)
            if u.exponent is None:
                u.exponent = -Number(1)
            else:
                u.exponent = -u.exponent
        elif other.unit is None:
            u = copy.deepcopy(self.unit)
        elif self.unit.content == other.unit.content:
            if self.unit.exponent is None:
                se = Number(1)
            else:
                se = Number(self.unit.exponent)
            if other.unit.exponent is None:
                oe = Number(1)
            else:
                oe = Number(other.unit.exponent)
            if se == oe:
                u = None
            elif se - oe == Number(1):
                u = Unit(self.unit.content, exponent=None)
            else:
                u = Unit(self.unit.content, exponent=se - oe)
        else:
            if ((self.unit.exponent is None or self.unit.exponent == Number(1))
                and (other.unit.exponent is None
                     or other.unit.exponent == Number(1))):
                u = Unit(self.unit.content + '/' + other.unit.content)
            else:
                raise NotImplementedError('Cannot yet handle a '
                                          'division of {} by {}.'
                                          .format(repr(self), repr(other)))
        return Number(Decimal(self).__truediv__(other), unit=u)

    def __rtruediv__(self, other, context=None):
        return Number.__truediv__(Number(other), self, context=context)

    def __floordiv__(self, other, context=None):
        if isinstance(other, Sign):
            other = other.evaluate()
        return Number(Decimal(self).__floordiv__(other))

    def __rfloordiv__(self, other, context=None):
        return Number.__floordiv__(Number(other), self, context=context)

    def __mod__(self, other, context=None):
        return Number(Decimal(self).__mod__(other))

    def __rmod__(self, other, context=None):
        return Number(Decimal(self).__rmod__(other))

    def __divmod__(self, other, context=None):
        r = Decimal(self).__divmod__(other)
        return (Number(r[0]), Number(r[1]))

    def __rdivmod__(self, other, context=None):
        r = Decimal(self).__rdivmod__(other)
        return (Number(r[0]), Number(r[1]))

    def __pow__(self, other, context=None):
        return Number(Decimal(self).__pow__(other))

    def __rpow__(self, other, context=None):
        return Number(Decimal(self).__rpow__(other))

    def __neg__(self):
        return Number(-Decimal(self), unit=copy.deepcopy(self.unit))

    def __pos__(self):
        return Number(+Decimal(self), unit=copy.deepcopy(self.unit))

    def __abs__(self):
        return Number(abs(Decimal(self)), unit=copy.deepcopy(self.unit))

    def __repr__(self):
        basic_repr = repr(Decimal(str(self))).replace('Decimal', 'Number')
        if self.unit is None:
            return basic_repr
        else:
            return basic_repr.replace("')", " {}')"
                                            .format(self.unit.uiprinted))

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, u):
        if u is None:
            self._unit = None
        else:
            self._unit = Unit(u)

    @property
    def sign(self):
        if self < 0:
            return Sign('-')
        else:
            return Sign('+')

    def imprint(self, start_expr=True, variant='latex'):
        extra_sign = ''
        if not start_expr and self >= 0:
            extra_sign = '+'
        if variant == 'latex':
            self_str = locale.str(self)
        elif variant == 'user_input':
            self_str = str(self)
        else:
            raise ValueError('variant must belong to [\'latex\', '
                             '\'user_input\']; got \'{}\' instead.'
                             .format(variant))
        if self.unit is None:
            return extra_sign + self_str
        else:
            if variant == 'latex':
                return extra_sign + r'\SI{' + str(abs(self)) + '}' \
                    '{' + self.unit.printed + '}'
            else:  # 'user_input'
                return extra_sign + self_str + ' ' + self.unit.printed

    def evaluate(self, **kwargs):
        return self

    def standardized(self):
        """Turn 8.0 to 8 and 1E+1 to 10"""
        return Number(self.quantize(Decimal(1))) \
            if self == self.to_integral() \
            else Number(self.normalize())

    def nonzero_digits_nb(self):
        """Return the number of nonzero digits."""
        n = str(abs(self.standardized()))
        return len(n) - n.count('0') - n.count('.')

    def isolated_zeros(self):
        """Return the number of zeros inside other digits."""
        if self == 0:
            return 0
        elif self % 10 == 0:
            return Number(self // 10).isolated_zeros()
        else:
            return self.standardized().as_tuple().digits.count(0)

    def rounded(self, precision, rounding=ROUND_HALF_UP):
        """
        Round the number. Return a standardized result.

        :param precision: a Decimal (same as decimal.Decimal().quantize()).
                          For instance, Decimal('1'), Decimal('1.0') etc.
        """
        return Number(self.quantize(precision,
                                    rounding=rounding)).standardized()

    def fracdigits_nb(self):
        """Return the number of fractional digits."""
        n = Number(abs(self)).standardized()
        temp = len(str((n - n.rounded(Decimal(1), rounding=ROUND_DOWN)))) - 2
        return temp if temp >= 0 else 0

    def is_power_of_10(self):
        """Check if n is a power of ten."""
        n = Number(abs(self))
        if Decimal(10) <= n:
            return Number(n / Number(10)).is_power_of_10()
        if Decimal(1) < n < Decimal(10):
            return False
        elif n == Decimal(1):
            return True
        elif Decimal('0.1') < n < Decimal(1):
            return False
        elif 0 < n <= Decimal('0.1'):
            return Number(n * Number(10)).is_power_of_10()
        elif n == 0:
            return False

    def atomized(self, keep_zeros=False):
        """Split abs(self) in as many Numbers as digits."""
        _, digits, e = self.standardized().as_tuple()
        digits = list(digits)
        result = []
        for i, d in enumerate(digits):
            if d != 0 or keep_zeros:
                result += [Number(d) * Number(10) ** (e + len(digits) - 1 - i)]
        if not len(result):
            return [Number(0)]
        return [Number(n) for n in result]

    def overlap_level(self):
        """
        Calculate the maximum overlap possible.

        For instance, 0.724 has an overlap level of 1 (can be split as
        0.71 + 0.14) but 0.714 has an overlap level of only 0 (can be split as
        0.7 + 0.014 or 0.71 + 0.004, but not as two decimals having a nonzero
        digits at tenths' position.)
        """
        base_level = self.standardized().nonzero_digits_nb() - 2
        digits = list(self.as_tuple().digits)
        level = base_level - digits[1:-1].count(1)
        return level

    def cut(self, overlap=0, return_all=False):
        """
        Cut self as a + b, a and b having only 0, 1... positions in common.

        For instance:
        Number('5.6').cut() == (Number('5'), Number('0.6'))
        Number('5.36').cut(return_all=True) == \
            [(Number('5'), Number('0.36')),
             (Number('5.3'), Number('0.06'))]
        Number('5.36').cut(overlap=1, return_all=True) == \
            [(Number('5.1'), Number('0.26')),
             (Number('5.2'), Number('0.16'))]

        :param overlap: tells how many decimal places in common the terms a
                        and b should have when splitting as a sum.
                        Values of overlap >= 2 are not handled yet
        :type overlap: int (only 0 or 1 are handled yet)
        :param return_all: if True, then all possibilities are returned, as a
                           list.
        :type return_all: bool
        :rtype: tuple (or a list of tuples)
        """
        if not isinstance(overlap, int):
            raise TypeError('When overlap is used, it must be an int. Got '
                            'a {} instead.'.format(type(overlap)))
        if overlap < 0:
            raise ValueError('overlap must be a positive int. Got a '
                             'negative int instead.')
        if self.overlap_level() < overlap:
            raise ValueError('Given overlap is too high.')
        if overlap not in [0, 1]:
            raise ValueError('Only 0 <= overlap <= 1 is implemented yet.')
        results = []
        digits = self.atomized()
        if overlap == 0:
            for n in range(len(digits) - 1):
                results += [(sum(digits[0:n + 1]), sum(digits[n + 1:]))]
        elif overlap == 1:
            for i in range(self.overlap_level()):
                results += [(sum(digits[0:i + 1] + [d[0]]),
                             sum(digits[i + 2:]) + d[1])
                            for d
                            in digits[i + 1].split(return_all=True)]
        if return_all:
            return results
        else:
            return random.choice(results)

    def split(self, operation='sum', dig=0, return_all=False):
        """
        Split self as a sum or difference, e.g. self = a + b or self = a - b

        By default, a and b have as many fractional digits as n does.
        The 'dig' keyword tells how many extra digits must have a and b
        (compared to self). For instance, if n=Decimal('4.5'), operation='sum',
        dig=1, then self will be split into 2-fractional-digits numbers,
        like 2.14 + 2.36.

        :param operation: must be 'sum', 'difference', '+' or '-'
        :type operation: str
        :param dig: extra depth level to use
        :type dig: int
        :rtype: tuple (of numbers)
        """
        if operation not in ['sum', 'difference', '+', '-']:
            raise ValueError('Argument "operation" should be either \'sum\' '
                             'or \'difference\'.')
        n_depth = self.fracdigits_nb()
        depth = dig + self.fracdigits_nb()
        n = self
        if operation in ['sum', '+']:
            if self.is_power_of_10() and abs(self) <= 1 and dig == 0:
                # This case is impossible: write 1 as a sum of two natural
                # numbers bigger than 1, or 0.1 as a sum of two positive
                # decimals having 1 digit either, etc. so we arbitrarily
                # replace self by a random number between 2 and 9
                warnings.warn('mathmakerlib is asked something impossible '
                              '(split {} as a sum of two numbers having as '
                              'many digits)'.format(self))
                n = random.choice([i + 2 for i in range(7)])
                n = n * (10 ** (Decimal(- n_depth)))
            amplitude = n
        elif operation in ['difference', '-']:
            amplitude = max(10 ** (n_depth), n)
        start, end = 0, int((amplitude) * 10 ** depth - 1)
        if start > end:
            start, end = end + 1, -1
        # default: all numbers, including integers
        seq = [(Decimal(i) + 1) / Decimal(10) ** Decimal(depth)
               for i in range(start, end)]
        # then if decimals are wanted, we remove the results that do not match
        # the wanted "depth" (if depth == 2, we remove 0.4 for instance)
        if depth >= 1:
            seq = [i for i in seq
                   if not is_integer(i * (10 ** (depth - 1)))]
        if return_all:
            if operation in ['sum', '+']:
                return [(Number(a), Number(n - a)) for a in seq]
            elif operation in ['difference', '-']:
                return [(Number(n + b), Number(b)) for b in seq]
        else:
            if operation in ['sum', '+']:
                a = random.choice(seq)
                b = n - a
            elif operation in ['difference', '-']:
                b = random.choice(seq)
                a = n + b
            return (Number(a), Number(b))


def move_fracdigits_to(n, from_nb=None):
    """
    Turn n into decimal instead of all decimals found in the from_nb list.

    Each decimal found in the numbers' list will be recursively replaced by
    10 times itself (until it is no decimal anymore) while in the same time
    n will be divided by 10.

    This is useful for the case division by a decimal is unwanted.

    :param n: the number who will be divided by 10 instead of the others
    :type n: any number (int, Decimal, float though they're not advised)
    :param from_nb: an iterable containing the numbers that must be integers
    :type from_nb: a list (of numbers)
    :rtype: a list (of numbers)
    """
    if type(from_nb) is not list:
        raise TypeError('A list of numbers must be given as argument '
                        '\'numbers\'.')
    if not is_number(n):
        raise TypeError('The first argument must be a number.')
    n = Decimal(str(n))
    # If any element of from_nb is not a number, is_integer() will raise
    # an exception.
    if all([is_integer(i) for i in from_nb]):
        return [n, ] + [i for i in from_nb]
    numbers_copy = copy.deepcopy(from_nb)
    for i, j in enumerate(from_nb):
        if not is_integer(j):
            numbers_copy[i] = j * 10
            return move_fracdigits_to(n / 10, from_nb=numbers_copy)


def remove_fracdigits_from(number, to=None):
    """
    Turn a number of the to list into a decimal, instead of number.

    In some cases this is not possible (for instance when all numbers of the
    to list are multiples of 10), then a ValueError is raised.

    :param number: the number that must be turned into integer
    :type number: decimal.Decimal
    :param to: the list of numbers where to find an integer that must be
               turned into a decimal
    :type to: list
    :rtype: a list (of numbers)
    """
    if not isinstance(number, Decimal):
        raise TypeError('The first argument must be a Decimal number.')
    if is_integer(number):
        raise TypeError('The first argument must be a decimal number.')
    if type(to) is not list:
        raise TypeError('Argument to: must be a list.')
    n = Number(number).fracdigits_nb()
    try:
        i = to.index(next(x for x in to
                          if not is_integer(x / 10 ** n)))
    except StopIteration:
        raise ValueError('None of the numbers of to can be turned into '
                         'decimal.')
    to[i] = Number(to[i]) / Number(10) ** n
    return [Number(number * 10 ** n).standardized(), ] + [x for x in to]


def fix_fracdigits(n1, *n2):
    """Ensure digits from n1 are removed. Change n2 if necessary."""
    n2 = list(n2)
    try:
        n1, *n2 = remove_fracdigits_from(n1, to=n2)
    except ValueError:
        j = random.choice([j for j in range(len(n2))])
        n2[j] += random.choice([i for i in range(-4, 5) if i != 0])
        n1, *n2 = remove_fracdigits_from(n1, to=n2)
    return (n1, *n2)
