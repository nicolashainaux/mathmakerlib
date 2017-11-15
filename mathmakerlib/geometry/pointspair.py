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
from abc import ABCMeta

from mathmakerlib.core.drawable import Drawable
from mathmakerlib.geometry.point import Point
from mathmakerlib.calculus.number import Number
from mathmakerlib.calculus.tools import is_number, is_integer


class PointsPair(Drawable, metaclass=ABCMeta):

    def __init__(self):
        self._deltax = self.points[1].x - self.points[0].x
        self._deltay = self.points[1].y - self.points[0].y

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
        """Slope of the pair of Points."""
        theta = Number(str(math.degrees(math.acos(self.deltax / self.length))))
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
