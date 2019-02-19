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
from . import Rectangle, Rhombus, Equilateral


class Square(Rectangle, Rhombus):
    """Squares."""

    def __init__(self, start_vertex=None, name=None,
                 side_length=Number('1'),
                 mark_right_angles=True,
                 mark_equal_sides=True, use_mark='||',
                 draw_vertices=False, label_vertices=True,
                 thickness='thick', color=None, rotation_angle=0,
                 winding=None, sloped_sides_labels=True):
        r"""
        Initialize Square

        :param start_vertex: the vertex to start to draw the Square
        (default (0; 0))
        :type start_vertex: Point
        :param name: the name of the Square, like ABCDE for a pentagon. Can
        be either None (the names will be automatically created), or a
        string of the letters to use to name the vertices. Only single letters
        are supported as Points' names so far (at Polygon's creation).
        See issue #3.
        :type name: None or str
        :param side_length: the length that will be used to calculate the
        coordinates of the vertices used to build the Square
        :type side_length: a number
        :param mark_right_angles: if True (default), all four angles will be
        automatically marked as right angles.
        :type mark_right_angles: bool
        :param mark_equal_sides: if True (default), all four sides will be
        automatically marked with the same symbol.
        :type mark_equal_sides: bool
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
        Rectangle.__init__(self, start_vertex=start_vertex, name=name,
                           width=side_length, length=side_length,
                           mark_right_angles=mark_right_angles,
                           draw_vertices=draw_vertices,
                           label_vertices=label_vertices,
                           thickness=thickness, color=color,
                           rotation_angle=rotation_angle,
                           winding=winding,
                           sloped_sides_labels=sloped_sides_labels)
        # TODO: see issue #5
        # Accepted type for side_length is number, already checked at
        # vertices' instanciations (in Rectangle.__init__() call).
        self._side_length = Number(side_length)
        Equilateral.__init__(self, mark_equal_sides=mark_equal_sides,
                             use_mark=use_mark)
        self._type = 'Square'

    @property
    def side_length(self):
        return self._side_length

    def setup_labels(self, labels=None, linesegments=None, masks=None):
        """Same as Rhombus.setup_labels()."""
        Rhombus.setup_labels(self, labels=labels, linesegments=linesegments,
                             masks=masks)

    @property
    def lbl_width(self):
        return self.lbl_side_length

    @property
    def lbl_length(self):
        return self.lbl_side_length
