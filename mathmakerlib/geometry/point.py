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

import string
import decimal
from math import cos, sin, radians

from mathmakerlib.core.drawable import Drawable, check_scale, tikz_options_list
from mathmakerlib.calculus.number import Number
from mathmakerlib.calculus.tools import is_number

OPPOSITE_LABEL_POSITIONS = {'right': 'left',
                            'above right': 'below left',
                            'above': 'below',
                            'above left': 'below right',
                            'left': 'right',
                            'below left': 'above right',
                            'below': 'above',
                            'below right': 'above left'}


class Point(Drawable):
    names_in_use = set()

    @classmethod
    def automatic_names(cls):
        use = Point.names_in_use
        names = [letter
                 for letter in string.ascii_uppercase
                 if letter not in use][::-1]
        if not names:
            layer = 1
            while not names:
                names = ['{}$_{}$'.format(letter, layer)
                         for letter in string.ascii_uppercase
                         if '{}$_{}$'.format(letter, layer)
                         not in use][::-1]
                layer += 1
        return names

    @classmethod
    def reset_names(cls):
        cls.names_in_use = set()

    def __init__(self, x=None, y=None, name='automatic', shape=r'$\times$',
                 label='default', label_position='below', color=None,
                 shape_scale=Number('0.67')):
        r"""
        Initialize Point
        :param x: the Point's abscissa
        :type x: anything that can be turned to a Number
        :param y: the Point's ordinate
        :type y: anything that can be turned to a Number
        :param name: the Point's name (e.g. 'A'). If it's left to None, a yet
        unused name will be set.
        :type name: str
        :param shape: the symbol that will be drawn at the Point's position.
        Default value is '$\times$', what draws a cross.
        :type shape: str
        :param label: what will be placed near the Point. The default value
        will set the Point's name as label. Setting label at '' will disable
        labeling the Point.
        :type label: str
        :param label_position: if any label is to be drawn, this is where to
        draw it. Available values are TikZ's ones ('above', 'below left'...).
        :type label_position: str
        """
        self._name = None
        self._x = None
        self._y = None
        self._shape = None
        self._label = None
        self._label_position = None
        self.name = name
        self.x = x
        self.y = y
        self.shape = shape
        if label is 'default':
            self.label = self.name
        else:
            self.label = label
        self.label_position = label_position
        if color is not None:
            self.color = color
        self.shape_scale = shape_scale

    def __str__(self):
        return '{}({}; {})'.format(self.name, self.x, self.y)

    def __repr__(self):
        return 'Point {}({}; {})'.format(self.name, self.x, self.y)

    # def __hash__(self):
    #     return hash(repr(self))

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

    def same_as(self, other):
        """Test geometric equality."""
        if not isinstance(other, Point):
            raise TypeError('Can only test if another Point is at the same '
                            'place. Got a {} instead.'.format(type(other)))
        return self.coordinates == other.coordinates

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if self._name is not None:
            Point.names_in_use.discard(self._name)
        if value is None:
            self._name = None
        else:
            value = str(value)
            if value == 'automatic':
                self._name = Point.automatic_names().pop()
            else:
                self._name = value
            Point.names_in_use.add(self._name)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, other):
        try:
            self._x = Number(other)
        except (TypeError, decimal.InvalidOperation) as excinfo:
            raise TypeError('Expected a number as abscissa, got \'{}\' '
                            'instead.'.format(other))

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, other):
        try:
            self._y = Number(other)
        except (TypeError, decimal.InvalidOperation) as excinfo:
            raise TypeError('Expected a number as ordinate, got \'{}\' '
                            'instead.'.format(other))

    @property
    def coordinates(self):
        return (self._x, self._y)

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, other):
        self._shape = str(other)

    @property
    def shape_scale(self):
        return self._shape_scale

    @shape_scale.setter
    def shape_scale(self, value):
        check_scale(value, 'Point\'s shape')
        self._shape_scale = Number(value)

    @property
    def label_position(self):
        return self._label_position

    @label_position.setter
    def label_position(self, other):
        if other is None:
            self._label_position = None
        else:
            self._label_position = str(other)

    def rotate(self, center, angle, rename='auto'):
        """
        Return a Point rotated around center of the provided angle.

        :param center: the center of the rotation
        :type center: Point
        :param angle: the angle of the rotation
        :type angle: a number
        :param rename: if set to 'auto', will name the rotated Point after the
        original, adding a ' (like A.rotate(...) creates a Point A'). If set
        to None, keep the original name. Otherwise, the provided str will be
        used as the rotated Point's name.
        :type rename: None or str
        :rtype: Point
        """
        if not isinstance(center, Point):
            raise TypeError('Expected a Point as rotation center, got {} '
                            'instead.'.format(type(center)))
        if not is_number(angle):
            raise TypeError('Expected a number as rotation angle, got {} '
                            'instead.'.format(type(angle)))
        deltax = self.x - center.x
        deltay = self.y - center.y
        rx = (deltax * Number(str(cos(radians(angle))))
              - deltay * Number(str(sin(radians(angle))))
              + center.x).rounded(Number('1.000'))
        ry = (deltax * Number(str(sin(radians(angle))))
              + deltay * Number(str(cos(radians(angle))))
              + center.y).rounded(Number('1.000'))
        if rename == 'keep_name':
            rname = self.name
        elif rename == 'auto':
            rname = self.name + "'"
        else:
            rname = rename
        return Point(rx, ry, rname)

    def tikz_declaring_comment(self):
        """
        Replace plural by singular in the declaring comment.

        :rtype: str
        """
        return '% Declare Point'

    def tikz_declarations(self):
        """Return the Point declaration."""
        if self.name is None:
            raise RuntimeError('Point at ({}, {}) has no name (None), '
                               'cannot create TikZ picture using it.')
        return r'\coordinate ({}) at ({},{});'\
            .format(self.name,
                    self.x.rounded(Number('0.001')),
                    self.y.rounded(Number('0.001')))

    def tikz_drawing_comment(self):
        """Return the comment preceding the Point's drawing."""
        return ['% Draw Point']

    def _tikz_draw_options(self):
        return [self.color]

    def tikz_draw(self):
        """Return the command to actually draw the Point."""
        sh_scale = ''
        if self.shape_scale != 1:
            sh_scale = '[scale={}]'.format(self.shape_scale)
        return [r'\draw{} ({}) node{} {};'
                .format(tikz_options_list('draw', self),
                        self.name,
                        sh_scale,
                        '{' + self.shape + '}')]

    def tikz_labeling_comment(self):
        """
        Replace plural by singular in the labeling comment.

        :rtype: str
        """
        return '% Label Point'

    def tikz_points_labels(self):
        return self.tikz_label()

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
