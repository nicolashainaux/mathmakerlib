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
from mathmakerlib.calculus.equations import TrigonometricEquation
from mathmakerlib.calculus.equations import TrigonometricFormula
from mathmakerlib.geometry import RightTriangle

DATA_PATH = Path(__file__).parent.parent.parent \
    / 'tests_compilations/data/trigonometric_equations'

ZAD_OPP_TAN0 = (DATA_PATH / 'ZAD_opp_tan0.tex').read_text()
ZAD_ADJ_TAN0 = (DATA_PATH / 'ZAD_adj_tan0.tex').read_text()
ZAD_ADJ_COS0 = (DATA_PATH / 'ZAD_adj_cos0.tex').read_text()
ZAD_HYP_COS0 = (DATA_PATH / 'ZAD_hyp_cos0.tex').read_text()
ZAD_OPP_SIN0 = (DATA_PATH / 'ZAD_opp_sin0.tex').read_text()
ZAD_HYP_SIN0 = (DATA_PATH / 'ZAD_hyp_sin0.tex').read_text()

ZAD_OPP_TAN2 = (DATA_PATH / 'ZAD_opp_tan2.tex').read_text()
ZAD_ADJ_TAN2 = (DATA_PATH / 'ZAD_adj_tan2.tex').read_text()
ZAD_ADJ_COS2 = (DATA_PATH / 'ZAD_adj_cos2.tex').read_text()
ZAD_HYP_COS2 = (DATA_PATH / 'ZAD_hyp_cos2.tex').read_text()
ZAD_OPP_SIN2 = (DATA_PATH / 'ZAD_opp_sin2.tex').read_text()
ZAD_HYP_SIN2 = (DATA_PATH / 'ZAD_hyp_sin2.tex').read_text()

TAO_ANGLE_TAN0 = (DATA_PATH / 'TAO_angle_tan0.tex').read_text()
TAO_ANGLE_TAN2 = (DATA_PATH / 'TAO_angle_tan2.tex').read_text()
TAO_ANGLE_COS0 = (DATA_PATH / 'TAO_angle_cos0.tex').read_text()
TAO_ANGLE_COS2 = (DATA_PATH / 'TAO_angle_cos2.tex').read_text()
TAO_ANGLE_SIN0 = (DATA_PATH / 'TAO_angle_sin0.tex').read_text()
TAO_ANGLE_SIN2 = (DATA_PATH / 'TAO_angle_sin2.tex').read_text()


@pytest.fixture
def t6():
    t6 = RightTriangle(name='ZAD', rotation_angle=90)
    # t6.setup_labels([Number('3'), Number('2.5'), None])
    return t6


@pytest.fixture
def t7():
    t7 = RightTriangle(name='TAO')
    return t7


def test_TrigonometricEquation_instanciation_error(t6):
    with pytest.raises(ValueError) as excinfo:
        TrigonometricEquation(t6)
    assert str(excinfo.value) == 'The provided object (expected: '\
        'RightTriangle, provided: RightTriangle) has not been set up '\
        "for trigonometry. rt._trigo_setup == ''"


def test_TrigonometricFormula_imprint(t6):
    assert TrigonometricFormula(t6, 'tan', 0).printed \
        == r'\[tan(\text{\angle AZD})=\frac{\text{AD}}{\text{AZ}}\]'
    assert TrigonometricFormula(t6, 'tan', 2).printed \
        == r'\[tan(\text{\angle ZDA})=\frac{\text{AZ}}{\text{AD}}\]'
    assert TrigonometricFormula(t6, 'cos', 0).printed \
        == r'\[cos(\text{\angle AZD})=\frac{\text{ZA}}{\text{ZD}}\]'
    assert TrigonometricFormula(t6, 'cos', 2).printed \
        == r'\[cos(\text{\angle ZDA})=\frac{\text{DA}}{\text{DZ}}\]'
    assert TrigonometricFormula(t6, 'sin', 0).printed \
        == r'\[sin(\text{\angle AZD})=\frac{\text{DA}}{\text{DZ}}\]'
    assert TrigonometricFormula(t6, 'sin', 2).printed \
        == r'\[sin(\text{\angle ZDA})=\frac{\text{ZA}}{\text{ZD}}\]'


def test_TrigonometricEquation_autosolve_opp_tan0(t6):
    t6.setup_for_trigonometry(angle_nb=0, trigo_fct='tan',
                              angle_val=Number(32, unit=r'\degree'),
                              down_length_val=Number('3.5', unit='cm'))
    eq = TrigonometricEquation(t6)
    assert eq.autosolve(required_rounding=Decimal('1.00')) == ZAD_OPP_TAN0


def test_TrigonometricEquation_autosolve_adj_tan0(t6):
    t6.setup_for_trigonometry(angle_nb=0, trigo_fct='tan',
                              angle_val=Number(40, unit=r'\degree'),
                              up_length_val=Number(18, unit='mm'))
    eq = TrigonometricEquation(t6)
    assert eq.autosolve(required_rounding=Decimal('1.000')) == ZAD_ADJ_TAN0


def test_TrigonometricEquation_autosolve_adj_cos0(t6):
    t6.setup_for_trigonometry(angle_nb=0, trigo_fct='cos',
                              angle_val=Number(36, unit=r'\degree'),
                              down_length_val=Number(53, unit='dm'))
    eq = TrigonometricEquation(t6)
    assert eq.autosolve(required_rounding=Decimal('1.00')) == ZAD_ADJ_COS0


def test_TrigonometricEquation_autosolve_hyp_cos0(t6):
    t6.setup_for_trigonometry(angle_nb=0, trigo_fct='cos',
                              angle_val=Number(80, unit=r'\degree'),
                              up_length_val=Number(53, unit='km'))
    eq = TrigonometricEquation(t6)
    assert eq.autosolve(required_rounding=Decimal('1.0')) == ZAD_HYP_COS0


def test_TrigonometricEquation_autosolve_opp_sin0(t6):
    t6.setup_for_trigonometry(angle_nb=0, trigo_fct='sin',
                              angle_val=Number(57, unit=r'\degree'),
                              down_length_val=Number(19, unit='hm'))
    eq = TrigonometricEquation(t6)
    assert eq.autosolve(required_rounding=Decimal('1.00')) == ZAD_OPP_SIN0


def test_TrigonometricEquation_autosolve_hyp_sin0(t6):
    t6.setup_for_trigonometry(angle_nb=0, trigo_fct='sin',
                              angle_val=Number(39, unit=r'\degree'),
                              up_length_val=Number(48, unit='m'))
    eq = TrigonometricEquation(t6)
    assert eq.autosolve(required_rounding=Decimal('1.0')) == ZAD_HYP_SIN0


def test_TrigonometricEquation_autosolve_opp_tan2(t6):
    t6.setup_for_trigonometry(angle_nb=2, trigo_fct='tan',
                              angle_val=Number(32, unit=r'\degree'),
                              down_length_val=Number('3.5', unit='cm'))
    eq = TrigonometricEquation(t6)
    assert eq.autosolve(required_rounding=Decimal('1.00')) == ZAD_OPP_TAN2


def test_TrigonometricEquation_autosolve_adj_tan2(t6):
    t6.setup_for_trigonometry(angle_nb=2, trigo_fct='tan',
                              angle_val=Number(40, unit=r'\degree'),
                              up_length_val=Number(18, unit='mm'))
    eq = TrigonometricEquation(t6)
    assert eq.autosolve(required_rounding=Decimal('1.000')) == ZAD_ADJ_TAN2


def test_TrigonometricEquation_autosolve_adj_cos2(t6):
    t6.setup_for_trigonometry(angle_nb=2, trigo_fct='cos',
                              angle_val=Number(36, unit=r'\degree'),
                              down_length_val=Number(53, unit='dm'))
    eq = TrigonometricEquation(t6)
    assert eq.autosolve(required_rounding=Decimal('1.00')) == ZAD_ADJ_COS2


def test_TrigonometricEquation_autosolve_hyp_cos2(t6):
    t6.setup_for_trigonometry(angle_nb=2, trigo_fct='cos',
                              angle_val=Number(80, unit=r'\degree'),
                              up_length_val=Number(53, unit='km'))
    eq = TrigonometricEquation(t6)
    assert eq.autosolve(required_rounding=Decimal('1.0')) == ZAD_HYP_COS2


def test_TrigonometricEquation_autosolve_opp_sin2(t6):
    t6.setup_for_trigonometry(angle_nb=2, trigo_fct='sin',
                              angle_val=Number(57, unit=r'\degree'),
                              down_length_val=Number(19, unit='hm'))
    eq = TrigonometricEquation(t6)
    assert eq.autosolve(required_rounding=Decimal('1.00')) == ZAD_OPP_SIN2


def test_TrigonometricEquation_autosolve_hyp_sin2(t6):
    t6.setup_for_trigonometry(angle_nb=2, trigo_fct='sin',
                              angle_val=Number(39, unit=r'\degree'),
                              up_length_val=Number(48, unit='m'))
    eq = TrigonometricEquation(t6)
    assert eq.autosolve(required_rounding=Decimal('1.0')) == ZAD_HYP_SIN2


def test_TrigonometricEquation_autosolve_angle_tan0(t7):
    t7.setup_for_trigonometry(angle_nb=0, trigo_fct='tan',
                              up_length_val=Number(9, unit='cm'),
                              down_length_val=Number(9, unit='cm'))
    eq = TrigonometricEquation(t7)
    assert eq.autosolve(required_rounding=Decimal('1.0')) == TAO_ANGLE_TAN0


def test_TrigonometricEquation_autosolve_angle_tan2(t7):
    t7.setup_for_trigonometry(angle_nb=2, trigo_fct='tan',
                              up_length_val=Number(3, unit='cm'),
                              down_length_val=Number(10, unit='cm'))
    eq = TrigonometricEquation(t7)
    assert eq.autosolve(required_rounding=Decimal('1.0')) == TAO_ANGLE_TAN2


def test_TrigonometricEquation_autosolve_angle_cos0(t7):
    t7.setup_for_trigonometry(angle_nb=0, trigo_fct='cos',
                              up_length_val=Number(3, unit='cm'),
                              down_length_val=Number(5, unit='cm'))
    eq = TrigonometricEquation(t7)
    assert eq.autosolve(required_rounding=Decimal('1.00')) == TAO_ANGLE_COS0


def test_TrigonometricEquation_autosolve_angle_cos2(t7):
    t7.setup_for_trigonometry(angle_nb=2, trigo_fct='cos',
                              up_length_val=Number(4, unit='cm'),
                              down_length_val=Number(5, unit='cm'))
    eq = TrigonometricEquation(t7)
    assert eq.autosolve(required_rounding=Decimal('1.0')) == TAO_ANGLE_COS2


def test_TrigonometricEquation_autosolve_angle_sin0(t7):
    t7.setup_for_trigonometry(angle_nb=0, trigo_fct='sin',
                              up_length_val=Number(3, unit='cm'),
                              down_length_val=Number(5, unit='cm'))
    eq = TrigonometricEquation(t7)
    assert eq.autosolve(required_rounding=Decimal('1.00')) == TAO_ANGLE_SIN0


def test_TrigonometricEquation_autosolve_angle_sin2(t7):
    t7.setup_for_trigonometry(angle_nb=2, trigo_fct='sin',
                              up_length_val=Number(4, unit='cm'),
                              down_length_val=Number(5, unit='cm'))
    eq = TrigonometricEquation(t7)
    assert eq.autosolve(required_rounding=Decimal('1.0')) == TAO_ANGLE_SIN2
