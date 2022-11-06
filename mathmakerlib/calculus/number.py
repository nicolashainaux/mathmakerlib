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

import copy
import math
import locale
import random
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP

from mathmakerlib import required
from mathmakerlib.calculus.unit import physical_quantity
from mathmakerlib.calculus.tools import is_number, is_integer
from mathmakerlib.core.signed import Signed
from mathmakerlib.core.printable import Printable
from mathmakerlib.core.evaluable import Evaluable
from mathmakerlib.calculus.unit import Unit, difference_of_orders_of_magnitude


class Sign(Printable, Evaluable):

    def __init__(self, o):
        self._sign = '+'
        self.sign = o

    def __repr__(self):
        return 'Sign({})'.format(self.sign)

    def __str__(self):
        return str(self.sign)

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
        if o in ['+', '-']:
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
    def __new__(cls, value='0', context=None, unit='undefined'):
        if isinstance(value, Sign):
            value = value.evaluate()
        if isinstance(value, float):
            value = str(value)
        if isinstance(value, Number) and unit == 'undefined':
            unit = copy.deepcopy(value.unit)
        if unit == 'undefined':
            unit = None
        self = super().__new__(cls, value=value, context=context)
        if unit is None:
            self._unit = None
        else:
            self._unit = Unit(unit)
        return self

    def __hash__(self):
        return hash(Decimal(self))

    def __copy__(self):  # Similar to Decimal.__copy__()
        if type(self) is Number:
            return self     # I'm immutable; therefore I am my own clone
        return self.__class__(self)

    def __deepcopy__(self, memo):  # Similar to Decimal.__deepcopy__()...
        if type(self) is Number:
            # ...but my components are *not* also immutable
            return Number(value=self, unit=self.unit)
        return self.__class__(self, unit=self.unit)

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
                other_unit = str(other.unit)
            else:
                other_unit = str(None)
            raise ValueError('Cannot add two Numbers having different '
                             'Units ({} and {}).'
                             .format(str(self.unit),
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
                other_unit = str(other.unit)
            else:
                other_unit = str(None)
            raise ValueError('Cannot subtract two Numbers having different '
                             'Units ({} and {}).'
                             .format(str(self.unit),
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

    def __str__(self):
        basic_str = Decimal.__str__(self)
        if self.unit is None:
            return basic_str
        else:
            return basic_str + ' ' + str(self.unit)

    def __repr__(self):
        basic_repr = repr(Decimal(Decimal.__str__(self))).replace('Decimal',
                                                                  'Number')
        if self.unit is None:
            return basic_repr
        else:
            return basic_repr.replace("')", " {}')"
                                            .format(self.unit.uiprinted))

    def sqrt(self):
        return Number(Decimal(self).sqrt())

    def quantize(self, exp, rounding=None, context=None):
        return Number(Decimal(self).quantize(exp,
                                             rounding=rounding,
                                             context=context),
                      context=context,
                      unit=self.unit)

    @property
    def unit(self):
        return self._unit

    @property
    def sign(self):
        if self < 0:
            return Sign('-')
        else:
            return Sign('+')

    def imprint(self, start_expr=True, variant='latex', dot=False):
        extra_sign = ''
        if not start_expr and self >= 0:
            extra_sign = '+'

        if variant in ['latex', 'siunitx']:
            self_str = locale.format_string(
                '%.{}f'.format(
                    self.fracdigits_nb(ignore_trailing_zeros=False)),
                Decimal(self))
        elif variant == 'user_input':
            self_str = Decimal.__str__(self)
        else:
            raise ValueError('variant must belong to [\'latex\', \'siunitx\', '
                             '\'user_input\']; got \'{}\' instead.'
                             .format(variant))
        if dot:
            self_str = self_str\
                .replace(locale.localeconv()['decimal_point'], '.')
        if self.unit is None:
            if variant == 'siunitx':
                required.package['siunitx'] = True
                return r'\num{{{}}}'.format(extra_sign + self_str)
            else:
                return extra_sign + self_str
        else:
            if variant == 'latex':
                required.package['siunitx'] = True
                if self.unit.content in ['€', r'\officialeuro']:
                    required.package['eurosym'] = True
                if physical_quantity(self.unit) == 'angle':
                    return extra_sign + r'\ang{' + self_str + '}'
                else:
                    return extra_sign + r'\SI{' + self_str \
                        + '}{' + self.unit.imprint(standalone=False) + '}'
            else:  # 'user_input'
                return extra_sign + self_str + ' ' + self.unit.uiprinted

    def evaluate(self, **kwargs):
        return self

    def standardized(self):
        """Turn 8.0 to 8 and 1E+1 to 10"""
        return Number(self.quantize(Decimal(1)), unit=self.unit) \
            if self == self.to_integral() \
            else Number(self.normalize(), unit=self.unit)

    def converted_to(self, unit):
        if isinstance(unit, str):
            unit = Unit(unit)
        try:
            factor = difference_of_orders_of_magnitude(self.unit, unit)
        except TypeError as excinfo:
            if str(excinfo).startswith('Cannot give the difference of orders '
                                       'of magnitude between two units that '
                                       'do not belong to the same '
                                       'physical quantity'):
                raise TypeError('Cannot convert {} into {}.'
                                .format(self.uiprinted, unit.uiprinted))
        return Number(self * factor, unit=unit)

    def lowest_nonzero_digit_index(self):
        """
        Index of the lowest digit different from zero.

        Indices are 0 for the unit position, 1 for tenths, 2 for hundredths,
        etc. and -1 for tens, -2 for hundreds etc.

        If self is 0, then return None.
        """
        if self == 0:
            return None
        fdn = self.fracdigits_nb()
        if fdn > 0:
            return fdn
        n_tenth = self / 10
        if n_tenth.fracdigits_nb() == 0:
            return -1 + n_tenth.lowest_nonzero_digit_index()
        else:
            return 0

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
        if precision >= 10:
            rounded_val = round(self, -int(math.log10(precision)))
        else:
            rounded_val = self.quantize(precision, rounding=rounding)
        return Number(rounded_val, unit=self.unit).standardized()

    def fracdigits_nb(self, ignore_trailing_zeros=True):
        """Return the number of fractional digits."""
        n = Number(Decimal(self), unit=None)
        if ignore_trailing_zeros:
            n = Number(abs(n)).standardized()
        else:
            n = abs(n)
        temp = len(str((n - n.rounded(Decimal(1), rounding=ROUND_DOWN)))) - 2
        return temp if temp >= 0 else 0

    def digits_sum(self):
        """Return the sum of all digits."""
        _, digits, e = self.standardized().as_tuple()
        return sum(list(digits))

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

    def is_pure_half(self):
        """True if fractional part is .5"""
        return self % 1 == Number('0.5')

    def is_pure_quarter(self):
        """True if fractional part is .25 or .75"""
        return self % 1 in (Number('0.25'), Number('0.75'))

    @property
    def digits(self):
        """Break down the number into a dictionary."""
        _, digits, e = self.standardized().as_tuple()
        return {Number(10) ** (e + len(digits) - 1 - i): d
                for i, d in enumerate(digits)}

    def highest_digitplace(self):
        """Return a power of ten matching the highest digitplace."""
        _, digits, e = self.standardized().as_tuple()
        return Number(10) ** (e + len(digits) - 1)

    def estimation(self):
        """Round to the highest digitplace possible."""
        return self.rounded(self.highest_digitplace())

    def digit(self, digitplace):
        """
        Return the digit matching digitplace.

        :param digitplace: a power of ten matching the digit to get
        :type digitplace: Decimal
        """
        if not Number(digitplace).is_power_of_10():
            raise ValueError('Expect a power of ten, found {} instead.'
                             .format(repr(digitplace)))
        if digitplace in self.digits:
            return self.digits[digitplace]
        else:
            return 0

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

    def split(self, operation='sum', dig=0, return_all=False,
              int_as_halves=False, int_as_quarters=False,
              int_as_halves_or_quarters=False, at_unit=False):
        """
        Split self as a sum or difference, e.g. self = a + b or self = a - b

        By default, a and b have as many fractional digits as n does.
        The 'dig' keyword tells how many extra digits must have a and b
        (compared to self). For instance, if n=Decimal('4.5'), operation='sum',
        dig=1, then self will be split into 2-fractional-digits numbers,
        like 2.14 + 2.36.

        For natural numbers, the split depth will match the lowest non-zero
        digit (except for powers of 10). For instance, 70 would, by default,
        be split at tens (10, 20, 30, 40, 50 and 60). Take care that splitting
        20 then leads to 10 + 10 only.

        The powers of 10 (natural numbers or not) cannot be split at their own
        rank, so by default, the value of dig will be 1 (a user-provided 0 will
        be ignored).

        :param operation: must be 'sum', 'difference', '+' or '-'
        :type operation: str
        :param dig: extra depth level to use
        :type dig: int
        :param at_unit: whether depth level should be set at unit
        :type at_unit: raise TypeError if self is not an integer
        :param int_as_halves: whether integers should be split as two integers
        ± 0.5. Disabled if self is not integer.
        :type int_as_halves: bool
        :param int_as_quarters: whether integers should be split as two
        integers ± 0.25 Disabled if self is not integer.
        :type int_as_quarters: bool
        :param int_as_halves_or_quarters: whether integers should be split as
        two integers ± 0.5 or ±0.25 (randomly). Disabled if self is not
        integer.
        :type int_as_halves_or_quarters: bool
        :rtype: tuple (of numbers)
        """
        if operation not in ['sum', 'difference', '+', '-']:
            raise ValueError('Argument "operation" should be either \'sum\' '
                             'or \'difference\'.')
        if at_unit and not is_integer(self):
            raise TypeError(
                f'Cannot split at unit the non integer Number {str(self)}')
        if self.is_power_of_10() and dig == 0 and not at_unit:
            dig = 1
        if at_unit:
            n_depth = self.fracdigits_nb()
            depth = dig + self.fracdigits_nb()
        else:
            n_depth = self.lowest_nonzero_digit_index()
            depth = dig + self.lowest_nonzero_digit_index()
        n = self
        if operation in ['sum', '+']:
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
        if not seq:
            raise RuntimeError(
                f'Cannot split {self} (operation=\'{operation}\', dig={dig}, '
                f'at_unit={at_unit}, int_as_halves={int_as_halves}, '
                f'int_as_quarters= {int_as_quarters}, int_as_halves_or_quar'
                f'ters={int_as_halves_or_quarters}, return_all={return_all})')
        delta = 0
        if is_integer(self):
            if int_as_halves_or_quarters:
                h, q = (True, False) if random.choice([True, False]) \
                    else (False, True)
                int_as_halves, int_as_quarters = h, q
            if int_as_halves:
                delta = Number('0.5')
            if int_as_quarters:
                delta = Number('0.25')
        if return_all:
            if operation in ['sum', '+']:
                return [(Number(a) + delta, Number(n - a) - delta)
                        for a in seq]
            elif operation in ['difference', '-']:
                return [(Number(n + b) + delta, Number(b) + delta)
                        for b in seq]
        else:
            if operation in ['sum', '+']:
                a = random.choice(seq)
                b = n - a
                a += delta
                b -= delta
            elif operation in ['difference', '-']:
                b = random.choice(seq)
                a = n + b
                a += delta
                b += delta
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
