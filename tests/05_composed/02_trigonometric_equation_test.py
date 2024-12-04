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
# from pathlib import Path
# from decimal import Decimal

from mathmakerlib.calculus import Number
from mathmakerlib.calculus.equations import TrigonometricEquation
from mathmakerlib.geometry import RightTriangle

# DATA_PATH = Path(__file__).parent.parent.parent \
#     / 'tests_compilations/data/trigonometric_equations'

# TEST_ABC_1 = (DATA_PATH / 'ABC_1.tex').read_text()


@pytest.fixture
def t6():
    t6 = RightTriangle(name='ZAD', rotation_angle=90)
    # t6.setup_labels([Number('3'), Number('2.5'), None])
    return t6


def test_TrigonometricEquation_instanciation_error(t6):
    with pytest.raises(ValueError) as excinfo:
        TrigonometricEquation(t6)
    assert str(excinfo.value) == 'The provided object (expected: '\
        'RightTriangle, provided: RightTriangle) has not been set up '\
        'for trigonometry.'


def test_TrigonometricEquation_imprint(t6):
    t6.setup_for_trigonometry(angle_nb=0, trigo_fct='tan',
                              angle_val=Number('32', unit='\\textdegree'),
                              down_length_val=Number('3.5', unit='cm'),
                              length_unit='cm')
    assert TrigonometricEquation(t6).printed \
        == r'\[tan(\widehat{\text{\angle AZD}})=\frac{\text{AD}}{\text{AZ}}\]'
    t6.setup_for_trigonometry(angle_nb=2, trigo_fct='tan',
                              angle_val=Number('32', unit='\\textdegree'),
                              down_length_val=Number('3.5', unit='cm'),
                              length_unit='cm')
    assert TrigonometricEquation(t6).printed \
        == r'\[tan(\widehat{\text{\angle ZDA}})=\frac{\text{AZ}}{\text{AD}}\]'
    t6.setup_for_trigonometry(angle_nb=0, trigo_fct='cos',
                              angle_val=Number('32', unit='\\textdegree'),
                              down_length_val=Number('3.5', unit='cm'),
                              length_unit='cm')
    assert TrigonometricEquation(t6).printed \
        == r'\[cos(\widehat{\text{\angle AZD}})=\frac{\text{ZA}}{\text{ZD}}\]'
    t6.setup_for_trigonometry(angle_nb=2, trigo_fct='cos',
                              angle_val=Number('32', unit='\\textdegree'),
                              down_length_val=Number('3.5', unit='cm'),
                              length_unit='cm')
    assert TrigonometricEquation(t6).printed \
        == r'\[cos(\widehat{\text{\angle ZDA}})=\frac{\text{DA}}{\text{DZ}}\]'
    t6.setup_for_trigonometry(angle_nb=0, trigo_fct='sin',
                              angle_val=Number('32', unit='\\textdegree'),
                              down_length_val=Number('3.5', unit='cm'),
                              length_unit='cm')
    assert TrigonometricEquation(t6).printed \
        == r'\[sin(\widehat{\text{\angle AZD}})=\frac{\text{DA}}{\text{DZ}}\]'
    t6.setup_for_trigonometry(angle_nb=2, trigo_fct='sin',
                              angle_val=Number('32', unit='\\textdegree'),
                              down_length_val=Number('3.5', unit='cm'),
                              length_unit='cm')
    assert TrigonometricEquation(t6).printed \
        == r'\[sin(\widehat{\text{\angle ZDA}})=\frac{\text{ZA}}{\text{ZD}}\]'
