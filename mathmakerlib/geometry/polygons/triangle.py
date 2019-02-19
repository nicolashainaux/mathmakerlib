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

from . import Polygon


class Triangle(Polygon):
    """Triangles."""

    def __init__(self, *vertices, name=None,
                 draw_vertices=False, label_vertices=True,
                 thickness='thick', color=None, rotation_angle=0,
                 winding=None, sloped_sides_labels=True):
        r"""
        Initialize Triangle

        :param vertices: the vertices of the Triangle
        :type vertices: a list of three Points
        :param name: the name of the Triangle, like ABC.
        Can be either None (the names will be automatically created), or a
        string of the letters to use to name the vertices. Only single letters
        are supported as Points' names so far (at Polygon's creation).
        See issue #3.
        :type name: None or str
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
        if len(vertices) != 3:
            raise ValueError('Three vertices are required to build a '
                             'Triangle. Found {} instead.'
                             .format(len(vertices)))
        Polygon.__init__(self, *vertices, name=name,
                         draw_vertices=draw_vertices,
                         label_vertices=label_vertices,
                         thickness=thickness, color=color,
                         rotation_angle=rotation_angle,
                         winding=winding,
                         sloped_sides_labels=sloped_sides_labels)
        self._type = 'Triangle'

    def setup_labels(self, labels=None, linesegments=None, masks=None):
        """
        Convenience method to easily setup Triangle's sides' labels.

        If masks is None, then by default, all labels will be masked.

        :param labels: None or the list of the labels
        :type labels: None or list of 3 elements
        :param linesegments: the list of the LineSegments to label
        (defaults to Polygon's sides)
        :type linesegments: list (of LineSegments)
        :param masks: the list of masks to setup. If None (default), all masks
        will be set to None.
        :type masks: None or list of 3 elements
        """
        if labels is None:
            labels = [None, None, None]
        if masks is None:
            masks = [None, None, None]
        if len(labels) != 3:
            raise ValueError('All three labels must be setup. Found {} values '
                             'instead.'.format(len(labels)))
        if len(masks) != 3:
            raise ValueError('All three masks must be setup. Found {} values '
                             'instead.'.format(len(masks)))
        if linesegments is None:
            linesegments = self.sides
        super().setup_labels(labels=labels, linesegments=linesegments,
                             masks=masks)
