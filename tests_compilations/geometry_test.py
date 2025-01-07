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

from .compilation_manager import CompilationManager


def test_RightTriangles_compilations():
    DATA_PATH = Path(__file__).parent / 'data/right_triangles'
    TEST_ICY1 = (DATA_PATH / 'ICY1.tex').read_text()
    TEST_LAC1 = (DATA_PATH / 'LAC1.tex').read_text()
    content = '\n'.join([TEST_ICY1, TEST_LAC1])
    with CompilationManager('test_RightTriangles_compilations',
                            'article.tex', content) as cmd:
        ret_code = subprocess.run(cmd, shell=True, executable='/bin/bash',
                                  capture_output=True).returncode
        assert ret_code == 0


def test_Angles_compilations():
    DATA_PATH = Path(__file__).parent / 'data/angles'
    TEST_XBY1 = (DATA_PATH / 'XBY1.tex').read_text()
    TEST_XBY2 = (DATA_PATH / 'XBY2.tex').read_text()
    TEST_XBY3 = (DATA_PATH / 'XBY3.tex').read_text()
    TEST_XBY4 = (DATA_PATH / 'XBY4.tex').read_text()
    TEST_XOY1 = (DATA_PATH / 'XOY1.tex').read_text()
    TEST_XOY2 = (DATA_PATH / 'XOY2.tex').read_text()
    content = '\n'.join([TEST_XBY1, TEST_XBY2, TEST_XBY3, TEST_XBY4,
                         TEST_XOY1, TEST_XOY2])
    with CompilationManager('test_Angles_compilations',
                            'article.tex', content) as cmd:
        ret_code = subprocess.run(cmd, shell=True, executable='/bin/bash',
                                  capture_output=True).returncode
        assert ret_code == 0
