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

import string
from decimal import InvalidOperation
from math import cos, sin, radians

from mathmakerlib import config
from mathmakerlib.core.drawable import Drawable, check_scale, tikz_options_list
from mathmakerlib.core.dimensional import Dimensional
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


class Point(Drawable, Dimensional):
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

    def __init__(self, x=None, y=None, z='undefined', name='automatic',
                 color=None, shape=r'$\times$', shape_scale=Number('0.67'),
                 label='default', label_position='below'):
        r"""
        Initialize Point

        When not naming the keyword arguments, it is possible to not mention
        the applicate, z:
        Point(3, 2, 'A') is almost equivalent to Point(3, 2, 0, 'A'):
        - all subsequent keyword arguments must be named
        - the first version is a 2D Point, the second version a 3D Point.

        :param x: the Point's abscissa
        :type x: anything that can be turned to a Number
        :param y: the Point's ordinate
        :type y: anything that can be turned to a Number
        :param z: the Point's applicate
        :type z: anything that can be turned to a Number
        :param name: the Point's name (e.g. 'A'). If it's left to 'automatic',
        a yet unused name will be set.
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
        self._three_dimensional = False
        self._name = None
        self._x = None
        self._y = None
        self._z = None
        self._shape = None
        self._label = None
        self._label_position = None
        self.x = x
        self.y = y
        try:
            self.z = z
        except (TypeError, InvalidOperation):
            # The third value cannot be used as z; let's assume it is actually
            # 2D geometry and the value is actually simply the name, implying
            # z should be set to 0.
            self.z = Number(0)
            self._three_dimensional = False
            self.name = z
        else:
            self.name = name
        self.shape = shape
        if label == 'default':
            self.label = self.name
        else:
            self.label = label
        self.label_position = label_position
        if color is not None:
            self.color = color
        self.shape_scale = shape_scale

    def __str__(self):
        if not self.three_dimensional:
            s = '{}({}, {})'.format(self.name, self.x, self.y)
        else:
            s = '{}({}, {}, {})'.format(self.name, self.x, self.y, self.z)
        return s

    def __repr__(self):
        if not self.three_dimensional:
            s = 'Point {}({}, {})'.format(self.name, self.x, self.y)
        else:
            s = 'Point {}({}, {}, {})'.format(self.name,
                                              self.x, self.y, self.z)
        return s

    def __hash__(self):
        if not self.three_dimensional:
            s = 'Point ({}, {})'.format(self.x, self.y)
        else:
            s = 'Point ({}, {}, {})'.format(self.x, self.y, self.z)
        return hash(s)

    def __eq__(self, other):
        if isinstance(other, Point):
            p = config.points.DEFAULT_POSITION_PRECISION
            return all([self.x.rounded(p) == other.x.rounded(p),
                        self.y.rounded(p) == other.y.rounded(p),
                        self.z.rounded(p) == other.z.rounded(p)])
        else:
            return False

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
    def x(self, value):
        try:
            self._x = Number(value)
        except (TypeError, InvalidOperation):
            raise TypeError('Expected a number as abscissa, found {} '
                            'instead.'.format(repr(value)))

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        try:
            self._y = Number(value)
        except (TypeError, InvalidOperation):
            raise TypeError('Expected a number as ordinate, found {} '
                            'instead.'.format(repr(value)))

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        three_dimensional = True
        if value == 'undefined':
            value = 0
            three_dimensional = False
        try:
            self._z = Number(value)
        except (TypeError, InvalidOperation):
            raise TypeError('Expected a number as applicate, found {} '
                            'instead.'.format(repr(value)))
        self._three_dimensional = three_dimensional

    @property
    def coordinates(self):
        return (self._x, self._y, self._z)

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

    def rotate(self, center, angle, axis=None, rename='auto'):
        """
        Rotate around center (or axis going through center).

        :param center: the center of the rotation
        :type center: Point
        :param angle: the angle of the rotation
        :type angle: a number
        :param axis: the axis of the rotation for 3D rotation. If left to None,
        the rotation happens around the center, in the plane.
        :type axis: Vector
        :param rename: if set to 'auto', will name the rotated Point after the
        original, adding a ' (like A.rotate(...) creates a Point A'). If set
        to None, keep the original name. Otherwise, the provided str will be
        used as the rotated Point's name.
        :type rename: None or str
        :rtype: Point
        """
        from mathmakerlib.geometry.vector import Vector
        if not isinstance(center, Point):
            raise TypeError('Expected a Point as rotation center, got {} '
                            'instead.'.format(type(center)))
        if not is_number(angle):
            raise TypeError('Expected a number as rotation angle, got {} '
                            'instead.'.format(type(angle)))
        if not (axis is None or isinstance(axis, Vector)):
            raise TypeError('Expected either None or a Vector as axis, '
                            'found {} instead.'.format(repr(axis)))
        Δx = self.x - center.x
        Δy = self.y - center.y
        Δz = self.z - center.z
        cosθ = Number(str(cos(radians(angle))))
        sinθ = Number(str(sin(radians(angle))))
        if axis is None:
            rx = (Δx * cosθ - Δy * sinθ + center.x).rounded(Number('1.000'))
            ry = (Δx * sinθ + Δy * cosθ + center.y).rounded(Number('1.000'))
            rz = 'undefined'
        else:
            ux, uy, uz = axis.normalized().coordinates
            rotation_matrix = [[cosθ + (1 - cosθ) * ux ** 2,
                                ux * uy * (1 - cosθ) - uz * sinθ,
                                ux * uz * (1 - cosθ) + uy * sinθ],
                               [uy * ux * (1 - cosθ) + uz * sinθ,
                                cosθ + (1 - cosθ) * uy ** 2,
                                uy * uz * (1 - cosθ) - ux * sinθ],
                               [uz * ux * (1 - cosθ) - uy * sinθ,
                                uz * uy * (1 - cosθ) + ux * sinθ,
                                cosθ + (1 - cosθ) * uz ** 2]]
            rx = sum([rc * coord
                      for rc, coord in zip(rotation_matrix[0], [Δx, Δy, Δz])])
            ry = sum([rc * coord
                      for rc, coord in zip(rotation_matrix[1], [Δx, Δy, Δz])])
            rz = sum([rc * coord
                      for rc, coord in zip(rotation_matrix[2], [Δx, Δy, Δz])])
            rx += center.x
            ry += center.y
            rz += center.z
            rx = rx.rounded(Number('1.000'))
            ry = ry.rounded(Number('1.000'))
            rz = rz.rounded(Number('1.000'))

        if rename == 'keep_name':
            rname = self.name
        elif rename == 'auto':
            rname = self.name + "'"
        else:
            rname = rename
        return Point(rx, ry, rz, rname)

    def belongs_to(self, other):
        """Check if the Point belongs to a LineSegment."""
        # This could be extended to Lines and Rays, later.
        # Then check if self is different from the 2 known Points, and
        # if it belongs to the Line, then:
        # (x - x1) / (x2 - x1) = (y - y1) / (y2 - y1)
        # also, if three_dimensional, all this = (z - z1) / (z2 - z1)
        from mathmakerlib.geometry import LineSegment
        if not isinstance(other, LineSegment):
            raise TypeError('Argument \'other\' must be a LineSegment. '
                            'Found {} instead.'.format(repr(other)))
        d1 = LineSegment(self, other.endpoints[0]).length
        d2 = LineSegment(self, other.endpoints[1]).length
        return d1 + d2 == other.length

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
