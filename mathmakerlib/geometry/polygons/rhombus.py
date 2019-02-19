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
                 mark_equal_sides=True, use_mark='||',
                 draw_vertices=False, label_vertices=True,
                 thickness='thick', color=None, rotation_angle=0,
                 winding=None, sloped_sides_labels=True):
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
        coordinates of the vertices used to build the Rhombus
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
        v1 = Point(x + start_vertex.x, -y + start_vertex.y)
        v2 = Point(2 * x + start_vertex.x, start_vertex.y)
        v3 = Point(x + start_vertex.x, y + start_vertex.y)
        Quadrilateral.__init__(self, start_vertex, v1, v2, v3, name=name,
                               draw_vertices=draw_vertices,
                               label_vertices=label_vertices,
                               thickness=thickness, color=color,
                               rotation_angle=rotation_angle,
                               winding=winding,
                               sloped_sides_labels=sloped_sides_labels)
        self._type = 'Rhombus'
        Equilateral.__init__(self, mark_equal_sides=mark_equal_sides,
                             use_mark=use_mark)

    @property
    def side_length(self):
        return self._side_length

    def setup_labels(self, labels=None, linesegments=None, masks=None):
        """
        Convenience method to easily setup Rhombus' side length label.

        If masks is None, then by default, only sides[3].label will be shown.
        The three others will be masked.

        If labels has only one element, then it is duplicated four times.

        :param labels: None or the list of the labels
        :type labels: None or list of 1 or 4 elements
        :param linesegments: the list of the LineSegments to label
        (defaults to Polygon's sides)
        :type linesegments: list (of LineSegments)
        :param masks: the list of masks to setup.
        :type masks: None or list of 4 elements
        """
        if masks is None:
            masks = self.default_masks
        if linesegments is None:
            linesegments = self.sides
        if len(labels) == 1:
            labels *= 4
        super().setup_labels(labels=labels, linesegments=linesegments,
                             masks=masks)
