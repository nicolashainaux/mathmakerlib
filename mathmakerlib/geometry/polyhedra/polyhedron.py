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

from abc import ABCMeta, abstractmethod

from mathmakerlib.geometry.point import Point
from mathmakerlib.core.drawable import HasThickness, Colored


class Polyhedron(Colored, HasThickness, metaclass=ABCMeta):
    """Polyhedra (not drawables yet)."""

    def __init__(self, *vertices, name=None,
                 draw_vertices=False, label_vertices=True,
                 thickness='thick', color=None):
        r"""
        Initialize Polyhedron.

        :param vertices: the vertices of the Polyhedron
        :type vertices: a list of at least three Points
        :param name: the name of the Polyhedron, like ABCDEFGH.
        Can be either None (the names will be automatically created), or a
        string of the letters to use to name the vertices. Only single letters
        are supported as Points' names so far (at Polyhedron's creation).
        See issue #3.
        :type name: None or str
        :param draw_vertices: whether to actually draw, or not, the vertices
        :type draw_vertices: bool
        :param label_vertices: whether to label, or not, the vertices
        :type label_vertices: bool
        :param thickness: the thickness of the Polyhedron's edges
        :type thickness: str
        :param color: the color of the Polyhedron's edges
        :type color: str
        """
        if len(vertices) <= 3:
            raise ValueError('At least four Points are required to be able '
                             'to build a Polyhedron. Found only {} positional '
                             'arguments, though.'.format(len(vertices)))
        if any([not (isinstance(v, Point) and v.three_dimensional)
                for v in vertices]):
            for i, v in enumerate(vertices):
                if not isinstance(v, Point):
                    raise TypeError('Only Points must be provided in order to '
                                    'build a Polyhedron. Yet found {} as '
                                    'positional argument #{}.'
                                    .format(type(v), i))
                if not v.three_dimensional:
                    raise TypeError('Points used to build a Polyhedron must '
                                    'be three-dimensional Points. Found a '
                                    'two-dimensional Point instead: {}.'
                                    .format(repr(v)))
        if name is not None:
            if not isinstance(name, str):
                raise TypeError('name must be a str, found {} instead.'
                                .format(repr(name)))
            if not len(name) == len(vertices):
                raise ValueError('A polyhedron\'s name must contain as many '
                                 'letters as the polyhedron\'s number of '
                                 'vertices, yet found {} letters (name: {}) '
                                 'and {} vertices.'
                                 ''.format(len(name), repr(name),
                                           len(vertices)))
        self.thickness = thickness
        self.color = color
        self.draw_vertices = draw_vertices
        self.label_vertices = label_vertices
        self._vertices = []
        for i, v in enumerate(vertices):
            if name is None:
                vname = v.name
            else:
                vname = name[i]
            if v.name == v.label:
                lbl = 'default'
            else:
                lbl = v.label
            self._vertices.append(Point(v.x, v.y, v.z, name=vname,
                                        shape=v.shape,
                                        label=lbl, color=v.color,
                                        shape_scale=v.shape_scale))
        self._init_faces()
        self._edges = []
        for F in self.faces:
            for s in F.sides:
                if s not in self._edges:
                    self._edges.append(s)

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges

    @property
    def faces(self):
        return self._faces

    @abstractmethod
    def _init_faces(self):
        """Each new Polyhedron must define its faces."""

    @property
    def name(self):
        return ''.join([v.name for v in self.vertices])

    @property
    def draw_vertices(self):
        return self._draw_vertices

    @draw_vertices.setter
    def draw_vertices(self, value):
        if isinstance(value, bool):
            self._draw_vertices = value
        else:
            raise TypeError('draw_vertices must be a boolean; '
                            'got {} instead.'.format(type(value)))

    @property
    def label_vertices(self):
        return self._label_vertices

    @label_vertices.setter
    def label_vertices(self, value):
        if isinstance(value, bool):
            self._label_vertices = value
        else:
            raise TypeError('label_vertices must be a boolean; '
                            'got {} instead.'.format(type(value)))
