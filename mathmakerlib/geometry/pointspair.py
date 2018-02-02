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


class PointsPair(object):
    """
    A pair of Points. Gather methods common to LineSegment, Line, Vector.

    This class won't ever need to get Drawable, but can be instanciated.
    """

    def __init__(self, point1, point2, allow_zero_length=True):
        if not isinstance(point1, Point):
            raise TypeError('Both arguments should be Points, got a {} '
                            'as first argument instead.'
                            .format(type(point1)))
        if not isinstance(point2, Point):
            raise TypeError('Both arguments should be Points, got a {} '
                            'as second argument instead.'
                            .format(type(point2)))
        if (not allow_zero_length
            and point1.coordinates == point2.coordinates):
            msg = 'Explicitly disallowed creation of a zero-length {}.'\
                .format(type(self).__name__)
            raise ZERO_OBJECTS_ERRORS[type(self).__name__](msg)
        self._points = [point1, point2]
        self._deltax = self.points[1].x - self.points[0].x
        self._deltay = self.points[1].y - self.points[0].y

    def same_as(self, other):
        """Test geometric equality."""
        return (self.points[0].coordinates[0].rounded(Number('0.001'))
                == other.points[0].coordinates[0].rounded(Number('0.001'))
                and self.points[0].coordinates[1].rounded(Number('0.001'))
                == other.points[0].coordinates[1].rounded(Number('0.001'))
                and self.points[1].coordinates[0].rounded(Number('0.001'))
                == other.points[1].coordinates[0].rounded(Number('0.001'))
                and self.points[1].coordinates[1].rounded(Number('0.001'))
                == other.points[1].coordinates[1].rounded(Number('0.001')))

    @property
    def points(self):
        return self._points

    @property
    def deltax(self):
        return self._deltax

    @property
    def deltay(self):
        return self._deltay

    @property
    def length(self):
        """Length between the two Points."""
        return Number(self.deltax ** 2 + self.deltay ** 2).sqrt()

    def midpoint(self, name='automatic'):
        """PointsPair's midpoint."""
        return Point((self.points[0].x + self.points[1].x) / 2,
                     (self.points[0].y + self.points[1].y) / 2,
                     name=name)

    def point_at(self, position, name='automatic'):
        """
        A Point aligned with the PointsPair, at provided position.

        The PointsPair's length is the length unit of position.
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
                         name=name)

    @property
    def slope(self):
        """Slope of the pair of Points, from -180° to 180°."""
        if self.length == 0:
            msg = 'Cannot calculate the slope of a zero-length {}.'\
                .format(type(self).__name__)
            raise ZERO_OBJECTS_ERRORS[type(self).__name__](msg)
        theta = Number(
            str(math.degrees(math.acos(self.deltax / self.length))))\
            .rounded(Number('0.001'))
        return theta if self.deltay >= 0 else -theta

    @property
    def slope360(self):
        """Slope of the pair of Points, from 0° to 360°."""
        if self.length == 0:
            msg = 'Cannot calculate the slope of a zero-length {}.'\
                .format(type(self).__name__)
            raise ZERO_OBJECTS_ERRORS[type(self).__name__](msg)
        theta = Number(
            str(math.degrees(math.acos(self.deltax / self.length))))\
            .rounded(Number('0.001'))
        return theta if self.deltay >= 0 else Number('360') - theta

    def dividing_points(self, n=None, prefix='a'):
        """
        Create the list of Points that divide the PointsPair in n parts.

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
        return [Point(x, y, prefix + str(i + 1))
                for i, (x, y) in enumerate(zip(x_list, y_list))]
