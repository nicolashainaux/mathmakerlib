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

from decimal import Decimal

from mathmakerlib.core.drawable import check_color, tikz_options_list
from mathmakerlib.calculus.tools import is_number, is_integer
from mathmakerlib.calculus.number import Number
from mathmakerlib.geometry.linesegment import LineSegment


class DividedLineSegment(LineSegment):

    def __init__(self, *points, thickness='ultra thick', label=None,
                 label_mask=None,
                 label_position='anticlockwise',
                 draw_endpoints=True, label_endpoints=False, color=None,
                 n=None, inner_points_shape='|',
                 endpoints_shape_as_inner_points=True,
                 fill=0, fillcolor='LimeGreen'):
        """
        Initialize DividedLineSegment

        First parameters are the same as for LineSegment. Default values may
        differ, though.
        The endpoints will be set to the same shape as others (they must be
        modified after initialization if desired another way).
        """
        LineSegment.__init__(self, *points, thickness=thickness, label=label,
                             label_mask=label_mask,
                             label_position=label_position,
                             draw_endpoints=draw_endpoints,
                             label_endpoints=label_endpoints,
                             color=color)
        self.n = n
        self.fill = fill
        self.inner_points_shape = inner_points_shape
        if endpoints_shape_as_inner_points:
            self.endpoints[0].shape = inner_points_shape
            self.endpoints[1].shape = inner_points_shape
        self._comment_designation = 'Divided Line Segment'
        self.fillcolor = fillcolor

    def __repr__(self):
        return 'DividedLineSegment({}, {}, {}/{}, {})' \
            .format(repr(self.endpoints[0]),
                    repr(self.endpoints[1]),
                    self.fill, self.n,
                    self.fillcolor)

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, n):
        if not (is_number(n) and is_integer(n) and n >= 1):
            raise TypeError('n must be an integer >= 1, got {} instead.'
                            .format(n))
        self._n = Number(n)

    @property
    def fill(self):
        return self._fill

    @fill.setter
    def fill(self, value):
        if not (is_integer(value) and 1 <= value <= self.n):
            raise TypeError('fill must be an 1 <= integer <= self.n == {}, '
                            'got {} instead.'
                            .format(self.n, value))
        self._fill = Number(value)

    @property
    def inner_points_shape(self):
        return self._inner_points_shape

    @inner_points_shape.setter
    def inner_points_shape(self, other):
        self._inner_points_shape = str(other)

    @property
    def fillcolor(self):
        return self._fillcolor

    @fillcolor.setter
    def fillcolor(self, value):
        check_color(value)
        self._fillcolor = value

    @property
    def fillpoint(self):
        fp = ([self.endpoints[0]] + self.dividing_points(self.n)
              + [self.endpoints[1]])[int(self.fill)]
        fp.x = fp.x.rounded(Decimal('0.001'))
        fp.y = fp.y.rounded(Decimal('0.001'))
        return fp

    def tikz_graduations(self):
        """Return the DividedLineSegment's nodes' list."""
        points_list = [(((i + 1) / self.n).rounded(Decimal('0.001')),
                        self.inner_points_shape)
                       for i in range(int(self.n - 1))]
        if self.draw_endpoints:
            points_list = [(0, self.endpoints[0].shape)] + points_list
            points_list = points_list + [(1, self.endpoints[1].shape)]
        return ' '.join(['node[opacity=1, pos={}, sloped] {}'
                         .format(position, '{' + shape + '}')
                         for (position, shape) in points_list])

    def tikz_declarations(self):
        """Return the DividedLineSegment's Points' declarations."""
        return '{}\n{}\n{}'\
            .format(self.endpoints[0].tikz_declarations(),
                    self.endpoints[1].tikz_declarations(),
                    self.fillpoint.tikz_declarations())

    def tikz_drawing_comment(self):
        """Return the comments preceding the DividedLineSegment's drawings."""
        return ['% Draw {}'.format(self._comment_designation)]

    def tikz_draw(self):
        """Return the command to actually draw the DividedLineSegment."""
        output = []
        draw_cmd = r'''\draw{} ({}) -- ({}){};
\draw{} ({}) -- ({});
\draw{} ({}) -- ({}) {};'''\
    .format(tikz_options_list('draw', self),
            self.endpoints[0].name, self.endpoints[1].name,
            self.tikz_label(),
            tikz_options_list([self.thickness, self.fillcolor]),
            self.endpoints[0].name, self.fillpoint.name,
            tikz_options_list([self.thickness, 'opacity=0']),
            self.endpoints[0].name, self.endpoints[1].name,
            self.tikz_graduations())
        output.append(draw_cmd)
        return output
