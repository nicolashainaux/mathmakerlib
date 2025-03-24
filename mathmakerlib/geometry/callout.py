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
from mathmakerlib.calculus import Number, weighted_average
from mathmakerlib.core import surrounding_keys
from mathmakerlib.core.drawable import Colored, Fillable, HasThickness

# This is only meant for 6 cm long arms of the angle. Possibly this doesn't
# fit well with other lengths. See toolbox/callout_positioning.py and .ods
# These values are also meant for a decoration radius of 1 cm; if this radius
# is lower, then decrease the matching radial distance and shorten values of
# the same amount; if it's higher, then there's no need to change the values
# because it means the angle is narrow, so the callout will already be far
# from the decoration.
# {measure in degrees: (polar angle correction,
#                       radial distance as % of arms_length,
#                       callout pointer shorten as % of arms_length)
CALLOUT_POSITIONING = {5: (1, '1.292', '0.958'),
                       10: ('1.5', '1.25', '0.917'),
                       15: ('1.63', '1.208', '0.833'),
                       20: ('1.75', '1.167', '0.75'),
                       25: ('1.88', '1.125', '0.708'),
                       30: (2, '1.083', '0.667'),
                       35: ('2.5', '0.983', '0.567'),
                       40: (3, '0.867', '0.45'),
                       45: ('3.5', '0.778', '0.367'),
                       50: (4, '0.667', '0.292'),
                       55: (5, '0.667', '0.267'),
                       60: (7, '0.667', '0.25'),
                       80: (7, '0.5', '0.167')}


def _average_triple(angle):
    angle1, angle2 = surrounding_keys(angle, CALLOUT_POSITIONING)
    w1 = angle2 - angle
    w2 = angle - angle1
    values1 = CALLOUT_POSITIONING[angle1]
    values2 = CALLOUT_POSITIONING[angle2]
    return (weighted_average(Number(values1[0]), Number(values2[0]), w1, w2),
            weighted_average(Number(values1[1]), Number(values2[1]), w1, w2),
            weighted_average(Number(values1[2]), Number(values2[2]), w1, w2))


def _convert(triple, arms_length):
    return (Number(triple[0]),
            Number(round(arms_length * Number(triple[1]), 2), unit='cm')
            .standardized(),
            Number(round(arms_length * Number(triple[2]), 2), unit='cm')
            .standardized())


def callout_positioning(angle, arms_length=6):
    # See comment before CALLOUT_POSITIONING: using another value than 6
    # for the arms_length might not work as expected. This is yet to test.
    arms_length = Number(arms_length)
    if angle <= 5:
        return _convert(CALLOUT_POSITIONING[5], arms_length)
    elif angle >= 80:
        return _convert(CALLOUT_POSITIONING[80], arms_length)
    elif angle in CALLOUT_POSITIONING:
        return _convert(CALLOUT_POSITIONING[angle], arms_length)
    else:
        return _convert(_average_triple(angle), arms_length)


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
