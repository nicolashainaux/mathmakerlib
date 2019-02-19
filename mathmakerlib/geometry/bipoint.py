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

from mathmakerlib.exceptions import ZERO_OBJECTS_ERRORS, ZeroVector
from mathmakerlib.geometry.point import Point
from mathmakerlib.geometry.vector import Vector
from mathmakerlib.calculus.number import Number
from mathmakerlib.core.dimensional import Dimensional
from mathmakerlib.calculus.tools import is_number, is_integer


class Bipoint(Dimensional):
    """
    A pair of Points. Gather methods common to LineSegment, Line, Ray.

    Bipoints are quite close to, but not completely the same as, bound vectors.
    For free vectors, see Vector.

    Notice that if:
    A = Point(0, 0); B = Point(1, 0); C = Point(0, 1) and D = Point(1, 1),
    then: Bipoint(A, B) != Bipoint(C, D)
    but: Vector(A, B) == Vector(C, D)

    Also, note that contrary to LineSegments, Bipoint(A, B) != Bipoint(B, A).

    This class won't ever need to get Drawable, but can be instanciated.
    """

    def __init__(self, tail, head, allow_zero_length=True):
        """
        A Bipoint can be created from a pair of Points or a Point + a Vector.

        :param tail: the first Point of the Bipoint
        :type tail: Point
        :param head: the second Point of the Bipoint. If a Vector is provided,
        the second Point will be calculated using the first Point and this
        Vector.
        :type head: Point or Vector
        :param allow_zero_length: whether zero length Bipoints are allowed or
        not (default True).
        :type allow_zero_length: bool
        """
        if not isinstance(tail, Point):
            raise TypeError('First argument must be a Point, found {} '
                            'instead.'.format(repr(tail)))
        if not isinstance(head, (Point, Vector)):
            raise TypeError('Second argument must be a Point or a Vector, '
                            'found {} instead.'.format(repr(head)))
        self._three_dimensional = tail.three_dimensional \
            or head.three_dimensional
        if isinstance(head, Vector):
            if self._three_dimensional:
                zval = tail.z + head.z
            else:
                zval = 'undefined'
            head = Point(tail.x + head.x, tail.y + head.y, zval)
        if (not allow_zero_length
            and tail.coordinates == head.coordinates):
            msg = 'Explicitly disallowed creation of a zero-length {}.'\
                .format(type(self).__name__)
            raise ZERO_OBJECTS_ERRORS[type(self).__name__](msg)
        self._points = [tail, head]
        self._Δx = self.points[1].x - self.points[0].x
        self._Δy = self.points[1].y - self.points[0].y
        self._Δz = self.points[1].z - self.points[0].z

    def __repr__(self):
        return 'Bipoint({}, {})'.format(repr(self.tail), repr(self.head))

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
        if self.three_dimensional:
            zval = self.points[1].z + other.Δz
        else:
            zval = 'undefined'
        return Bipoint(self.points[0],
                       Point(self.points[1].x + other.Δx,
                             self.points[1].y + other.Δy,
                             z=zval,
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
    def Δx(self):
        return self._Δx

    @property
    def Δy(self):
        return self._Δy

    @property
    def Δz(self):
        return self._Δz

    @property
    def coordinates(self):
        return (self._Δx, self._Δy, self._Δz)

    @property
    def length(self):
        """Length between the two Points."""
        return Number(self.Δx ** 2 + self.Δy ** 2 + self.Δz ** 2)\
            .sqrt()

    @property
    def slope(self):
        """Slope of the pair of Points, from -180° to 180°."""
        try:
            return Vector(self).slope
        except ZeroVector:
            msg = 'Cannot calculate the slope of a zero-length {}.'\
                .format(type(self).__name__)
            raise ZERO_OBJECTS_ERRORS[type(self).__name__](msg)

    @property
    def slope360(self):
        """Slope of the pair of Points, from 0° to 360°."""
        try:
            return Vector(self).slope360
        except ZeroVector:
            msg = 'Cannot calculate the slope of a zero-length {}.'\
                .format(type(self).__name__)
            raise ZERO_OBJECTS_ERRORS[type(self).__name__](msg)

    def midpoint(self, name='automatic'):
        """Bipoint's midpoint."""
        if self.three_dimensional:
            zval = (self.points[0].z + self.points[1].z) / 2
        else:
            zval = 'undefined'
        return Point((self.points[0].x + self.points[1].x) / 2,
                     (self.points[0].y + self.points[1].y) / 2,
                     z=zval,
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
            if self.three_dimensional:
                zval = (self.points[0].z
                        + (self.points[1].z - self.points[0].z) * k)
            else:
                zval = 'undefined'
            return Point((self.points[0].x
                          + (self.points[1].x - self.points[0].x) * k),
                         (self.points[0].y
                          + (self.points[1].y - self.points[0].y) * k),
                         z=zval,
                         name=name)

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
        if self.three_dimensional:
            z0 = self.points[0].z
            z1 = self.points[1].z
            zstep = (z1 - z0) / n
            z_list = [z0 + (i + 1) * zstep for i in range(int(n - 1))]
        else:
            z_list = ['undefined' for i in range(int(n - 1))]
        return [Point(x, y, z, prefix + str(i + 1))
                for i, (x, y, z) in enumerate(zip(x_list, y_list, z_list))]
