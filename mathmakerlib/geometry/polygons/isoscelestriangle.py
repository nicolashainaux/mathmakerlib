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

from mathmakerlib.calculus.number import Number
from mathmakerlib.geometry.point import Point
from . import Triangle


class IsoscelesTriangle(Triangle):
    """Isosceles Triangles."""

    def __init__(self, start_vertex=None, name=None,
                 base_length=Number('1.5'),
                 equal_legs_length=Number('1'),
                 mark_equal_sides=True,
                 draw_vertices=False, label_vertices=True,
                 thickness='thick', color=None, rotation_angle=0):
        r"""
        Initialize Isosceles Triangle

        :param start_vertex: the vertex to start to draw the Right Triangle
        (default (0; 0))
        :type start_vertex: Point
        :param name: the name of the Triangle, like ABC.
        Can be either None (the names will be automatically created), or a
        string of the letters to use to name the vertices. Only single letters
        are supported as Points' names so far (at Polygon's creation).
        See issue #3.
        :type name: None or str
        :param base_length: the length of the base of the IsoscelesTriangle,
        that will be used to calculate the coordinates of its vertices
        :type base_length: a number
        :param equal_legs_length: the length of the equal legs of the
        IsoscelesTriangle, that will be used to calculate the coordinates of
        its vertices
        :type equal_legs_length: a number
        :param mark_equal_sides: if True (default), all three sides will be
        automatically marked with the same symbol.
        :type mark_equal_sides: bool
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
        self._base_length = Number(base_length)
        self._equal_legs_length = Number(equal_legs_length)
        v1 = Point(base_length + start_vertex.x, start_vertex.y)
        v2 = Point(base_length / 2,
                   (equal_legs_length ** 2 - Number('0.25') * base_length ** 2)
                   .sqrt().rounded(Number('0.001')) + start_vertex.y)
        Triangle.__init__(self, start_vertex, v1, v2, name=name,
                          draw_vertices=draw_vertices,
                          label_vertices=label_vertices,
                          thickness=thickness, color=color,
                          rotation_angle=rotation_angle)
        self._type = 'IsoscelesTriangle'
        if mark_equal_sides:
            self.sides[1].mark = '//'
            self.sides[2].mark = r'\textbackslash\textbackslash'

    @property
    def base_length(self):
        return self._base_length

    @property
    def equal_legs_length(self):
        return self._equal_legs_length

    def setup_labels(self, lbl_base_length, lbl_equal_legs_length,
                     masks=None):
        """
        Convenience to easily setup IsoscelesTriangle's sides length labels.

        If masks is None, then by default, only base's label and sides[2].label
        will be shown. The other will be masked.

        :param lbl_base_length: the base's length's label
        :type lbl_base_length: a label (either str or Number)
        :param lbl_equal_legs_length: the equal legs's length's label
        :type lbl_equal_legs_length: a label (either str or Number)
        :param masks: the list of masks to setup.
        :type masks: None or list of 3 elements
        """
        if masks is None:
            masks = [None, ' ', None]
        super().setup_labels(labels=[lbl_base_length, lbl_equal_legs_length,
                                     lbl_equal_legs_length],
                             masks=masks)
