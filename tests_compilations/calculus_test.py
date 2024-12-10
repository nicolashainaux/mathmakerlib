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

import subprocess
from pathlib import Path

from mathmakerlib.calculus import Table
from .compilation_manager import CompilationManager


def test1():
    t3 = Table([(1, 2), (3, 4), (5, 6)], bubble_operator='+', bubble_value='4',
               bubble_color='OliveGreen')
    t2 = Table([(1, 2), (3, 4)], bubble_value='?', bubble_color='BrickRed',
               compact=True, baseline=-5)
    content = f'{t3.printed}\n{t2.printed}'
    with CompilationManager('test1', 'article.tex', content) as cmd:
        # import sys
        # sys.stderr.write(f'cmd={cmd}\n')
        ret_code = subprocess.run(cmd, shell=True, executable='/bin/bash')\
            .returncode
        assert ret_code == 0


def test_PythagoreanEquation_compilations():
    DATA_PATH = Path(__file__).parent / 'data/pythagorean_equations'
    TEST_ABC_1 = (DATA_PATH / 'ABC_1.tex').read_text()
    TEST_ABC_2 = (DATA_PATH / 'ABC_2.tex').read_text()
    TEST_GIH = (DATA_PATH / 'GIH.tex').read_text()
    TEST_GMW = (DATA_PATH / 'GMW.tex').read_text()
    TEST_ZIP = (DATA_PATH / 'ZIP.tex').read_text()
    TEST_ZIP1 = (DATA_PATH / 'ZIP1.tex').read_text()
    TEST_ZIP2 = (DATA_PATH / 'ZIP2.tex').read_text()
    TEST_ZIP3 = (DATA_PATH / 'ZIP3.tex').read_text()
    TEST_SVK = (DATA_PATH / 'SVK.tex').read_text()
    TEST_SVK1 = (DATA_PATH / 'SVK1.tex').read_text()
    TEST_SVK2 = (DATA_PATH / 'SVK2.tex').read_text()
    TEST_SVK3 = (DATA_PATH / 'SVK3.tex').read_text()
    content = '\n'.join([TEST_ABC_1, TEST_ABC_2, TEST_GIH, TEST_GMW, TEST_ZIP,
                        TEST_ZIP1, TEST_ZIP2, TEST_ZIP3, TEST_SVK, TEST_SVK1,
                        TEST_SVK2, TEST_SVK3])
    with CompilationManager('test_PythagoreanEquation_compilations',
                            'article.tex', content) as cmd:
        ret_code = subprocess.run(cmd, shell=True, executable='/bin/bash',
                                  capture_output=True).returncode
        assert ret_code == 0


def test_TrigonometricEquation_compilations():
    DATA_PATH = Path(__file__).parent / 'data/trigonometric_equations'
    ZAD_ADJ_TAN0 = (DATA_PATH / 'ZAD_adj_tan0.tex').read_text()
    ZAD_OPP_TAN0 = (DATA_PATH / 'ZAD_opp_tan0.tex').read_text()
    ZAD_ADJ_COS0 = (DATA_PATH / 'ZAD_adj_cos0.tex').read_text()
    ZAD_HYP_COS0 = (DATA_PATH / 'ZAD_hyp_cos0.tex').read_text()
    ZAD_OPP_SIN0 = (DATA_PATH / 'ZAD_opp_sin0.tex').read_text()
    ZAD_HYP_SIN0 = (DATA_PATH / 'ZAD_hyp_sin0.tex').read_text()
    ZAD_ADJ_TAN2 = (DATA_PATH / 'ZAD_adj_tan2.tex').read_text()
    ZAD_OPP_TAN2 = (DATA_PATH / 'ZAD_opp_tan2.tex').read_text()
    ZAD_ADJ_COS2 = (DATA_PATH / 'ZAD_adj_cos2.tex').read_text()
    ZAD_HYP_COS2 = (DATA_PATH / 'ZAD_hyp_cos2.tex').read_text()
    ZAD_OPP_SIN2 = (DATA_PATH / 'ZAD_opp_sin2.tex').read_text()
    ZAD_HYP_SIN2 = (DATA_PATH / 'ZAD_hyp_sin2.tex').read_text()
    content = '\n'.join([ZAD_ADJ_TAN0, ZAD_OPP_TAN0, ZAD_ADJ_COS0,
                         ZAD_HYP_COS0, ZAD_OPP_SIN0, ZAD_HYP_SIN0,
                         ZAD_ADJ_TAN2, ZAD_OPP_TAN2, ZAD_ADJ_COS2,
                         ZAD_HYP_COS2, ZAD_OPP_SIN2, ZAD_HYP_SIN2])
    with CompilationManager('test_TrigonometricEquation_compilations',
                            'article.tex', content) as cmd:
        ret_code = subprocess.run(cmd, shell=True, executable='/bin/bash',
                                  capture_output=True).returncode
        assert ret_code == 0
