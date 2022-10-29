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

from mathmakerlib.calculus import Table
from .compilation_manager import CompilationManager


def test1():
    t3 = Table([(1, 2), (3, 4), (5, 6)], bubble_operator='+', bubble_value='4',
               bubble_color='OliveGreen')
    with CompilationManager('test1', 'article.tex', t3.printed) as cmd:
        import sys
        sys.stderr.write(f'cmd={cmd}\n')
        subprocess.run('lualatex --version', shell=True,
                       executable='/bin/bash')
        ret_code = subprocess.run(cmd, shell=True, executable='/bin/bash',
                                  capture_output=True).returncode
        assert ret_code == 0
