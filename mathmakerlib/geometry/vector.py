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

import math

from mathmakerlib.exceptions import ZERO_OBJECTS_ERRORS
from mathmakerlib.geometry.point import Point
from mathmakerlib.calculus.number import Number
from mathmakerlib.core.dimensional import Dimensional
from mathmakerlib.calculus.tools import is_number


class Vector(Dimensional):
    """
    A euclidean (free) vector.

    Differences with Bipoints are discussed in Bipoint docstring.

    This class won't ever need to get Drawable, but can be instanciated.
    """

    def __init__(self, *args, allow_zero_length=True):
        """
        It's possible to create a Vector giving:
        - a Bipoint: Bipoint(A, B)
        - a pair of Points: A, B
        - its coordinates x, y or x, y, z
        """
        if not args or len(args) >= 4:
            raise TypeError('Vector() takes one, two or three arguments '
                            '({} given)'.format(len(args)))
        if len(args) == 1:
            from mathmakerlib.geometry.bipoint import Bipoint
            if not isinstance(args[0], Bipoint):
                raise TypeError('a Vector can be created from one Bipoint, '
                                'found {} instead.'.format(repr(args[0])))
            self._x = args[0].Δx
            self._y = args[0].Δy
            if args[0].three_dimensional:
                self._z = args[0].Δz
                self._three_dimensional = True
            else:
                self._z = Number(0)
                self._three_dimensional = False
        elif len(args) == 2:
            # Two Points
            if isinstance(args[0], Point) and isinstance(args[1], Point):
                self._x = args[1].x - args[0].x
                self._y = args[1].y - args[0].y
                if args[0].three_dimensional or args[1].three_dimensional:
                    self._three_dimensional = True
                    self._z = args[1].z - args[0].z
                else:
                    self._three_dimensional = False
                    self._z = Number(0)
            # Two numbers
            elif is_number(args[0]) and is_number(args[1]):
                self._three_dimensional = False
                self._x = Number(args[0])
                self._y = Number(args[1])
                self._z = Number(0)
            else:
                raise TypeError('a Vector can be created from two arguments, '
                                'either two Points or two numbers. '
                                'Found {} and {} instead.'
                                .format(repr(args[0]), repr(args[1])))
        elif len(args) == 3:
            self._three_dimensional = True
            self._x = Number(args[0])
            self._y = Number(args[1])
            self._z = Number(args[2])
        self._length = Number(self.x ** 2 + self.y ** 2 + self.z ** 2).sqrt()
        if not allow_zero_length and self.length == 0:
            msg = 'Explicitly disallowed creation of a zero-length {}.'\
                .format(type(self).__name__)
            raise ZERO_OBJECTS_ERRORS[type(self).__name__](msg)

    def __repr__(self):
        if self.three_dimensional:
            return 'Vector({}, {}, {})'.format(str(self.x), str(self.y),
                                               str(self.z))
        else:
            return 'Vector({}, {})'.format(str(self.x), str(self.y))

    def __eq__(self, other):
        if isinstance(other, Vector):
            return (self.x == other.x and self.y == other.y
                    and self.z == other.z)
        else:
            return False

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError('Can only add a Vector to another Vector. '
                            'Found {} instead.'.format(repr(other)))
        if self.three_dimensional or other.three_dimensional:
            return Vector(self.x + other.x,
                          self.y + other.y,
                          self.z + other.z)
        else:
            return Vector(self.x + other.x,
                          self.y + other.y)

    def __neg__(self):
        if self.three_dimensional:
            return Vector(-self.x, -self.y, -self.z)
        else:
            return Vector(-self.x, -self.y)

    def dot(self, other):
        if not isinstance(other, Vector):
            raise TypeError('Can only calculate the dot product of a '
                            'Vector by another Vector. Found {} instead.'
                            .format(repr(other)))
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        if not isinstance(other, Vector):
            raise TypeError('Can only calculate the cross product of a '
                            'Vector by another Vector. Found {} instead.'
                            .format(repr(other)))
        return Vector(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def coordinates(self):
        return (self._x, self._y, self._z)

    @property
    def length(self):
        """Vector's norm."""
        return self._length

    def normalized(self):
        """Return the unit Vector colinear (to self)."""
        if self.three_dimensional:
            return Vector(self.x / self.length,
                          self.y / self.length,
                          self.z / self.length)
        else:
            return Vector(self.x / self.length,
                          self.y / self.length)

    def _slope(self, offset=0):
        if self.length == 0:
            msg = 'Cannot calculate the slope of a zero-length {}.'\
                .format(type(self).__name__)
            raise ZERO_OBJECTS_ERRORS[type(self).__name__](msg)
        theta = Number(
            str(math.degrees(math.acos(self.x / self.length))))\
            .rounded(Number('0.001'))
        return theta if self.y >= 0 else Number(offset) - theta

    @property
    def slope(self):
        """Slope between the Vector and X-axis, from -180° to 180°."""
        return self._slope()

    @property
    def slope360(self):
        """Slope between the Vector and X-axis, from 0° to 360°."""
        return self._slope(360)

    def angle_measure(self, other):
        """Angle between the Vector and another Vector."""
        result = other.slope360 - self.slope360
        if result < 0:
            result += 360
        return result

    def bisector(self, other, new_endpoint_name='automatic'):
        """
        Return the bisector vector of self and another vector.

        :param arg: the other Vector
        :type arg: Vector
        """
        if not isinstance(other, Vector):
            raise TypeError('Can only create the bisector with another '
                            'Vector. Found {} instead.'
                            .format(repr(other)))
        result = self.normalized() + other.normalized()
        if self.angle_measure(other) > 180:
            result = -result
        return result
