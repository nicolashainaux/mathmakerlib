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

from mathmakerlib.calculus.number import Number
from mathmakerlib.geometry.point import Point
from mathmakerlib.geometry.bipoint import Bipoint
from mathmakerlib.geometry.angle import AngleDecoration
from . import Quadrilateral


class Rectangle(Quadrilateral):
    """Rectangles."""

    def __init__(self, *points, start_vertex=None, name=None,
                 width=Number(1), length=Number(2),
                 mark_right_angles=True,
                 draw_vertices=False, label_vertices=True,
                 thickness='thick', color=None, rotation_angle=0,
                 winding=None, sloped_sides_labels=True):
        r"""
        Initialize Rectangle.

        This will be done either using the points (if provided) of the points
        parameter or using the keyword arguments start_vertex, width...

        :param points: a list of 4 points that will be the vertices of the
        Rectangle. It is possible to provide no Point at all.
        :type points: a list of Points
        :param start_vertex: the vertex to start to draw the Rectangle
        (default (0; 0))
        :type start_vertex: Point
        :param name: the name of the Rectangle, like ABCD.
        Can be either None (the names will be automatically created), or a
        string of the letters to use to name the vertices. Only single letters
        are supported as Points' names so far (at Polygon's creation).
        See issue #3.
        :type name: None or str
        :param width: the width that will be used to calculate the coordinates
        of the vertices used to build the Rectangle
        :type width: a number
        :param length: the length that will be used to calculate the
        coordinates of the vertices used to build the Rectangle
        :type length: a number
        :param mark_right_angles: if True (default), all four angles will be
        automatically marked as right angles.
        :type mark_right_angles: bool
        :param draw_vertices: whether to actually draw, or not, the vertices
        :type draw_vertices: bool
        :param label_vertices: whether to label, or not, the vertices
        :type label_vertices: bool
        :param thickness: the thickness of the Polygon's sides
        :type thickness: str
        :param color: the color of the Polygon's sides
        :type color: str
        :param rotate: the angle of rotation around isobarycenter
        :type rotate: int
        """
        if points:
            (v0, v1, v2, v3) = points
            self._length = Bipoint(v0, v1).length
            self._width = Bipoint(v1, v2).length
        else:  # 2D Rectangles only (so far)
            if start_vertex is None:
                start_vertex = Point(0, 0)
            # Accepted type for width and length is number, will be checked at
            # vertices' instanciations.
            self._width = width
            self._length = length
            v0 = start_vertex
            v1 = Point(length + start_vertex.x, start_vertex.y)
            v2 = Point(length + start_vertex.x, width + start_vertex.y)
            v3 = Point(start_vertex.x, width + start_vertex.y)
        Quadrilateral.__init__(self, v0, v1, v2, v3, name=name,
                               draw_vertices=draw_vertices,
                               label_vertices=label_vertices,
                               thickness=thickness, color=color,
                               rotation_angle=rotation_angle,
                               winding=winding,
                               sloped_sides_labels=sloped_sides_labels)
        self._type = 'Rectangle'
        if mark_right_angles:
            for a in self.angles:
                a.decoration = AngleDecoration(thickness=thickness)
                a.mark_right = True

    @property
    def width(self):
        return self._width

    @property
    def length(self):
        return self._length

    @property
    def area(self):
        return self.width * self.length

    def setup_labels(self, labels=None, linesegments=None, masks=None):
        """
        Convenience method to easily setup Rectangle's length and width labels.

        If masks is None, then by default, only sides[1] (width) and sides[2]
        (length) labels will be shown. The two others will be masked.

        If labels has only two elements, then the first one will be considered
        as the width and the second one as the length. They will be
        appropriately duplicated.

        :param labels: None or the list of the labels
        :type labels: None or list of 2 or 4 elements
        :param linesegments: the list of the LineSegments to label
        (defaults to Polygon's sides)
        :type linesegments: list (of LineSegments)
        :param masks: the list of masks to setup.
        :type masks: None or list of 4 elements
        """
        if linesegments is None:
            linesegments = self.sides
        if len(labels) == 2:
            labels = [labels[1], labels[0], labels[1], labels[0]]
        if masks is None:
            masks = [' ', None, None, ' ']
        super().setup_labels(labels=labels, linesegments=linesegments,
                             masks=masks)

    @property
    def lbl_width(self):
        if isinstance(self.sides[1].label_value, Number):
            if isinstance(self.sides[3].label_value, Number):
                if self.sides[1].label_value == self.sides[3].label_value:
                    return self.sides[1].label_value
                else:
                    raise ValueError('Two different labels have been set '
                                     'for the width: {} and {}.'
                                     .format(repr(self.sides[1].label_value),
                                             repr(self.sides[3].label_value)))
            else:
                return self.sides[1].label_value
        elif isinstance(self.sides[3].label_value, Number):
            return self.sides[3].label_value
        raise ValueError('No width has been set as a Number.')

    @property
    def lbl_length(self):
        if isinstance(self.sides[0].label_value, Number):
            if isinstance(self.sides[2].label_value, Number):
                if self.sides[0].label_value == self.sides[2].label_value:
                    return self.sides[0].label_value
                else:
                    raise ValueError('Two different labels have been set '
                                     'for the length: {} and {}.'
                                     .format(repr(self.sides[0].label_value),
                                             repr(self.sides[2].label_value)))
            else:
                return self.sides[0].label_value
        elif isinstance(self.sides[2].label_value, Number):
            return self.sides[2].label_value
        raise ValueError('No length has been set as a Number.')

    @property
    def lbl_area(self):
        return self.lbl_width * self.lbl_length
