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

import math

from mathmakerlib.exceptions import ZERO_OBJECTS_ERRORS
from mathmakerlib.geometry.point import Point
from mathmakerlib.calculus.number import Number
from mathmakerlib.calculus.tools import is_number, is_integer


class Bipoint(object):
    """
    A pair of Points. Gather methods common to LineSegment, Line, Vector.

    This is quite close but not exactly the same as a euclidean vector.

    This class won't ever need to get Drawable, but can be instanciated.
    """

    def __init__(self, tail, head, allow_zero_length=True):
        if not isinstance(tail, Point):
            raise TypeError('Both arguments should be Points, got a {} '
                            'as first argument instead.'
                            .format(type(tail)))
        if not isinstance(head, Point):
            raise TypeError('Both arguments should be Points, got a {} '
                            'as second argument instead.'
                            .format(type(head)))
        if (not allow_zero_length
            and tail.coordinates == head.coordinates):
            msg = 'Explicitly disallowed creation of a zero-length {}.'\
                .format(type(self).__name__)
            raise ZERO_OBJECTS_ERRORS[type(self).__name__](msg)
        self._points = [tail, head]
        self._x = self.points[1].x - self.points[0].x
        self._y = self.points[1].y - self.points[0].y
        self._z = self.points[1].z - self.points[0].z

    def __repr__(self):
        return 'Bipoint({}; {})'.format(repr(self.tail), repr(self.head))

    def __eq__(self, other):
        if isinstance(other, Bipoint):
            return self.head == other.head and self.tail == other.tail
        else:
            return False

    def __add__(self, other):
        return self.add(other)

    def add(self, other, new_endpoint_name='automatic'):
        if not isinstance(other, Bipoint):
            raise TypeError('Can only add a Bipoint to another Bipoint. '
                            'Found {} instead.'.format(repr(other)))
        return Bipoint(self.points[0],
                       Point(self.points[1].x + other.x,
                             self.points[1].y + other.y,
                             self.points[1].z + other.z,
                             name=new_endpoint_name))

    def cross_product(self, other, new_endpoint_name='automatic'):
        if not isinstance(other, Bipoint):
            raise TypeError('Can only calculate the cross product of a '
                            'Bipoint by another Bipoint. Found {} instead.'
                            .format(repr(other)))
        return Bipoint(self.points[0],
                       Point(self.points[0].x
                             + self.y * other.z - self.z * other.y,
                             self.points[0].y
                             + self.z * other.x - self.x * other.z,
                             self.points[0].z
                             + self.x * other.y - self.y * other.x,
                             name=new_endpoint_name))

    @property
    def points(self):
        return self._points

    @property
    def tail(self):
        return self.points[0]

    @property
    def head(self):
        return self.points[1]

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
        """Length between the two Points."""
        return Number(self.x ** 2 + self.y ** 2 + self.z ** 2)\
            .sqrt()

    def normalized(self, new_endpoint_name='automatic'):
        """Return the unit Bipoint colinear (to self)."""
        return Bipoint(self.points[0],
                       Point(self.points[0].x + self.x / self.length,
                             self.points[0].y + self.y / self.length,
                             self.points[0].z + self.z / self.length,
                             name=new_endpoint_name))

    def midpoint(self, name='automatic'):
        """Bipoint's midpoint."""
        return Point((self.points[0].x + self.points[1].x) / 2,
                     (self.points[0].y + self.points[1].y) / 2,
                     (self.points[0].z + self.points[1].z) / 2,
                     name=name)

    def point_at(self, position, name='automatic'):
        """
        A Point aligned with the Bipoint, at provided position.

        The Bipoint's length is the length unit of position.
        Hence, position 0 matches points[0], position 1 matches points[1],
        position 0.5 matches the midpoint, position 0.75 is three quarters
        on the way from points[0] to points[1], position 2 is a Point that
        makes points[1] the middle between it and points[0], position -1 makes
        points[0] the middle between it and points[1].

        :param position: a number
        :type position: number
        :param name: the name to give to the Point
        :type name: str
        """
        if not is_number(position):
            raise TypeError('position must be a number, found {} instead.'
                            .format(type(position)))
        k = Number(position)
        if k == 0:
            return self.points[0]
        elif k == 1:
            return self.points[1]
        else:
            return Point((self.points[0].x
                          + (self.points[1].x - self.points[0].x) * k),
                         (self.points[0].y
                          + (self.points[1].y - self.points[0].y) * k),
                         (self.points[0].z
                          + (self.points[1].z - self.points[0].z) * k),
                         name=name)

    @property
    def slope(self):
        """Slope of the pair of Points, from -180° to 180°."""
        if self.length == 0:
            msg = 'Cannot calculate the slope of a zero-length {}.'\
                .format(type(self).__name__)
            raise ZERO_OBJECTS_ERRORS[type(self).__name__](msg)
        theta = Number(
            str(math.degrees(math.acos(self.x / self.length))))\
            .rounded(Number('0.001'))
        return theta if self.y >= 0 else -theta

    @property
    def slope360(self):
        """Slope of the pair of Points, from 0° to 360°."""
        if self.length == 0:
            msg = 'Cannot calculate the slope of a zero-length {}.'\
                .format(type(self).__name__)
            raise ZERO_OBJECTS_ERRORS[type(self).__name__](msg)
        theta = Number(
            str(math.degrees(math.acos(self.x / self.length))))\
            .rounded(Number('0.001'))
        return theta if self.y >= 0 else Number('360') - theta

    def dividing_points(self, n=None, prefix='a'):
        """
        Create the list of Points that divide the Bipoint in n parts.

        :param n: the number of parts (so it will create n - 1 points)
        n must be greater or equal to 1
        :type n: int
        """
        if not (is_number(n) and is_integer(n)):
            raise TypeError('n must be an integer')
        if not n >= 1:
            raise ValueError('n must be greater or equal to 1')
        x0 = self.points[0].x
        x1 = self.points[1].x
        xstep = (x1 - x0) / n
        x_list = [x0 + (i + 1) * xstep for i in range(int(n - 1))]
        y0 = self.points[0].y
        y1 = self.points[1].y
        ystep = (y1 - y0) / n
        y_list = [y0 + (i + 1) * ystep for i in range(int(n - 1))]
        z0 = self.points[0].z
        z1 = self.points[1].z
        zstep = (z1 - z0) / n
        z_list = [z0 + (i + 1) * zstep for i in range(int(n - 1))]
        return [Point(x, y, z, prefix + str(i + 1))
                for i, (x, y, z) in enumerate(zip(x_list, y_list, z_list))]

    def bisector(self, other, new_endpoint_name='automatic'):
        """
        Return a bipoint colinear to the bisector of self and another bipoint.

        :param arg: the other Bipoint
        :type arg: Bipoint
        """
        if not isinstance(other, Bipoint):
            raise TypeError('Can only create the bisector with another '
                            'Bipoint. Found {} instead.'
                            .format(repr(other)))
        return self.normalized(new_endpoint_name=new_endpoint_name)\
            .add(other.normalized(new_endpoint_name=new_endpoint_name),
                 new_endpoint_name=new_endpoint_name)
