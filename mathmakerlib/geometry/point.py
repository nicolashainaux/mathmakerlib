# -*- coding: utf-8 -*-

# Mathmaker Lib offers lualatex-printable mathematical objects.
# Copyright 2006-2017 Nicolas Hainaux <nh.techn@gmail.com>

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

from mathmakerlib.core.drawable import Drawable
from mathmakerlib.calculus.number import Number


class Point(Drawable):

    def __init__(self, p=None, x=None, y=None, shape=r'$\times$',
                 label_position='below'):
        """
        Initialize Point

        :param p: either the Point's label (e.g. 'A') or another Point to copy
        :type p: str
        :param x: the Point's abscissa
        :type x: anything that can be turned to a Number
        :param y: the Point's ordinate
        :type y: anything that can be turned to a Number
        """
        if isinstance(p, Point):
            Point.__init__(self, p=p.label, x=p.x, y=p.y, shape=p.shape,
                           label_position=p.label_position)
        else:
            self._label = None
            self._x = None
            self._y = None
            self._shape = None
            self._label_position = None
            self.label = p
            self.x = x
            self.y = y
            self.shape = shape
            self.label_position = label_position

    def __repr__(self):
        return 'Point {}({}; {})'.format(self.label, self.x, self.y)

    def __eq__(self, other):
        return all([self.x == other.x, self.y == other.y,
                    self.label == other.label])

    def __ne__(self, other):
        return any([self.x != other.x, self.y != other.y,
                    self.label != other.label])

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, other):
        self._x = Number(other)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, other):
        self._y = Number(other)

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, other):
        self._shape = str(other)

    @property
    def label_position(self):
        return self._label_position

    @label_position.setter
    def label_position(self, other):
        if other is None:
            self._label_position = None
        else:
            self._label_position = str(other)

    def tikz_definition(self, **kwargs):
        """Return the Point definition."""
        return r'\coordinate ({}) at ({},{});'\
            .format(self.label, self.x, self.y)

    def tikz_draw(self, **kwargs):
        """Return the command to actually draw the Point."""
        return r'\draw ({}) node {};'\
            .format(self.label, '{' + self.shape + '}')

    def tikz_label(self, label_position=None, **kwargs):
        """Return the command to write the Point's label."""
        if label_position is None:
            if self.label_position is None:
                label_position = ''
            else:
                label_position = '[' + self.label_position + ']'
        else:
            label_position = '[' + label_position + ']'
        return r'\draw ({}) node{} {};'\
            .format(self.label, label_position, '{' + self.label + '}')
