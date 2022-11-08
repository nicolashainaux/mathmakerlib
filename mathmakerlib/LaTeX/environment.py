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

from . import OptionsList


class Environment(object):
    r"""
    Any LaTeX environment, structured like:
    \begin{...}[...]
    ...
    \end{...}
    """

    def __init__(self, name, content, *options):
        self.name = str(name)
        self.content = str(content)
        self._options = OptionsList(*options)

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, values):
        self._options = OptionsList(*values)

    @property
    def template(self):
        return r'''\begin{NAME}OPTIONS
CONTENT
\end{NAME}'''

    def __str__(self):
        return self.template.replace('NAME', self.name)\
            .replace('CONTENT', self.content)\
            .replace('OPTIONS', str(self.options))


class TikZPicture(Environment):
    """Shorcut for TikZ picture environment."""

    def __init__(self, content, *options):
        super().__init__('tikzpicture', content, *options)
