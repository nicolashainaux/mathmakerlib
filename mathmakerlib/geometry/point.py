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
                 label='default', label_position='below'):
        """
        Initialize Point

        :param p: either the Point's name (e.g. 'A') or another Point to copy
        :type p: str
        :param x: the Point's abscissa
        :type x: anything that can be turned to a Number
        :param y: the Point's ordinate
        :type y: anything that can be turned to a Number
        :param shape: the symbol that will be drawn at the Point's position.
        Default value is '$\times$', what draws a cross.
        :type shape: str
        :param label: what will be placed near the Point. The default value
        will set the Point's name as label. It may be practical to set label
        at None (or '') to draw no label at all.
        :type label: None or str
        :param label_position: if any label is to be drawn, this is where to
        draw it. Available values are TikZ's ones ('above', 'below left'...).
        :type label_position: str
        """
        if isinstance(p, Point):
            Point.__init__(self, p=p.name, x=p.x, y=p.y, shape=p.shape,
                           label=p.label, label_position=p.label_position)
        else:
            self._name = None
            self._x = None
            self._y = None
            self._shape = None
            self._label = None
            self._label_position = None
            self.name = p
            self.x = x
            self.y = y
            self.shape = shape
            if label == 'default':
                self.label = self.name
            else:
                self.label = label
            self.label_position = label_position

    def __repr__(self):
        return 'Point {}({}; {})'.format(self.name, self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return all([self.x == other.x, self.y == other.y,
                        self.name == other.name])
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, Point):
            return any([self.x != other.x, self.y != other.y,
                        self.name != other.name])
        else:
            return True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, other):
        self._name = str(other)

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

    def tikz_definition(self):
        """Return the Point definition."""
        return r'\coordinate ({}) at ({},{});'\
            .format(self.name, self.x, self.y)

    def tikz_draw(self):
        """Return the command to actually draw the Point."""
        return r'\draw ({}) node {};'\
            .format(self.name, '{' + self.shape + '}')

    def tikz_label(self):
        """Return the command to write the Point's label."""
        if self.label is None:
            return ''
        else:
            if self.label_position is None:
                label_position = ''
            else:
                label_position = '[' + self.label_position + ']'
            return r'\draw ({}) node{} {};'\
                .format(self.label, label_position, '{' + self.label + '}')
