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
from copy import deepcopy

from mathmakerlib.geometry.point import Point
from mathmakerlib.calculus.number import Number
from mathmakerlib.calculus.tools import is_number, is_integer


class PointsPair(object):
    """
    A pair of Points. Gather methods common to LineSegment, Line, Vector.

    This class won't ever need to get Drawable, but can be instanciated.
    """

    def __init__(self, point1, point2):
        if not isinstance(point1, Point):
            raise TypeError('Both arguments should be Points, got a {} '
                            'as first argument instead.'
                            .format(type(point1)))
        if not isinstance(point2, Point):
            raise TypeError('Both arguments should be Points, got a {} '
                            'as second argument instead.'
                            .format(type(point2)))
        if point1.coordinates == point2.coordinates:
            raise ValueError('Cannot instantiate any PointsPair if both '
                             'endpoints have the same coordinates: '
                             '({}; {}).'.format(point1.x, point1.y))
        self._points = [deepcopy(point1), deepcopy(point2)]
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

    @property
    def slope(self):
        """Slope of the pair of Points, from -180° to 180°."""
        theta = Number(
            str(math.degrees(math.acos(self.deltax / self.length))))\
            .rounded(Number('0.001'))
        return theta if self.deltay >= 0 else -theta

    @property
    def slope360(self):
        """Slope of the pair of Points, from 0° to 360°."""
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
