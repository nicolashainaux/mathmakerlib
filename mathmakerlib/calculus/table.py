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

from mathmakerlib import required
from mathmakerlib.core.printable import Printable


class Table(Printable):

    def __init__(self, couples, bubble_operator='×', bubble_value=None,
                 bubble_color=None):
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

    @property
    def size(self):
        """The number of columns."""
        return len(self.couples)

    @property
    def template(self):
        """The template matching self's size."""
        return (Path(__file__).parent / f'templates/table{self.size}.tikz')\
            .read_text()

    @property
    def xoffset(self):
        """The x-offset to start drawing the possible arrow and bubble."""
        return {2: '2.5', 3: '4', 4: '5.5'}[self.size]

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
            bubble_template = (Path(__file__).parent
                               / 'templates/table_bubble.tikz').read_text()
            return bubble_template.replace('BUBBLETEXT', text)\
                .replace('XOFF', self.xoffset)

    def imprint(self, start_expr=True, variant='latex'):
        required.package['tikz'] = True
        output = self.template
        for i in range(self.size):
            output = output.replace(f'XVAL{i}', str(self.couples[i][0]))
            output = output.replace(f'YVAL{i}', str(self.couples[i][1]))
        return output.replace('BUBBLE', self.bubble)
