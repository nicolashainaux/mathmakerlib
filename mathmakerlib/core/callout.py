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

from mathmakerlib import required
from .drawable import Colored, Fillable, HasThickness


class Callout(Colored, Fillable, HasThickness):

    def __init__(self, content, radial_distance, polar_angle, thickness=None,
                 color=None, fillcolor=None, style='default',
                 absolute_pointer=None, relative_pointer=None, shorten=None):
        if not [absolute_pointer, relative_pointer].count(None) == 1:
            raise ValueError(f'Exactly one among absolute_pointer and '
                             f'relative_pointer must be None. Instead, got '
                             f'"{absolute_pointer}" and "{relative_pointer}".')
        self.content = content
        self.radial_distance = radial_distance
        self.polar_angle = polar_angle
        self.thickness = thickness
        self.color = color
        self.fillcolor = fillcolor
        if style == 'default':
            style = 'callout_style1'
        self.style = style
        self.shorten = shorten
        self.absolute_pointer = absolute_pointer
        self.relative_pointer = relative_pointer

    def generate_tikz(self):
        required.package['tikz'] = True
        required.tikz_library['shapes.geometric'] = True
        required.tikz_library['shapes.callouts'] = True
        required.tikz_library['arrows.meta'] = True
        required.tikz_library['positioning'] = True
        attr_list = []
        if self.absolute_pointer:
            attr_list.append(f'callout absolute pointer=('
                             f'{self.absolute_pointer})')
        if self.relative_pointer:
            attr_list.append('callout relative pointer={'
                             f'({self.relative_pointer[0]},'
                             f'{self.relative_pointer[1]})'
                             '}')
        if self.style:
            attr_list.append(self.style)
            if self.style in required.callout_style:
                required.callout_style[self.style] = True
        if self.shorten:
            attr_list.append(f'callout pointer shorten={self.shorten}')
        if self.color:
            attr_list.append(f'draw={self.color}')
        if self.thickness:
            if not self.color:
                attr_list.append('draw')
            attr_list.append(self.thickness)
        if self.fillcolor:
            attr_list.append(f'fill={self.fillcolor}')
        attr_list = ', '.join(attr_list)
        coordinates = f'({self.polar_angle}:{self.radial_distance})'
        return r'\node[{attr_list}] at {coordinates} {{{content}}};'\
            .format(attr_list=attr_list, coordinates=coordinates,
                    content=self.content)
