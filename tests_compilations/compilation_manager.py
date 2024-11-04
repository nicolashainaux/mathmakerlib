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

from pathlib import Path


class CompilationManager:
    """
    Simple Context Manager to create lualatex command and handle LaTeX files.

    def test_my_stuff():
        with CompilationManager('test1', 'article.tex', body_content) as cmd:
            ret_code = subprocess.run(cmd, shell=True, executable='/bin/bash',
                                      capture_output=True).returncode
            assert ret_code == 0
    """
    def __init__(self, test_name, template_name, content):
        self.content = content
        self.test_name = test_name
        self.out_tex = Path(__file__).parent / f'{test_name}.tex'
        template_path = Path(__file__).parent / f'templates/{template_name}'
        self.template = template_path.read_text()

    def __enter__(self):
        self.out_tex.write_text(self.template.replace('CONTENT', self.content))
        return f'lualatex {self.out_tex}'

    def __exit__(self, exc_class, exc, traceback):
        self.out_tex.unlink()
        for ext in ['aux', 'log', 'pdf']:
            (Path(__file__).parent.parent / f'{self.test_name}.{ext}').unlink()
