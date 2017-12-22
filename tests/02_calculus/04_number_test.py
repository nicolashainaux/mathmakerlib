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

import sys
import locale
import pytest
from copy import copy, deepcopy
from decimal import Decimal, ROUND_HALF_UP

from mathmakerlib import required
from mathmakerlib.core import Signed, Printable, Evaluable
from mathmakerlib.calculus import is_integer, Unit, Number, Sign
from mathmakerlib.calculus import move_fracdigits_to
from mathmakerlib.calculus import remove_fracdigits_from
from mathmakerlib.calculus import fix_fracdigits

LOCALE_US = 'en-US' if sys.platform.startswith('win') else 'en_US.UTF-8'
LOCALE_FR = 'fr-FR' if sys.platform.startswith('win') else 'fr_FR.UTF-8'


def test_Number_inheritance():
    """Check Number is instance of..."""
    assert isinstance(Number(4), Decimal)
    assert isinstance(Number(4), Signed)
    assert isinstance(Number(4), Printable)
    assert isinstance(Number(4), Evaluable)


def test_Number_instanciation():
    """Check Number instanciations."""
    assert Number(Number(4)).unit is None
    assert Number(Number(4, unit='cm')).unit == Unit('cm')
    assert Number(Number(4), unit='cm').unit == Unit('cm')
    assert Number(Number(4, unit='dm'), unit='cm').unit == Unit('cm')
    assert Number(4, unit='cm').unit == Unit('cm')


def test_Number_equality():
    """Check Number __eq__ and __ne__."""
    assert Number(4) == Decimal(4)
    assert Number(4) == 4
    assert not (Number(4, unit='cm') == 4)
    assert Number(4, unit='cm') != 4
    assert Number(4) != Decimal(5)
    assert Number(4, unit='cm') != Decimal(4)
    assert Number(4, unit='cm') != Number(5, unit='cm')
    assert Number(4, unit='cm') != Number(4, unit='dm')


def test_Number_hashability():
    """Check Number is hashable."""
    hash(Number(7))
    hash(Number('8.5'))
    hash(Number('8.5', unit='cm'))


def test_Sign_errors():
    """Check the Sign class exceptions."""
    with pytest.raises(ValueError) as excinfo:
        Sign('-4')
    assert str(excinfo.value) == 'o must be \'+\', \'-\' or a Number.'
    with pytest.raises(TypeError) as excinfo:
        Sign('-') * '+'
    assert str(excinfo.value) == 'Cannot multiply a Sign by a <class \'str\'>.'


def test_Sign():
    """Check the Sign class"""
    assert Sign('+') == '+'
    assert Sign('-') == '-'
    assert Sign('+') == Sign('+')
    assert Sign('+') != Sign('-')
    assert Sign('+') != '-'
    assert Sign('+') in ['+', '-']
    assert not (Sign('+') == 8)
    assert Sign('+') != 8
    p = Sign('+')
    n = Sign('-')
    assert repr(p) == 'Sign(+)'
    assert repr(Sign(n)) == 'Sign(-)'
    assert p.printed == '+'
    assert Sign(Number(-7)).printed == '-'
    assert Sign(Number('9.4')).printed == '+'
    assert repr(p * p) == 'Sign(+)'
    assert repr(n * n) == 'Sign(+)'
    assert repr(n * p) == 'Sign(-)'
    assert repr(p * n) == 'Sign(-)'
    assert p * Number(4) == Number(4)
    assert n * Number(4) == Number(-4)
    assert Number(4) * p == Number(4)
    assert Number(-4) * n == Number(4)
    assert p.evaluate() == Number(1)
    assert n.evaluate() == Number(-1)


def test_copyability():
    """Check copy.copy() and copy.deepcopy() work correctly."""
    assert copy(Number('6')) == 6
    assert copy(Number('6', unit='cm')) == Number(6, unit='cm')
    assert deepcopy(Number('6')) == 6
    assert deepcopy(Number('6', unit='cm')).uiprinted == '6 cm'

    class DerivedNb(Number):
        pass

    assert copy(DerivedNb(Number('6'))) == 6
    assert copy(DerivedNb(Number('6', unit='cm'))) == Number(6, unit='cm')
    assert deepcopy(DerivedNb(Number('6'))) == 6
    assert deepcopy(DerivedNb(Number('6', unit='cm'))) == Number(6, unit='cm')


def test__repr__():
    """Check __repr__ is correct."""
    assert repr(Number('8.6')) == 'Number(\'8.6\')'
    assert repr(Number('8.6', unit='cm')) == 'Number(\'8.6 cm\')'


def test_sqrt():
    """Check sqrt() is correct."""
    assert Number(2).sqrt().rounded(Decimal('0.0001')) == Number('1.4142')


def test_additions_errors():
    """Check additions exceptions."""
    with pytest.raises(TypeError) as excinfo:
        Number(4) + Sign('+')
    assert str(excinfo.value) == 'Cannot add a Sign and a Number'

    with pytest.raises(TypeError) as excinfo:
        Sign('+') + Number(4)
    assert str(excinfo.value) == 'Cannot add a Sign and a Number'

    with pytest.raises(ValueError) as excinfo:
        Number(4, unit='cm') + Number(4)
    assert str(excinfo.value) == 'Cannot add two Numbers having different ' \
        'Units (cm and None).'

    with pytest.raises(ValueError) as excinfo:
        Number(4, unit='cm') + Number(4, unit='dm')
    assert str(excinfo.value) == 'Cannot add two Numbers having different ' \
        'Units (cm and dm).'


def test_additions():
    """Check __add__, __radd__, __iadd__, __abs__, __pos__."""
    assert isinstance(Number(4) + Number(4), Number)
    assert isinstance(4 + Number(4), Number)
    assert isinstance(Number(4) + 4, Number)
    n = Number(4)
    n += Number(1)
    assert isinstance(n, Number)
    n += 1
    assert isinstance(n, Number)
    assert isinstance(abs(n), Number)
    assert isinstance(+n, Number)
    assert Number(7, unit='cm') + Number(8, unit='cm') == Number(15, unit='cm')
    n = Number(-5, unit='cm')
    assert +n == n
    assert -n == Number(5, unit='cm')
    assert abs(n) == Number(5, unit='cm')


def test_subtractions_errors():
    """Check subtractions exceptions."""
    with pytest.raises(TypeError) as excinfo:
        Number(4) - Sign('+')
    assert str(excinfo.value) == 'Cannot subtract a Sign and a Number'

    with pytest.raises(TypeError) as excinfo:
        Sign('+') - Number(4)
    assert str(excinfo.value) == 'Cannot subtract a Sign and a Number'

    with pytest.raises(ValueError) as excinfo:
        Number(4, unit='cm') - Number(4)
    assert str(excinfo.value) == 'Cannot subtract two Numbers having ' \
        'different Units (cm and None).'

    with pytest.raises(ValueError) as excinfo:
        Number(4, unit='cm') - Number(4, unit='dm')
    assert str(excinfo.value) == 'Cannot subtract two Numbers having ' \
        'different Units (cm and dm).'


def test_subtractions():
    """Check __sub__, __rsub__, __isub__, __neg__."""
    assert isinstance(Number(4) - Number(4), Number)
    assert isinstance(4 - Number(4), Number)
    assert isinstance(Number(4) - 4, Number)
    n = Number(4)
    n -= Number(1)
    assert isinstance(n, Number)
    n -= 1
    assert isinstance(n, Number)
    assert isinstance(-n, Number)
    assert Number(9, unit='cm') - Number(3, unit='cm') == Number(6, unit='cm')


def test_multiplications_errors():
    """Check subtractions exceptions."""
    with pytest.raises(TypeError) as excinfo:
        8 * Sign('-')
    assert str(excinfo.value) == 'Cannot multiply a Sign by a <class \'int\'>.'

    with pytest.raises(NotImplementedError) as excinfo:
        Number(6, unit=Unit('cm', exponent=Number(2))) \
            * Number(6, unit=Unit('dm', exponent=Number(3)))
    assert str(excinfo.value) == 'Cannot yet handle a ' \
                                 'multiplication of Number(\'6 cm^2\') ' \
                                 'by Number(\'6 dm^3\').'


def test_multiplications():
    """Check __mul__, __rmul__, __imul__."""
    assert isinstance(Number(4) * Number(4), Number)
    assert isinstance(4 * Number(4), Number)
    assert isinstance(Number(4) * 4, Number)
    n = Number(4)
    n *= Number(4)
    n *= 4
    assert isinstance(n, Number)
    n = Number(6, unit='cm')
    p = Number(7)
    assert n * p == Number(42, unit='cm')
    n = Number(6)
    p = Number(7, unit='cm')
    assert n * p == Number(42, unit='cm')
    n = Number(6, unit='cm')
    p = Number(7, unit='cm')
    assert n * p == Number(42, unit=Unit('cm', exponent=Number(2)))
    n = Number(6, unit='cm')
    p = Number(7, unit=Unit('cm', exponent=Number(2)))
    assert n * p == Number(42, unit=Unit('cm', exponent=Number(3)))
    n = Number(6, unit=Unit('cm', exponent=Number(2)))
    p = Number(7, unit='cm')
    assert n * p == Number(42, unit=Unit('cm', exponent=Number(3)))
    n = Number(6, unit='W')
    p = Number(7, unit='h')
    assert n * p == Number(42, unit=Unit('W.h'))
    n = Number(6, unit='cm')
    p = Number(7, unit=Unit('h', exponent=Number(2)))
    assert n * p == Number(42, unit=Unit('cm.h', exponent=Number(2)))
    assert (n * p).printed == r'\SI{42}{cm.h^{2}}'
    n = Number(6, unit=Unit('cm', exponent=Number(2)))
    p = Number(7, unit='h')
    assert n * p == Number(42, unit=Unit('h.cm', exponent=Number(2)))


def test_power():
    """Check __pow__, __rpow__, __ipow__."""
    assert isinstance(pow(Number(4), Number(4)), Number)
    assert isinstance(pow(4, Number(4)), Number)
    assert isinstance(pow(Number(4), 4), Number)
    assert isinstance(Number(4) ** Number(4), Number)
    assert isinstance(4 ** Number(4), Number)
    assert isinstance(Number(4) ** 4, Number)
    n = Number(4)
    n **= Number(4)
    assert isinstance(n, Number)
    n **= 4
    assert isinstance(n, Number)


def test_divisions_errors():
    """Check divisions exceptions."""
    with pytest.raises(NotImplementedError) as excinfo:
        Number(6, unit=Unit('cm', exponent=Number(2))) \
            / Number(6, unit=Unit('dm', exponent=Number(3)))
    assert str(excinfo.value) == 'Cannot yet handle a ' \
                                 'division of Number(\'6 cm^2\') ' \
                                 'by Number(\'6 dm^3\').'


def test_divisions():
    """Check __truediv__, __floordiv__, __mod__, __divmod__ + their __r*__."""
    assert isinstance(Number(4) / Number(4), Number)
    assert isinstance(4 / Number(4), Number)
    assert isinstance(Number(4) / 4, Number)
    assert isinstance(Number(4) // Number(4), Number)
    assert isinstance(4 // Number(4), Number)
    assert isinstance(Number(4) // 4, Number)
    assert isinstance(Number(4) % Number(4), Number)
    assert isinstance(4 % Number(4), Number)
    assert isinstance(Number(4) % 4, Number)
    assert divmod(Number(42), Number(15)) == (Number('2'), Number('12'))
    assert isinstance(divmod(Number(42), Number(15))[0], Number)
    assert isinstance(divmod(Number(42), Number(15))[1], Number)
    assert divmod(42, Number(15)) == (Number('2'), Number('12'))
    assert isinstance(divmod(42, Number(15))[0], Number)
    assert isinstance(divmod(42, Number(15))[1], Number)
    assert divmod(Number(42), 15) == (Number('2'), Number('12'))
    assert isinstance(divmod(Number(42), 15)[0], Number)
    assert isinstance(divmod(Number(42), 15)[1], Number)
    n = Number(4)
    assert isinstance(n, Number)
    n /= Number(4)
    assert isinstance(n, Number)
    n = Number(256)
    n //= Number(4)
    assert isinstance(n, Number)
    n = Number(256)
    n %= Number(3)
    assert isinstance(n, Number)
    n = Number(4)
    n /= 4
    assert isinstance(n, Number)
    n = Number(256)
    n //= 4
    assert isinstance(n, Number)
    n = Number(256)
    n %= 3
    assert isinstance(n, Number)
    assert Number(4) / Sign('-') == -4
    assert Sign('-') / Number(4) == Number('-0.25')
    assert Number(4) // Sign('-') == -4
    assert Sign('-') // Number(4) == Number('0')
    n = Number(7, unit='cm')
    p = Number(4)
    assert n / p == Number('1.75', unit='cm')
    n = Number(7)
    p = Number(4, unit='cm')
    assert n / p == Number('1.75', unit=Unit('cm', exponent=Number(-1)))
    n = Number(7, unit='cm')
    p = Number(4, unit='cm')
    assert n / p == Number('1.75')
    n = Number(7, unit='km')
    p = Number(4, unit='h')
    assert n / p == Number('1.75', unit='km/h')
    n = Number(7, unit=Unit('cm', exponent=Number(2)))
    p = Number(4, unit='cm')
    assert n / p == Number('1.75', unit='cm')
    n = Number(7, unit='cm')
    p = Number(4, unit=Unit('cm', exponent=Number(2)))
    assert n / p == Number('1.75', unit=Unit('cm', exponent=Number(-1)))
    n = 7
    p = Number(4, unit=Unit('cm', exponent=Number(2)))
    assert n / p == Number('1.75', unit=Unit('cm', exponent=Number(-2)))
    n = Number(7, unit='cm')
    p = 4
    assert n / p == Number('1.75', unit='cm')
    n = 7
    p = Number(4, unit='cm')
    assert n / p == Number('1.75', unit=Unit('cm', exponent=Number(-1)))


def test_printing_errors():
    """Check exceptions raised by self.imprint()."""
    with pytest.raises(ValueError) as excinfo:
        Number('8.6').imprint(variant='undefined')
    assert str(excinfo.value) == 'variant must belong to [\'latex\', ' \
        '\'user_input\']; got \'undefined\' instead.'


def test_evaluate():
    """Check evaluate() is correct."""
    assert Number(4).evaluate() == Number(4)


def test_printing():
    """Check printing is correct."""
    assert Number('8.6').printed == '8.6'
    assert Number('8.6').imprint(mod_locale=LOCALE_US) == '8.6'
    locale.setlocale(locale.LC_ALL, LOCALE_FR)
    assert locale.str(Decimal('8.6')) == '8,6'
    assert Number('8.6').printed == '8,6'
    assert Number('8.6').uiprinted == '8.6'
    assert Number('8.6').imprint(mod_locale=LOCALE_US) == '8.6'
    assert Number('8.6').printed == '8,6'
    locale.setlocale(locale.LC_ALL, LOCALE_US)
    assert Number('8.6').imprint(start_expr=False) == '+8.6'
    required.package['siunitx'] = False
    n = Number('9', unit='cm')
    assert n.printed == r'\SI{9}{cm}'
    assert required.package['siunitx']
    assert n.uiprinted == '9 cm'
    assert str(n) == '9 cm'
    n = Number('9')
    assert str(n) == '9'
    assert Number(60, unit=Unit('cm', exponent=Number(2))).uiprinted \
        == '60 cm^2'


def test_sign():
    """Check Number.sign is correct."""
    assert Number(4).sign == '+'
    assert Number(-6).sign == '-'


def test_rounded():
    """Check rounding is good."""
    assert Number(4.2).rounded(0) == 4
    assert Number(4.2).rounded(Decimal('1'), rounding=ROUND_HALF_UP) == 4


def test_is_power_of_10():
    """Check is_power_of_10() in different cases."""
    for n in [1, 10, 100, 1000, 10000, -1, -10, -100]:
        assert Number(n).is_power_of_10()
    for n in [Decimal('0.1'), Decimal('0.01'), Decimal('0.001'),
              Decimal('-0.1'), Decimal('-0.01'), Decimal('-0.001')]:
        assert Number(n).is_power_of_10()
    for n in [0, 2, Decimal('0.5'), Decimal('-0.02'), Decimal('10.09'),
              1001, -999]:
        assert not Number(n).is_power_of_10()


def test_is_pure_half():
    """Check is_pure_half() in different cases."""
    assert Number('10.5').is_pure_half()
    assert not Number('4.25').is_pure_half()
    assert not Number('4').is_pure_half()


def test_is_pure_quarter():
    """Check is_pure_quarter() in different cases."""
    assert not Number('10.5').is_pure_quarter()
    assert Number('4.25').is_pure_quarter()
    assert Number('8.75').is_pure_quarter()
    assert not Number('4').is_pure_quarter()


def test_nonzero_digits_nb():
    """Check nonzero_digits_nb() in different cases."""
    assert Number('0').nonzero_digits_nb() == 0
    assert Number('2.0').nonzero_digits_nb() == 1
    assert Number('0.2').nonzero_digits_nb() == 1
    assert Number('0.104').nonzero_digits_nb() == 2
    assert Number('30.506').nonzero_digits_nb() == 3


def test_isolated_zeros():
    """Check isolated_zeros() in different cases."""
    assert Number('0').isolated_zeros() == 0
    assert Number('10').isolated_zeros() == 0
    assert Number('100').isolated_zeros() == 0
    assert Number('1010').isolated_zeros() == 1
    assert Number('3.871').isolated_zeros() == 0
    assert Number('3.801').isolated_zeros() == 1
    assert Number('3.001').isolated_zeros() == 2
    assert Number('3.0001').isolated_zeros() == 3
    assert Number('10.04').isolated_zeros() == 2
    assert Number('0.04').isolated_zeros() == 0
    assert Number('0.0409').isolated_zeros() == 1
    assert Number('0.3006').isolated_zeros() == 2


def test_fracdigits_nb():
    """Check fracdigits_nb() in different cases."""
    assert all(Number(n).fracdigits_nb() == 0
               for n in [0, 1, 8, Decimal(4), Decimal('4.0'),
                         Decimal('4.00000000000000000000')])
    assert all(Number(n).fracdigits_nb() == 1
               for n in [Decimal('0.4'), Decimal('10.000') / 4])
    assert all(Number(n).fracdigits_nb() == 0
               for n in [-0, -1, -8, Decimal(-4), Decimal('-4.0'),
                         Decimal('-4.00000000000000000000')])
    assert all(Number(n).fracdigits_nb() == 1
               for n in [Decimal('-0.4'), Decimal('-10.000') / 4])


def test_atomized():
    """Check atomized()."""
    assert Number('0').atomized() == [Number('0')]
    assert Number('0.683').atomized() == [Number('0.6'), Number('0.08'),
                                          Number('0.003')]
    assert Number('25.104').atomized() == [Number('20'), Number('5'),
                                           Number('0.1'), Number('0.004')]
    assert Number('25.104').atomized(keep_zeros=True) == \
        [Number('20'), Number('5'), Number('0.1'), Number('0.0'),
         Number('0.004')]


def test_overlap_level():
    """Check overlap_level()."""
    assert Number('0.724').overlap_level() == 1
    assert Number('0.714').overlap_level() == 0
    assert Number('0.704').overlap_level() == 0
    assert Number('0.74').overlap_level() == 0
    assert Number('0.7').overlap_level() == -1
    assert Number('0.7224').overlap_level() == 2
    assert Number('0.7124').overlap_level() == 1
    assert Number('0.7214').overlap_level() == 1
    assert Number('0.7024').overlap_level() == 1
    assert Number('0.7204').overlap_level() == 1
    assert Number('0.7114').overlap_level() == 0
    assert Number('0.7104').overlap_level() == 0
    assert Number('0.17').overlap_level() == 0


def test_cut_exceptions():
    """Check cut() raises exceptions in expected cases."""
    with pytest.raises(ValueError) as excinfo:
        Number(10).cut(overlap=-1)
    assert str(excinfo.value) == 'overlap must be a positive int. Got a ' \
        'negative int instead.'
    with pytest.raises(TypeError) as excinfo:
        Number(10).cut(overlap='a')
    assert str(excinfo.value) == 'When overlap is used, it must be an int. ' \
        'Got a <class \'str\'> instead.'
    with pytest.raises(ValueError) as excinfo:
        Number('4.3').cut(overlap=1)
    assert str(excinfo.value) == 'Given overlap is too high.'
    with pytest.raises(ValueError) as excinfo:
        Number('4.15').cut(overlap=1)
    assert str(excinfo.value) == 'Given overlap is too high.'
    with pytest.raises(ValueError) as excinfo:
        Number('4.683').cut(overlap=2)
    assert str(excinfo.value) == 'Only 0 <= overlap <= 1 is implemented yet.'


def test_cut():
    """Check cut() in various cases."""
    assert Number('4.3').cut() == (Number('4'), Number('0.3'))
    assert Number('4.03').cut() == (Number('4'), Number('0.03'))
    assert Number('4.63').cut(return_all=True) == \
        [(Number('4'), Number('0.63')), (Number('4.6'), Number('0.03'))]
    assert Number('5.836').cut(return_all=True) == \
        [(Number('5'), Number('0.836')),
         (Number('5.8'), Number('0.036')),
         (Number('5.83'), Number('0.006'))]
    assert Number('5.806').cut(return_all=True) == \
        [(Number('5'), Number('0.806')),
         (Number('5.8'), Number('0.006'))]
    assert Number('5.36').cut(overlap=1, return_all=True) == \
        [(Number('5.1'), Number('0.26')),
         (Number('5.2'), Number('0.16'))]
    assert Number('5.476').cut(overlap=1, return_all=True) == \
        [(Number('5.1'), Number('0.376')),
         (Number('5.2'), Number('0.276')),
         (Number('5.3'), Number('0.176')),
         (Number('5.41'), Number('0.066')),
         (Number('5.42'), Number('0.056')),
         (Number('5.43'), Number('0.046')),
         (Number('5.44'), Number('0.036')),
         (Number('5.45'), Number('0.026')),
         (Number('5.46'), Number('0.016'))]
    assert Number('25.104').cut(overlap=1, return_all=True) == \
        [(Number('21'), Number('4.104')),
         (Number('22'), Number('3.104')),
         (Number('23'), Number('2.104')),
         (Number('24'), Number('1.104'))]


def test_split_exceptions():
    """Check split() raises exceptions in expected cases."""
    with pytest.raises(ValueError):
        Number(10).split(operation='*')
    with pytest.warns(UserWarning):
        Number(1).split()
    with pytest.warns(UserWarning):
        Number('0.1').split()
    with pytest.warns(UserWarning):
        Number('0.01').split()


def test_split():
    """Check split() in different cases."""
    result = Number(14).split()
    assert type(result) is tuple
    assert len(result) is 2
    assert is_integer(result[0]) and is_integer(result[1])
    assert 1 <= result[0] <= 13
    assert 1 <= result[1] <= 13
    assert sum(result) == 14
    assert Number(14).split(return_all=True) \
        == [(1, 13), (2, 12), (3, 11), (4, 10), (5, 9), (6, 8), (7, 7),
            (8, 6), (9, 5), (10, 4), (11, 3), (12, 2), (13, 1)]
    result = Number(14).split(operation='-')
    assert all([is_integer(r) for r in result])
    assert result[0] - result[1] == 14
    result = Number('4.3').split()
    # Can not say 'all' will be decimals, because we could have: 3 + 1.3
    assert any([Number(r).fracdigits_nb() == 1 for r in result])
    result = Number(4).split(dig=2)
    assert all([Number(r).fracdigits_nb() == 2 for r in result])
    result = Number(-7).split()
    assert all(-6 <= r <= -1 for r in result)
    result = Number('4.3').split(dig=1)
    assert all([Number(r).fracdigits_nb() == 2 for r in result])
    assert Number(14).split(operation='difference', return_all=True) \
        == [(15, 1), (16, 2), (17, 3), (18, 4,), (19, 5), (20, 6), (21, 7),
            (22, 8), (23, 9), (24, 10), (25, 11), (26, 12), (27, 13)]


def test_move_fracdigits_to():
    """Check move_digits_to() in different cases."""
    with pytest.raises(TypeError):
        move_fracdigits_to(14)
    with pytest.raises(TypeError):
        move_fracdigits_to(14, (7, 5))
    with pytest.raises(TypeError):
        move_fracdigits_to(14, {7: 'a', 6: 'b'})
    with pytest.raises(TypeError):
        move_fracdigits_to(14, [7, '5'])
    with pytest.raises(TypeError):
        move_fracdigits_to('14', [7, 5])
    with pytest.raises(TypeError) as excinfo:
        move_fracdigits_to(14, ['a', Decimal('0.5')])
    assert str(excinfo.value).startswith('Expected a number, either float, '
                                         'int or Decimal')
    assert move_fracdigits_to(14, [7, 5]) == [14, 7, 5]
    assert move_fracdigits_to(14, [Decimal('0.7'), 5]) \
        == [Decimal('1.4'), Decimal(7), 5]
    assert move_fracdigits_to(14, [Decimal('0.7'), Decimal('0.5')]) \
        == [Decimal('0.14'), Decimal(7), Decimal(5)]


def test_remove_fracdigits_from():
    """Check remove_fracdigits_from() in different cases."""
    with pytest.raises(TypeError):
        remove_fracdigits_from('14', to=[])
    with pytest.raises(TypeError):
        remove_fracdigits_from(14)
    with pytest.raises(TypeError):
        remove_fracdigits_from(1.4)
    with pytest.raises(ValueError):
        remove_fracdigits_from(Decimal('1.4'), to=[])
    with pytest.raises(ValueError):
        remove_fracdigits_from(Decimal('1.4'), to=[10, 20, 30])
    with pytest.raises(TypeError):
        remove_fracdigits_from(Decimal('14'), to=[10, 20, 30])
    with pytest.raises(TypeError):
        remove_fracdigits_from(Decimal('1.4'), to=10)
    assert remove_fracdigits_from(Decimal('1.4'), to=[10, 20, 36]) ==\
        [Decimal('14'), 10, 20, Decimal('3.6')]


def test_fix_digits():
    """Check fix_digits() in different cases."""
    n1, n2 = fix_fracdigits(Decimal('0.6'), Decimal('2'))
    assert n1 == Decimal('6')
    assert n2 == Decimal('0.2')
    n1, n2 = fix_fracdigits(Decimal('0.6'), Decimal('10'))
    assert n1 == Decimal('6')
    assert not is_integer(n2)
    n1, n2, n3 = fix_fracdigits(Decimal('0.6'), Decimal('10'), Decimal('100'))
    assert n1 == Decimal('6')
    assert not is_integer(n2) or not is_integer(n3)
