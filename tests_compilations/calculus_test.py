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
    with CompilationManager('test1', 'article.tex', t3.printed) as cmd:
        # import sys
        # sys.stderr.write(f'cmd={cmd}\n')
        # subprocess.run(cmd, shell=True, executable='/bin/bash')
        ret_code = subprocess.run(cmd, shell=True, executable='/bin/bash',
                                  capture_output=True).returncode
        assert ret_code == 0


def test_PythagoreanEquation_compilations():
    DATA_PATH = Path(__file__).parent / 'data/pythagorean_equations'
    TEST_ABC_1 = (DATA_PATH / 'ABC_1.tex').read_text()
    TEST_ABC_2 = (DATA_PATH / 'ABC_2.tex').read_text()
    TEST_GIH = (DATA_PATH / 'GIH.tex').read_text()
    TEST_GMW = (DATA_PATH / 'GMW.tex').read_text()
    content = '\n'.join([TEST_ABC_1, TEST_ABC_2, TEST_GIH, TEST_GMW])
    with CompilationManager('test_PythagoreanEquation_compilations',
                            'article.tex', content) as cmd:
        ret_code = subprocess.run(cmd, shell=True, executable='/bin/bash',
                                  capture_output=True).returncode
        assert ret_code == 0
