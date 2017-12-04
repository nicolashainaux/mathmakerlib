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
from . import Triangle, Equilateral


class EquilateralTriangle(Triangle, Equilateral):
    """Equilateral Triangles."""

    def __init__(self, start_vertex=None, name=None,
                 side_length=Number('1'),
                 mark_equal_sides=True,
                 draw_vertices=False, label_vertices=True,
                 thickness='thick', color=None, rotation_angle=0):
        r"""
        Initialize Equilateral Triangle

        :param start_vertex: the vertex to start to draw the Right Triangle
        (default (0; 0))
        :type start_vertex: Point
        :param name: the name of the Triangle, like ABC.
        Can be either None (the names will be automatically created), or a
        string of the letters to use to name the vertices. Only single letters
        are supported as Points' names so far (at Polygon's creation).
        See issue #3.
        :type name: None or str
        :param side_length: the length that will be used to calculate the
        coordinates of the vertices used to build the EquilateralTriangle
        :type side_length: a number
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
        self._side_length = Number(side_length)
        v1 = Point(side_length, 0)
        v2 = Point(side_length / 2,
                   (side_length * Number(3).sqrt() * Number('0.5'))
                   .rounded(Number('0.001')))
        Triangle.__init__(self, start_vertex, v1, v2, name=name,
                          draw_vertices=draw_vertices,
                          label_vertices=label_vertices,
                          thickness=thickness, color=color,
                          rotation_angle=rotation_angle)
        Equilateral.__init__(self, mark_equal_sides=mark_equal_sides)
        self._type = 'EquilateralTriangle'

    @property
    def side_length(self):
        return self._side_length

    def setup_labels(self, lbl_side_length, masks=None):
        """
        Convenience to easily setup EquilateralTriangle's side length label.

        If masks is None, then by default, only sides[2].label will be shown.
        The two others will be masked.

        :param lbl_side_length: the side's length's label
        :type lbl_side_length: a label (either str or Number)
        :param masks: the list of masks to setup.
        :type masks: None or list of 3 elements
        """
        if masks is None:
            masks = self.default_masks
        super().setup_labels(labels=[lbl_side_length, lbl_side_length,
                                     lbl_side_length],
                             masks=masks)
