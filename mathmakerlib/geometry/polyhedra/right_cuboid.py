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
from mathmakerlib.core.drawable import Drawable
from mathmakerlib.geometry.polyhedra.polyhedron import Polyhedron


class RightCuboid(Drawable, Polyhedron):
    """Right Cuboids."""

    def __init__(self, start_vertex=None, dimensions=None, name=None,
                 draw_vertices=False, label_vertices=True,
                 thickness='thick', color=None):
        r"""
        Initialize Right Cuboid

        :param start_vertex: the vertex to start to draw the Right Cuboid
        (default (0; 0))
        :type start_vertex: Point (must be a 3D Point)
        :param dimensions: (width, depth, height)
        :type dimensions: tuple (of numbers)
        :param name: the name of the RightCuboid, like ABCDEFGH.
        Can be either None (the names will be automatically created), or a
        string of the letters to use to name the vertices. Only single letters
        are supported as Points' names so far (at Polyhedra's creation).
        See issue #3.
        :type name: None or str
        :param draw_vertices: whether to actually draw, or not, the vertices
        :type draw_vertices: bool
        :param label_vertices: whether to label, or not, the vertices
        :type label_vertices: bool
        :param thickness: the thickness of the RightCuboid's edges
        :type thickness: str
        :param color: the color of the RightCuboid's edges
        :type color: str
        """
        if not isinstance(start_vertex, Point):
            raise TypeError('start_vertex must be a Point; found {} instead.'
                            .format(repr(start_vertex)))
        if not start_vertex.three_dimensional:
            raise TypeError('start_vertex must be a three-dimensional Point. '
                            'Found this two-dimensional Point instead: {}.'
                            .format(repr(start_vertex)))
        if not isinstance(dimensions, (tuple, list)):
            raise TypeError('dimensions must be a tuple or a list. Found {} '
                            'instead.'.format(dimensions))
        if not len(dimensions) == 3:
            raise TypeError('dimensions must have a length of 3. Found {} '
                            'instead.'.format(dimensions))
        x, y, z = start_vertex.coordinates
        width, depth, height = dimensions
        vertices = [start_vertex,
                    Point(x + width, y, z),
                    Point(x + width, y + depth, z),
                    Point(x, y + depth, z),
                    Point(x, y, z + height),
                    Point(x + width, y, z + height),
                    Point(x + width, y + depth, z + height),
                    Point(x, y + depth, z + height)]
        Polyhedron.__init__(self, *vertices, name=name,
                            draw_vertices=draw_vertices,
                            label_vertices=label_vertices,
                            thickness=thickness, color=color)

    def tikz_declarations(self):
        """
        Return the necessary declarations (e.g. Points declarations).

        :rtype: str
        """

    def _tikz_draw_options(self):
        """
        The list of possible options for draw command.

        :rtype: list
        """

    def tikz_drawing_comment(self):
        """
        Return the comments matching each drawing category.

        :rtype: list
        """

    def tikz_draw(self):
        """
        Return the commands to actually draw the object.

        They should be grouped in categories (the Points, the Segments etc.).
        Caution, this method must return a list (containing one string per
        category). tikz_drawing_comment() must return a list containing as many
        elements as this one.

        :rtype: list
        """

    def tikz_label(self):
        """Return the command to write the object's label."""

    def tikz_points_labels(self):
        """Return the command to write the object's points' labels."""
