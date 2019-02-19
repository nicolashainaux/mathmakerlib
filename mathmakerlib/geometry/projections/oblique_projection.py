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

from math import radians, sin, cos

from mathmakerlib import config
from mathmakerlib.core.drawable import Drawable, tikz_approx_position
from mathmakerlib.core.drawable import HasThickness
from mathmakerlib.geometry.tools import convex_hull
from mathmakerlib.calculus.tools import is_number
from mathmakerlib.geometry.point import Point
from mathmakerlib.geometry.linesegment import LineSegment
from mathmakerlib.geometry.vector import Vector
from mathmakerlib.geometry.polyhedra import Polyhedron

DIRECTION_VALUES = ['top-left', 'top-right', 'bottom-left', 'bottom-right']


def check_direction(value):
    if value not in DIRECTION_VALUES:
        raise ValueError('Allowed values for direction argument are {}. '
                         'Found {} instead.'
                         .format(DIRECTION_VALUES, repr(value)))


class ObliqueProjection(Drawable, HasThickness):
    """
    Oblique projection of 3D objects.

    The objects will be projected on the XOY plane.
    Introduced in version 0.7, supporting only Polyhedra projections yet.
    """

    def __init__(self, object3D=None, k=None, α=None, direction=None,
                 thickness='thick', color=None,
                 draw_vertices=False, label_vertices=False):
        r"""
        Initialize ObliqueProjection.

        :param object3D: the object to project.
        :type object3D: Polyhedron
        :param k: the ratio of the oblique projection. Defaults to
        config.oblique_projection.RATIO
        :type k: number
        :param α: the angle between the receding Z-axis, and X-axis.
        :type α: number
        :param direction: 'top-left', 'top-right', 'bottom-left' or
        'bottom-right'
        :type direction: str
        """
        self.draw_vertices = draw_vertices
        self.label_vertices = label_vertices
        if k is None:
            k = config.oblique_projection.RATIO
        if not is_number(k):
            raise TypeError('Ratio k must be a number. Found {} instead.'
                            .format(repr(k)))
        if α is None:
            α = config.oblique_projection.RECEDING_AXIS_ANGLE
        if direction is None:
            direction = config.oblique_projection.DIRECTION
        if not is_number(α):
            raise TypeError('Angle α must be a number. Found {} instead.'
                            .format(repr(α)))
        if not isinstance(object3D, Polyhedron):
            raise TypeError('object3D must be a Polyhedron, found {} instead.'
                            .format(repr(object3D)))
        check_direction(direction)
        self._direction = direction
        self._object3D_name = type(object3D).__name__

        # Setup the edges' labels
        if object3D.labels is not None:
            edges_to_label = object3D.edges_to_label['oblique_projection:{}'
                                                     .format(direction)]
            w_coord, d_coord, h_coord = edges_to_label
            object3D.faces[w_coord[0]].sides[w_coord[1]].unlock_label()
            object3D.faces[w_coord[0]].sides[w_coord[1]].label_winding = \
                w_coord[2]
            object3D.faces[w_coord[0]].sides[w_coord[1]].label = \
                object3D.labels[0]
            object3D.faces[w_coord[0]].sides[w_coord[1]].lock_label()
            object3D.faces[d_coord[0]].sides[d_coord[1]].unlock_label()
            object3D.faces[d_coord[0]].sides[d_coord[1]].label_winding = \
                d_coord[2]
            object3D.faces[d_coord[0]].sides[d_coord[1]].label = \
                object3D.labels[1]
            object3D.faces[d_coord[0]].sides[d_coord[1]].lock_label()
            object3D.faces[h_coord[0]].sides[h_coord[1]].unlock_label()
            object3D.faces[h_coord[0]].sides[h_coord[1]].label_winding = \
                h_coord[2]
            object3D.faces[h_coord[0]].sides[h_coord[1]].label = \
                object3D.labels[2]
            object3D.faces[h_coord[0]].sides[h_coord[1]].lock_label()

        matrix = {'top-right': [[1, 0, k * sin(radians(α))],
                                [0, 1, k * cos(radians(α))]],
                  'bottom-right': [[1, 0, k * sin(radians(α))],
                                   [0, 1, -k * cos(radians(α))]],
                  'bottom-left': [[1, 0, -k * sin(radians(α))],
                                  [0, 1, -k * cos(radians(α))]],
                  'top-left': [[1, 0, -k * sin(radians(α))],
                               [0, 1, k * cos(radians(α))]]}[direction]
        self._edges = []
        self._edges3D = {}
        self._vertices = []
        self._vertices_match = {}

        def project(point, matrix):
            x = sum([pc * coord
                     for pc, coord in zip(matrix[0],
                                          point.coordinates)])
            y = sum([pc * coord
                     for pc, coord in zip(matrix[1],
                                          point.coordinates)])
            return Point(x, y, point.name)

        for vertex in object3D.vertices:
            projected_point = project(vertex, matrix)
            self._vertices.append(projected_point)
            self._vertices_match[vertex.name] = (vertex, projected_point)

        # To store to which edges a vertex belongs
        vertices_connexions = {k: [] for k in self._vertices}

        # Build the projected edges
        for edge in object3D.edges:
            p0 = self._vertices_match[edge.endpoints[0].name][1]
            p1 = self._vertices_match[edge.endpoints[1].name][1]
            # TODO: check cases when the projected edge is a single point
            # (ZeroBipoint should be raised)
            projected_edge = LineSegment(p0, p1,
                                         thickness=thickness,
                                         draw_endpoints=draw_vertices,
                                         label_endpoints=label_vertices,
                                         color=color,
                                         allow_zero_length=False,
                                         locked_label=True,
                                         label_scale=edge.label_scale,
                                         label=edge.label,
                                         label_mask=edge.label_mask,
                                         label_winding=edge.label_winding,
                                         sloped_label=False)
            vertices_connexions[p0].append(LineSegment(p0, p1))
            vertices_connexions[p1].append(LineSegment(p1, p0))
            if projected_edge not in self._edges:  # TODO: else, what...?
                self._edges.append(projected_edge)
            if projected_edge not in self._edges3D:  # TODO: else, what...?
                self._edges3D[projected_edge] = edge
        # Find out which edges are hidden.
        # The ones that belong to convex hull of the projected vertices are
        # considered visible. By default, they will remain visible (i.e. keep
        # the default 'solid' dashpattern).
        points_cloud = set()  # to avoid duplicates
        for edge in self.edges:
            points_cloud.update(edge.endpoints)
        cvh = convex_hull(*points_cloud)
        for edge in self.edges:
            # Only edges not belonging to the convex hull may be hidden
            if not (edge.endpoints[0] in cvh and edge.endpoints[1] in cvh):
                m = self._edges3D[edge].midpoint()
                pm = project(m, matrix)  # projected midpoint
                # Check if the midpoint of the tested edge is behind (i.e.
                # deeper) than a face while being inside it
                for f in object3D.faces:
                    pface = [project(v, matrix) for v in f.vertices]
                    if (all([v.z <= m.z for v in f.vertices])
                        and pm not in convex_hull(pm, *pface)
                        and not any(m.belongs_to(s) for s in f.sides)):
                        edge.dashpattern = \
                            config.oblique_projection.DASHPATTERN

        # Setup the vertices' labels
        for vertex in self.vertices:
            edges = sorted(vertices_connexions[vertex],
                           key=lambda edge: Vector(edge).slope360)
            couples = [(edges[n], edges[(n + 1) % len(edges)])
                       for n, _ in enumerate(edges)]
            widest = max(couples,
                         key=lambda couple:
                         Vector(couple[0]).angle_measure(Vector(couple[1])))
            u = Vector(vertex, widest[0].endpoints[1])
            v = Vector(vertex, widest[1].endpoints[1])
            vertex.label_position = \
                tikz_approx_position(u.bisector(v).slope360)

    @property
    def edges(self):
        return self._edges

    @property
    def vertices(self):
        return self._vertices

    @property
    def object3D_name(self):
        return self._object3D_name

    @property
    def draw_vertices(self):
        return self._draw_vertices

    @draw_vertices.setter
    def draw_vertices(self, value):
        if isinstance(value, bool):
            self._draw_vertices = value
        else:
            raise TypeError('draw_vertices must be a boolean; '
                            'found {} instead.'.format(type(value)))

    @property
    def label_vertices(self):
        return self._label_vertices

    @label_vertices.setter
    def label_vertices(self, value):
        if isinstance(value, bool):
            self._label_vertices = value
        else:
            raise TypeError('label_vertices must be a boolean; '
                            'found {} instead.'.format(type(value)))

    def tikz_declarations(self):
        """Return the Points declarations."""
        return '\n'.join([v.tikz_declarations() for v in self.vertices])

    def _tikz_draw_options(self):
        """Unused, as the picture consists of several draw commands."""

    def _tikz_draw_vertices(self):
        return '\n'.join([v.tikz_draw()[0] for v in self.vertices]) + '\n'

    def tikz_drawing_comment(self):
        """Return the comment preceding the Oblique Projection's drawing."""
        output = []
        if self.draw_vertices:
            output.append('% Draw Vertices')
        output.append('% Draw Oblique Projection of {}'
                      .format(self.object3D_name))
        return output

    def tikz_draw(self):
        """
        Return the commands to actually draw the projected 3D object.

        :rtype: list
        """
        output = []
        if self.draw_vertices:
            output.append(self._tikz_draw_vertices())
        drawn_edges = ''
        for edge in self.edges:
            drawn_edges += edge.tikz_draw()[-1] + '\n'
        output.append(drawn_edges)
        return output

    def tikz_label(self):
        """Return the command to write the object's label."""

    def tikz_points_labels(self):
        """Return the command to write the Vertices' labels."""
        if self.label_vertices:
            return '\n'.join([v.tikz_label() for v in self.vertices])
        return ''
