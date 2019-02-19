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

from mathmakerlib import config
from mathmakerlib.calculus.number import Number
from mathmakerlib.geometry.point import Point
from mathmakerlib.geometry.angle import AngleDecoration
from . import Triangle


class RightTriangle(Triangle):
    """Right Triangles."""

    def __init__(self, start_vertex=None, name=None,
                 leg1_length=Number(2), leg2_length=Number(1),
                 mark_right_angle=True,
                 draw_vertices=False, label_vertices=True,
                 thickness='thick', color=None, rotation_angle=0,
                 winding=None, sloped_sides_labels=True):
        r"""
        Initialize Right Triangle

        :param start_vertex: the vertex to start to draw the Right Triangle
        (default (0; 0))
        :type start_vertex: Point
        :param name: the name of the Triangle, like ABC.
        Can be either None (the names will be automatically created), or a
        string of the letters to use to name the vertices. Only single letters
        are supported as Points' names so far (at Polygon's creation).
        See issue #3.
        :type name: None or str
        :param leg1_length: the leg1's length that will be used to calculate
        the coordinates of the vertices used to build the RightTriangle
        :type leg1_length: a number
        :param leg2_length: the leg2's length that will be used to calculate
        the coordinates of the vertices used to build the RightTriangle
        :type leg2_length: a number
        :param mark_right_angle: if True (default), the right angle will be
        automatically marked as right angle.
        :type mark_right_angle: bool
        :param draw_vertices: whether to actually draw, or not, the vertices
        :type draw_vertices: bool
        :param label_vertices: whether to label, or not, the vertices
        :type label_vertices: bool
        :param thickness: the thickness of the Triangle's sides
        :type thickness: str
        :param color: the color of the Triangle's sides
        :type color: str
        :param rotate: the angle of rotation around isobarycenter
        :type rotate: int
        """
        if start_vertex is None:
            start_vertex = Point(0, 0)
        # Accepted type for leg1's and leg2's lengths is number, will be
        # checked at vertices' instanciations.
        v1 = Point(leg1_length + start_vertex.x, start_vertex.y)
        v2 = Point(leg1_length + start_vertex.x, leg2_length + start_vertex.y)
        if (winding == 'clockwise'
            or (winding is None
                and config.polygons.DEFAULT_WINDING == 'clockwise')):
            start_vertex, v2 = v2, start_vertex
        Triangle.__init__(self, start_vertex, v1, v2, name=name,
                          draw_vertices=draw_vertices,
                          label_vertices=label_vertices,
                          thickness=thickness, color=color,
                          rotation_angle=rotation_angle,
                          winding=winding,
                          sloped_sides_labels=sloped_sides_labels)
        self._type = 'RightTriangle'
        if mark_right_angle:
            self.right_angle.decoration = AngleDecoration(thickness=thickness)
            self.right_angle.mark_right = True

    @property
    def hypotenuse(self):
        return self._sides[2]

    @property
    def right_angle(self):
        return self.angles[1]
