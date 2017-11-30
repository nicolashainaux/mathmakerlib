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

from math import cos, sin, radians

from mathmakerlib.calculus.tools import is_number
from mathmakerlib.calculus.number import Number
from mathmakerlib.geometry.point import Point
from . import Quadrilateral, Equilateral


class Rhombus(Quadrilateral, Equilateral):
    """Rhombi."""

    def __init__(self, start_vertex=None, name=None,
                 side_length=Number('1'),
                 build_angle=60,
                 mark_equal_sides=True,
                 draw_vertices=False, label_vertices=True,
                 thickness='thick', color=None, rotation_angle=0):
        r"""
        Initialize Rhombus

        :param start_vertex: the vertex to start to draw the Rhombus
        (default (0; 0))
        :type start_vertex: Point
        :param name: the name of the Rhombus, like ABCD.
        Can be either None (the names will be automatically created), or a
        string of the letters to use to name the vertices. Only single letters
        are supported as Points' names so far (at Polygon's creation).
        See issue #3.
        :type name: None or str
        :param side_length: the length that will be used to calculate the
        coordinates of the vertices used to build the Square
        :type side_length: a number
        :param build_angle: one of the interior angles of the Rhombus.
        :type build_angle: any number
        :param mark_equal_sides: if True (default), all four sides will be
        automatically marked with the same symbol.
        :type mark_equal_sides: bool
        :param draw_vertices: whether to actually draw, or not, the vertices
        :type draw_vertices: bool
        :param label_vertices: whether to label, or not, the vertices
        :type label_vertices: bool
        :param thickness: the thickness of the Quadrilateral's sides
        :type thickness: str
        :param color: the color of the Quadrilateral's sides
        :type color: str
        :param rotate: the angle of rotation around isobarycenter
        :type rotate: int
        """
        if start_vertex is None:
            start_vertex = Point(0, 0)
        self._side_length = Number(side_length)
        if is_number(build_angle):
            self._build_angle = build_angle
        else:
            raise TypeError('Expected an integer as build_angle, found {}.'
                            .format(type(build_angle)))
        x = (side_length * Number(str(cos(radians(build_angle / 2)))))\
            .rounded(Number('0.001'))
        y = (side_length * Number(str(sin(radians(build_angle / 2)))))\
            .rounded(Number('0.001'))
        v1 = Point(x, -y)
        v2 = Point(2 * x, 0)
        v3 = Point(x, y)
        Quadrilateral.__init__(self, start_vertex, v1, v2, v3, name=name,
                               draw_vertices=draw_vertices,
                               label_vertices=label_vertices,
                               thickness=thickness, color=color,
                               rotation_angle=rotation_angle)
        self._type = 'Rhombus'
        Equilateral.__init__(self, mark_equal_sides=mark_equal_sides)

    @property
    def side_length(self):
        return self._side_length

    def setup_labels(self, lbl_side_length, masks=None):
        """
        Convenience method to easily setup Rhombus' side length label.

        If masks is None, then by default, only sides[3].label will be shown.
        The three others will be masked.

        :param lbl_side_length: the side's length's label
        :type lbl_side_length: a label (either str or Number)
        :param masks: the list of masks to setup.
        :type masks: None or list of 4 elements
        """
        if masks is None:
            masks = [' ', ' ', ' ', None]
        super().setup_labels(labels=[lbl_side_length, lbl_side_length,
                                     lbl_side_length, lbl_side_length],
                             masks=masks)

    @property
    def lbl_side_length(self):
        collected_values = []
        for s in self.sides:
            if isinstance(s.label_value, Number):
                collected_values.append(s.label_value)
        if not collected_values:
            raise ValueError('Found no side labeled as a Number.')
        ref = collected_values[0]
        for v in collected_values:
            if v != ref:
                raise ValueError('Found different values for the sides: {} '
                                 'and {}.'.format(repr(ref), repr(v)))
        return ref
