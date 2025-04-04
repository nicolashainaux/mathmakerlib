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

import pytest
from pathlib import Path
from decimal import Decimal

from mathmakerlib.calculus import Number
from mathmakerlib.calculus.equations import PythagoreanEquation
from mathmakerlib.geometry import RightTriangle

DATA_PATH = Path(__file__).parent.parent.parent \
    / 'tests_compilations/data/pythagorean_equations'

TEST_ABC_1 = (DATA_PATH / 'ABC_1.tex').read_text()
TEST_ABC_2 = (DATA_PATH / 'ABC_2.tex').read_text()
TEST_GIH = (DATA_PATH / 'GIH.tex').read_text()
TEST_GMW = (DATA_PATH / 'GMW.tex').read_text()
TEST_GMW2 = (DATA_PATH / 'GMW2.tex').read_text()
TEST_ZIP = (DATA_PATH / 'ZIP.tex').read_text()
TEST_ZIP1 = (DATA_PATH / 'ZIP1.tex').read_text()
TEST_ZIP2 = (DATA_PATH / 'ZIP2.tex').read_text()
TEST_ZIP3 = (DATA_PATH / 'ZIP3.tex').read_text()
TEST_SVK = (DATA_PATH / 'SVK.tex').read_text()
TEST_SVK1 = (DATA_PATH / 'SVK1.tex').read_text()
TEST_SVK2 = (DATA_PATH / 'SVK2.tex').read_text()
TEST_SVK3 = (DATA_PATH / 'SVK3.tex').read_text()


def test_PythagoreanEquation_imprint():
    r = RightTriangle(name='ABC')
    r.setup_labels(labels=[Number(3, unit='cm'),
                           Number(4, unit='cm'),
                           None],
                   masks=[None, None, ' '])
    assert PythagoreanEquation(r).printed == \
        r'\text{CA}^{2}=\text{AB}^{2}+\text{BC}^{2}'

    assert PythagoreanEquation(r).imprint(neq=True) == \
        r'\text{CA}^{2}\neq \text{AB}^{2}+\text{BC}^{2}'


def test_PythagoreanEquation_calculate_square_hyp():
    r = RightTriangle(name='ABC')
    r.setup_labels(labels=[Number(55, unit='cm'),
                           Number(48, unit='cm'),
                           Number(73, unit='cm')],
                   masks=[None, None, None])
    assert PythagoreanEquation(r).calculate_square_hyp() == \
        r"""\[\text{CA}^{2}=73^{2}\]
\[\text{CA}^{2}=5329\]
"""


def test_PythagoreanEquation_calculate_square_legs_sum():
    r = RightTriangle(name='ABC')
    r.setup_labels(labels=[Number(55, unit='cm'),
                           Number(48, unit='cm'),
                           Number(73, unit='cm')],
                   masks=[None, None, None])
    assert PythagoreanEquation(r).calculate_square_legs_sum() == \
        r"""\[\text{AB}^{2}+\text{BC}^{2}=55^{2}+48^{2}\]
\[\text{AB}^{2}+\text{BC}^{2}=5329\]
"""


def test_PythagoreanEquation_calculate_hyp():
    r = RightTriangle(name='ABC')
    r.setup_labels(labels=[Number(3, unit='cm'),
                           Number(4, unit='cm'),
                           None],
                   masks=[None, None, ' '])

    with pytest.raises(ValueError) as excinfo:
        PythagoreanEquation(r).autosolve('hypo')
    assert str(excinfo.value) == "Expected a value belonging to ['leg0', "\
        "'leg1', 'hyp']; got 'hypo' instead."

    assert PythagoreanEquation(r).autosolve('hyp') == TEST_ABC_1

    r.setup_labels(labels=[Number(3, unit='cm'),
                           Number(5, unit='cm'),
                           None],
                   masks=[None, None, ' '])
    assert PythagoreanEquation(r).autosolve('hyp') == TEST_ABC_2

    r = RightTriangle(name='GIH')
    r.setup_labels(labels=[Number(145, unit='mm'),
                           Number(168, unit='mm'),
                           None],
                   masks=[None, None, ' '])
    assert PythagoreanEquation(r)\
        .autosolve('hyp', show_squares_step=True,
                   required_rounding=Decimal('0.01')) == TEST_GIH

    r = RightTriangle(name='GMW')
    r.setup_labels(labels=[Number('0.8', unit='m'),
                           Number('1.5', unit='m'),
                           None],
                   masks=[None, None, ' '])
    assert PythagoreanEquation(r)\
        .autosolve('hyp', required_rounding=Decimal('0.1')) == TEST_GMW
    assert PythagoreanEquation(r).autosolve('hyp') == TEST_GMW

    r = RightTriangle(name='GMW')
    r.setup_labels(labels=[Number('1.2', unit='m'),
                           Number('1.6', unit='m'),
                           None],
                   masks=[None, None, ' '])
    assert PythagoreanEquation(r).autosolve('hyp') == TEST_GMW2


def test_PythagoreanEquation_calculate_leg0():
    r = RightTriangle(name='ZIP')
    r.setup_labels(labels=[None,
                           Number('15.4', unit='dm'),
                           Number('17', unit='dm')],
                   masks=[' ', None, None])

    assert PythagoreanEquation(r).autosolve('leg0') == TEST_ZIP
    assert PythagoreanEquation(r).autosolve('leg0', show_squares_step=True) \
        == TEST_ZIP1
    assert PythagoreanEquation(r).autosolve(
        'leg0', shortcut_mode=False, show_squares_step=True) == TEST_ZIP2
    assert PythagoreanEquation(r).autosolve(
        'leg0', shortcut_mode=False) == TEST_ZIP3


def test_PythagoreanEquation_calculate_leg1():
    r = RightTriangle(name='SVK')
    r.setup_labels(labels=[Number('37', unit='dm'),
                           None,
                           Number('68', unit='dm')],
                   masks=[None, ' ', None])

    assert PythagoreanEquation(r).autosolve(
        'leg1', required_rounding=Decimal('0.01')) == TEST_SVK
    assert PythagoreanEquation(r).autosolve(
        'leg1', required_rounding=Decimal('0.01'), show_squares_step=True) \
        == TEST_SVK1
    assert PythagoreanEquation(r).autosolve(
        'leg1', shortcut_mode=False, show_squares_step=True,
        required_rounding=Decimal('0.01')) == TEST_SVK2
    assert PythagoreanEquation(r).autosolve(
        'leg1', shortcut_mode=False, required_rounding=Decimal('0.01')) \
        == TEST_SVK3


def test_PythagoreanEquation_autotest():
    r = RightTriangle(name='TAO')
    r.setup_labels(labels=[Number('96', unit='dm'),
                           Number('40', unit='dm'),
                           Number('104', unit='dm')])
    assert PythagoreanEquation(r).autotest() == \
        r"""On one hand:
\[\text{OT}^{2}=104^{2}\]
\[\text{OT}^{2}=10816\]

On the other hand:
\[\text{TA}^{2}+\text{AO}^{2}=96^{2}+40^{2}\]
\[\text{TA}^{2}+\text{AO}^{2}=10816\]

Hence: $\text{OT}^{2}=\text{TA}^{2}+\text{AO}^{2}$ \newline
So, by the converse of the pythagorean theorem, TAO has a right angle in A.
"""

    r.setup_labels(labels=[Number('96', unit='dm'),
                           Number('40', unit='dm'),
                           Number('105', unit='dm')])
    assert PythagoreanEquation(r).autotest() == \
        (r"""On one hand:
\[\text{OT}^{2}=105^{2}\]
\[\text{OT}^{2}=11025\]

On the other hand:
\[\text{TA}^{2}+\text{AO}^{2}=96^{2}+40^{2}\]
\[\text{TA}^{2}+\text{AO}^{2}=10816\]

Hence: $\text{OT}^{2}\neq \text{TA}^{2}+\text{AO}^{2}$ \newline
So, by the contrapositive of the pythagorean theorem, """
         r"""TAO has no right angle.
""")
