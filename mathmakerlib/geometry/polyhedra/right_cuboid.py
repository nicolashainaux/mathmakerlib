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

from mathmakerlib.geometry.point import Point
from mathmakerlib.geometry.polygons.rectangle import Rectangle
from mathmakerlib.geometry.polyhedra.polyhedron import Polyhedron


class RightCuboid(Polyhedron):
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
        if start_vertex is None:
            start_vertex = Point(0, 0, 0)
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
        self._width, self._depth, self._height = width, depth, height
        self._labels = None
        self._edges_to_label = {}

    def _init_faces(self):
        """Faces of the RightCuboid."""
        self._faces = [Rectangle(self.vertices[0], self.vertices[1],
                                 self.vertices[2], self.vertices[3]),
                       Rectangle(self.vertices[0], self.vertices[1],
                                 self.vertices[5], self.vertices[4]),
                       Rectangle(self.vertices[1], self.vertices[2],
                                 self.vertices[6], self.vertices[5]),
                       Rectangle(self.vertices[2], self.vertices[3],
                                 self.vertices[7], self.vertices[6]),
                       Rectangle(self.vertices[3], self.vertices[0],
                                 self.vertices[4], self.vertices[7]),
                       Rectangle(self.vertices[4], self.vertices[5],
                                 self.vertices[6], self.vertices[7]),
                       ]

    def setup_labels(self, labels=None):
        """
        Easily setup RightCuboid's width, depth and height labels.

        :param labels: the labels to store: (width, depth, height)
        :type labels: tuple or list
        """
        if not (isinstance(labels, (tuple, list)) and len(labels) == 3):
            raise TypeError('labels argument must be a list or tuple, '
                            'of length 3. Found {} instead.'
                            .format(repr(labels)))
        self._labels = labels
        # These coordinates represent the face number, then the edge number.
        # Depends on _init_faces()
        self._edges_to_label = {'oblique_projection:top-right':
                                [(0, 0, 'anticlockwise'),
                                 (1, 1, 'anticlockwise'),
                                 (2, 2, 'clockwise')],
                                'oblique_projection:top-left':
                                [(0, 0, 'anticlockwise'),
                                 (1, 3, 'anticlockwise'),
                                 (4, 2, 'clockwise')],
                                'oblique_projection:bottom-left':
                                [(0, 2, 'anticlockwise'),
                                 (3, 1, 'anticlockwise'),
                                 (4, 2, 'clockwise')],
                                'oblique_projection:bottom-right':
                                [(0, 2, 'anticlockwise'),
                                 (2, 1, 'clockwise'),
                                 (2, 2, 'clockwise')],
                                }

    @property
    def width(self):
        return self._width

    @property
    def depth(self):
        return self._depth

    @property
    def height(self):
        return self._height

    @property
    def labels(self):
        return self._labels

    @property
    def lbl_width(self):
        if self.labels is None:
            raise AttributeError('Labels must be set before trying to get '
                                 'them.')
        return self.labels[0]

    @property
    def lbl_depth(self):
        if self.labels is None:
            raise AttributeError('Labels must be set before trying to get '
                                 'them.')
        return self.labels[1]

    @property
    def lbl_height(self):
        if self.labels is None:
            raise AttributeError('Labels must be set before trying to get '
                                 'them.')
        return self.labels[2]

    @property
    def edges_to_label(self):
        return self._edges_to_label

    @property
    def lbl_volume(self):
        if self.labels is None:
            raise AttributeError('Labels must be set before trying to get '
                                 'them.')
        return self.lbl_width * self.lbl_depth * self.lbl_height
