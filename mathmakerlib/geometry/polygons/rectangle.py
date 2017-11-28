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
from mathmakerlib.geometry.angle import AngleMark
from . import Polygon


class Rectangle(Polygon):
    """Rectangles."""

    def __init__(self, start_vertex=None, name=None,
                 width=Number(1), length=Number(2),
                 mark_right_angles=True,
                 draw_vertices=False, label_vertices=True,
                 thickness='thick', color=None, rotation_angle=0):
        r"""
        Initialize Rectangle

        :param start_vertex: the vertex to start to draw the Rectangle
        (default (0; 0))
        :type start_vertex: Point
        :param name: the name of the Rectangle, like ABCDE for a pentagon. Can
        be either None (the names will be automatically created), or a
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
        if start_vertex is None:
            start_vertex = Point(0, 0)
        # Accepted type for width and length is number, will be checked at
        # vertices' instanciations.
        self._width = width
        self._length = length
        v1 = Point(length, 0)
        v2 = Point(length, width)
        v3 = Point(0, width)
        Polygon.__init__(self, start_vertex, v1, v2, v3, name=name,
                         draw_vertices=draw_vertices,
                         label_vertices=label_vertices,
                         thickness=thickness, color=color,
                         rotation_angle=rotation_angle)
        self._type = 'Rectangle'
        if mark_right_angles:
            for a in self.angles:
                a.mark = AngleMark()
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

    def setup_labels(self, lbl_width, lbl_length, masks=None):
        """
        Convenience method to easily setup Rectangle's length and width labels.

        If masks is None, then by default, only side[1] (width) and side[2]
        (length) labels will be shown. The two others will be masked.

        :param lbl_length: the lengths' labels
        :type lbl_length: a label (either str or Number)
        :param lbl_width: the widths' labels
        :type lbl_width: a label (either str or Number)
        :param masks: the list of masks to setup.
        :type masks: None or list of 4 elements
        """
        if masks is None:
            masks = [' ', None, None, ' ']
        if len(masks) != 4:
            raise ValueError('All four masks must be setup. Found {} values '
                             'instead.'.format(len(masks)))
        for s in self.sides:
            s.unlock_label()
        self.sides[0].label = self.sides[2].label = lbl_length
        self.sides[1].label = self.sides[3].label = lbl_width
        for s in self.sides:
            s.lock_label()
        for i, m in enumerate(masks):
            self.sides[i].label_mask = m

    @property
    def lbl_width(self):
        return self.sides[1].label_value

    @property
    def lbl_length(self):
        return self.sides[0].label_value

    @property
    def lbl_area(self):
        if not isinstance(self.lbl_width, Number):
            raise TypeError('The Rectangle\'s width has not been set as a '
                            'Number. Cannot calculate the area from labels.')
        if not isinstance(self.lbl_length, Number):
            raise TypeError('The Rectangle\'s length has not been set as a '
                            'Number. Cannot calculate the area from labels.')
        return self.lbl_width * self.lbl_length
