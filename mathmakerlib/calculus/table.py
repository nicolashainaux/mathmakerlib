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

import copy
from pathlib import Path

from mathmakerlib import required
from mathmakerlib.core.printable import Printable
from mathmakerlib.LaTeX import AttrList, TikZPicture


class Table(Printable):

    def __init__(self, couples, bubble_operator='×', bubble_value=None,
                 bubble_color=None, compact=False, baseline=None):
        if len(couples) not in [2, 3, 4]:
            raise ValueError(f'Only tables of 2, 3 or 4 columns may be created'
                             f' so far; but got {len(couples)} couple(s).')
        if any(len(couple) != 2 for couple in couples):
            raise ValueError('Only couples may be provided to build a table, '
                             'got one tuple, at least, of length != 2')
        self.couples = couples
        self.bubble_operator = bubble_operator
        self.bubble_value = bubble_value
        self.bubble_color = bubble_color
        self.compact = compact
        if baseline is None:
            self.baseline = ''
        else:
            self.baseline = baseline
        self._options_list = [
            {'roundnode/.style': AttrList('circle', 'thick',
                                          {'draw': 'black'},
                                          {'fill': 'black!1'},
                                          {'inner sep': '0.5mm'},
                                          {'radius': '0.3cm'})}]

    @property
    def size(self):
        """The number of columns."""
        return len(self.couples)

    @property
    def compact_suffix(self):
        """'_compact' if self.compact else ''."""
        return '_compact' if self.compact else ''

    @property
    def template(self):
        """The template matching self's size."""
        fn = f'templates/table{self.size}{self.compact_suffix}.tikz'
        return (Path(__file__).parent / fn).read_text()

    @property
    def xoffset(self):
        """The x-offset to start drawing the possible arrow and bubble."""
        if self.compact:
            offsets = {2: '1.65', 3: '2.75', 4: '3.85'}
        else:
            offsets = {2: '2.5', 3: '4', 4: '5.5'}
        return offsets[self.size]

    @property
    def options_list(self):
        options = copy.deepcopy(self._options_list)
        if self.baseline:
            options.append({'baseline': self.baseline})
        return options

    @property
    def bubble(self):
        """The tikz code to draw an arrow, bubble and its content; if any."""
        if self.bubble_value is None:
            return ''
        else:
            text = f'{self.bubble_operator}{self.bubble_value}'
            if self.bubble_color:
                text = r'\textcolor{{{color}}}{{{text}}}'\
                    .format(color=self.bubble_color, text=text)
            fn = f'table_bubble{self.compact_suffix}.tikz'
            bubble_template = (Path(__file__).parent / f'templates/{fn}')\
                .read_text()
            return bubble_template.replace('BUBBLETEXT', text)\
                .replace('XOFF', self.xoffset)

    def imprint(self, start_expr=True, variant='latex'):
        required.package['tikz'] = True
        content = self.template
        for i in range(self.size):
            content = content.replace(f'XVAL{i}', str(self.couples[i][0]))
            content = content.replace(f'YVAL{i}', str(self.couples[i][1]))
        content = content.replace('BUBBLE', self.bubble)
        return str(TikZPicture(content, *self.options_list))
