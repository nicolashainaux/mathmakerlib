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
from mathmakerlib.calculus.number import Number


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

    # The automatic naming of the midpoint is a problem.
    # It will require to add a mean to generate new points names automatically.
    # With same convention as in geogebra for instance: A, B, C... A_1, B_1,...
    # @property
    # def midpoint(self):
    #     """PointsPair's midpoint."""
    #     return Point('M',
    #                  (self.points[0].x + self.points[1].x) / 2,
    #                  (self.points[0].y + self.points[1].y) / 2)

    @property
    def slope(self):
        """Slope of the pair of Points."""
        theta = Number(str(math.degrees(math.acos(self.deltax / self.length))))
        return theta if self.deltay >= 0 else Number('360') - theta
