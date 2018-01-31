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

from mathmakerlib.geometry.point import Point
from mathmakerlib.geometry.pointspair import PointsPair


class Vector(PointsPair):
    """Vectors. Not Drawable yet. Not publicly available yet."""

    def __add__(self, other):
        return self.add(other)

    def add(self, other, new_endpoint_name='automatic'):
        if not isinstance(other, Vector):
            raise TypeError('Can only add a Vector to another Vector. '
                            'Got {} instead.'.format(type(other)))
        return Vector(self.points[0], Point(self.points[1].x + other.deltax,
                                            self.points[1].y + other.deltay,
                                            name=new_endpoint_name))

    def unit_vector(self, new_endpoint_name='automatic'):
        """Return the unit vector colinear (to self)."""
        return Vector(self.points[0],
                      Point(self.points[0].x + self.deltax / self.length,
                            self.points[0].y + self.deltay / self.length,
                            name=new_endpoint_name))

    def bisector_vector(self, other, new_endpoint_name='automatic'):
        """
        Return a vector colinear to the bisector of self and another vector.

        :param arg: the other vector
        :type arg: Vector
        """
        if not isinstance(other, Vector):
            raise TypeError('Can only create the bisector with another Vector.'
                            ' Got a {} instead.'.format(type(other)))
        return self.unit_vector(new_endpoint_name=new_endpoint_name)\
            .add(other.unit_vector(new_endpoint_name=new_endpoint_name),
                 new_endpoint_name=new_endpoint_name)
