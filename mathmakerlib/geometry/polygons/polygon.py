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

from copy import deepcopy
from statistics import mean

from mathmakerlib import mmlib_setup
from mathmakerlib.calculus.number import Number
from mathmakerlib.calculus.tools import is_number
from mathmakerlib.core.drawable import Drawable, HasThickness, Colored
from mathmakerlib.core.oriented import Oriented, check_winding
from mathmakerlib.core.drawable import tikz_approx_position, tikz_options_list
from mathmakerlib.geometry.point import Point, OPPOSITE_LABEL_POSITIONS
from mathmakerlib.geometry.linesegment import LineSegment
from mathmakerlib.geometry.vector import Vector
from mathmakerlib.geometry.angle import Angle

POLYGONS_TYPES = {3: 'Triangle', 4: 'Quadrilateral', 5: 'Pentagon',
                  6: 'Hexagon', 7: 'Heptagon', 8: 'Octogon',
                  9: 'Nonagon', 10: 'Decagon', 11: 'Hendecagon',
                  12: 'Dodecagon', 13: 'Tridecagon', 14: 'Tetradecagon',
                  15: 'Pentadecagon', 16: 'Hexadecagon', 17: 'Heptadecagon',
                  18: 'Octodecagon', 19: 'Enneadecagon', 20: 'Icosagon'}


def shoelace_formula(*points):
    x = [v.x for v in points]
    y = [v.y for v in points]
    x.append(x[0])
    y.append(y[0])
    x.append(x[1])
    y.append(y[1])
    return sum(x[i] * (y[i + 1] - y[i - 1])
               for i in range(1, len(points) + 1)) / 2


class Polygon(Drawable, Colored, HasThickness, Oriented):
    """Polygons."""

    def __init__(self, *vertices, name=None,
                 draw_vertices=False, label_vertices=True,
                 thickness='thick', color=None, rotation_angle=0,
                 winding=None):
        r"""
        Initialize Polygon

        :param vertices: the vertices of the Polygon
        :type vertices: a list of at least three Points
        :param name: the name of the Polygon, like ABCDE for a pentagon. Can
        be either None (the names of the provided Points will be kept), or a
        string of the letters to use to rename the provided Points. Only
        single letters are supported as Points' names so far (at Polygon's
        creation). See issue #3.
        :type name: None or str
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
        :param winding: force the winding to be either 'clockwise' or
        'anticlockwise'. If left to None (default), doesn't force anything,
        the winding will be either forced by the value of
        mmlib_setup.DEFAULT_POLYGON_WINDING, or if it is None too, then the
        winding will be deduced from the given vertices' order.
        :type winding: None or a str ('clockwise' or 'anticlockwise')
        """
        self.thickness = thickness
        self.color = color
        self.draw_vertices = draw_vertices
        self.label_vertices = label_vertices
        if len(vertices) <= 2:
            raise ValueError('At least three Points are required to be able '
                             'to build a Polygon. Got only {} positional '
                             'arguments, though.'.format(len(vertices)))
        if any([not isinstance(v, Point) for v in vertices]):
            for i, v in enumerate(vertices):
                if not isinstance(v, Point):
                    raise TypeError('Only Points must be provided in order to '
                                    'build a Polygon. Got a {} as positional '
                                    'argument #{}.'.format(type(v), i))
        if not is_number(rotation_angle):
            raise TypeError('Expected a number as rotation angle, got a {} '
                            'instead.'.format(type(rotation_angle)))
        if name is not None:
            if len(name) != len(vertices):
                raise ValueError('The number of provided vertices ({}) does '
                                 'not match the number of Points\' names '
                                 '({}).'.format(len(vertices), len(name)))

        if (winding is None
            and mmlib_setup.polygons.DEFAULT_WINDING is not None):
            winding = mmlib_setup.polygons.DEFAULT_WINDING

        if winding is not None:
            check_winding(winding)

        if shoelace_formula(*vertices) < 0:
            if winding == 'anticlockwise':
                vertices = vertices[::-1]
                self.winding = 'anticlockwise'
            else:
                self.winding = 'clockwise'
        else:
            if winding == 'clockwise':
                vertices = vertices[::-1]
                self.winding = 'clockwise'
            else:
                self.winding = 'anticlockwise'

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
            self._vertices.append(Point(v.x, v.y, name=vname, shape=v.shape,
                                        label=lbl, color=v.color,
                                        shape_scale=v.shape_scale))
        if rotation_angle:
            center = self.isobarycenter()
            for i in range(len(self._vertices)):
                self._vertices[i] = self._vertices[i].rotate(
                    center=center,
                    angle=rotation_angle,
                    rename=None)

        self._sides = []
        shifted_vertices = deepcopy(self._vertices)
        shifted_vertices += [shifted_vertices.pop(0)]
        for (v0, v1) in zip(self._vertices, shifted_vertices):
            self._sides += [LineSegment(v0, v1, label_position=self.winding,
                                        locked_label=True)]
        self._angles = []
        left_shifted_vertices = deepcopy(self._vertices)
        left_shifted_vertices = \
            [left_shifted_vertices.pop(-1)] + left_shifted_vertices
        for (v0, v1, v2) in zip(left_shifted_vertices,
                                self._vertices,
                                shifted_vertices):
            self._angles += [Angle(v2, v1, v0)]
        for i in range(len(self._vertices)):
            bisector = Vector(self._vertices[i], shifted_vertices[i])\
                .bisector_vector(Vector(self._vertices[i],
                                        left_shifted_vertices[i]))
            self._vertices[i].label_position = OPPOSITE_LABEL_POSITIONS[
                tikz_approx_position(bisector.slope360)]

        if len(self._sides) in POLYGONS_TYPES:
            self._type = POLYGONS_TYPES[len(self._sides)]
        else:
            self._type = \
                '{n}-sided Polygon'.format(n=str(len(self._sides)))

    def __repr__(self):
        return '{} {}'.format(self.type, self.name)

    @property
    def vertices(self):
        return self._vertices

    @property
    def sides(self):
        return self._sides

    @property
    def angles(self):
        return self._angles

    @property
    def name(self):
        return ''.join([v.name for v in self.vertices])

    @property
    def type(self):
        return self._type

    def isobarycenter(self, name='automatic'):
        return Point(mean([v.x for v in self.vertices]),
                     mean([v.y for v in self.vertices]),
                     name)

    @property
    def perimeter(self):
        return sum([s.length for s in self.sides])

    @property
    def lbl_perimeter(self):
        if any([not isinstance(s.label_value, Number) for s in self.sides]):
            raise RuntimeError('All labels must have been set as Numbers '
                               'in order to calculate the perimeter from '
                               'labels.')
        else:
            return sum([s.label_value for s in self.sides],
                       Number(0, unit=self.sides[0].label_value.unit))

    def setup_labels(self, labels=None, linesegments=None, masks=None):
        """
        Convenience method to easily setup all sides' labels in a row.

        If labels is None, then the labels won't be set.
        If masks is None, then the masks won't be set.
        At least labels or masks must be different from None.

        If linesegments is None, it defaults to the Polygon's sides. This is
        practical if extra line segments require labeling, like in
        InterceptTheoremFigure, or if one wants to label a diagonal.

        It is expected that both the labels' and line segments' lists
        have the same length.

        :param labels: None or the list of the labels
        :type labels: list
        :param linesegments: the list of the LineSegments to label
        (defaults to Polygon's sides)
        :type linesegments: list (of LineSegments)
        :param masks: the list of masks to setup. If None (default), all masks
        will be set to None.
        :type masks: None or list
        """
        if labels is None and masks is None:
            raise ValueError('There must be at least either labels or masks '
                             'to setup. Both are undefined (None).')
        if linesegments is None:
            linesegments = self.sides
        if labels is not None and len(labels) != len(linesegments):
            raise ValueError('The number of labels ({}) should be equal '
                             'to the number of line segments ({}).'
                             .format(str(len(labels)),
                                     str(len(linesegments))))
        if masks is None:
            masks = [None for _ in range(len(linesegments))]
        if len(masks) != len(linesegments):
            raise ValueError('The number of label masks ({}) should be equal '
                             'to the number of line segments ({}).'
                             .format(str(len(masks)),
                                     str(len(linesegments))))
        if labels is not None:
            for (ls, lbl) in zip(linesegments, labels):
                ls.unlock_label()
                ls.label = lbl
                ls.lock_label()
        for (ls, m) in zip(linesegments, masks):
            ls.label_mask = m

    def setup_marks(self, marks=None, linesegments=None):
        """
        Convenience method to easily setup all sides' marks in a row.

        If marks is None, no LineSegment's mark will be set.

        :param marks: None or the list of the marks
        :type marks: list
        :param linesegments: the list of the LineSegments to mark
        (defaults to Polygon's sides)
        :type linesegments: list (of LineSegments)
        """
        if linesegments is None:
            linesegments = self.sides
        if marks is not None and len(marks) == len(linesegments):
            for s, m in zip(linesegments, marks):
                s.mark = m

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

    def tikz_declarations(self):
        """Return the Points declarations."""
        return '\n'.join([v.tikz_declarations() for v in self.vertices])

    def tikz_drawing_comment(self):
        """Return the comment preceding the Polygon's drawing."""
        output = []
        if self.draw_vertices:
            output.append('% Draw Vertices')
        output.append('% Draw {}'.format(self.type))
        if any([θ.mark_right for θ in self.angles]):
            output.append('\n% Mark right angles')
        return output

    def _tikz_draw_options(self):
        return [self.thickness, self.color]

    def _tikz_draw_vertices(self):
        return '\n'.join([v.tikz_draw()[0] for v in self.vertices]) + '\n'

    def _tikz_draw_sides(self):
        return '\n'.join([s.tikz_draw_section() for s in self.sides[:-1]])

    def _tikz_draw_angles_marks(self):
        marks = '\n'.join([a.tikz_angle_mark()
                          for a in self.angles
                          if a.tikz_angle_mark() != ''])
        if marks == '':
            return ''
        else:
            return '\n' + marks

    def _tikz_draw_right_angles_marks(self):
        return '\n'.join([θ.tikz_rightangle_mark(self.winding)
                          for θ in self.angles
                          if θ.tikz_rightangle_mark(self.winding) != ''])

    def tikz_draw(self):
        """Return the command to actually draw the Polygon."""
        output = []
        if self.draw_vertices:
            output.append(self._tikz_draw_vertices())
        output.append('\draw{} ({})\n{}\n-- cycle{}{}{};'
                      .format(tikz_options_list('draw', self),
                              self.vertices[0].name,
                              self._tikz_draw_sides(),
                              self.sides[-1].tikz_label(),
                              self.sides[-1]._tikz_ls_mark(),
                              self._tikz_draw_angles_marks()))
        if any([θ.mark_right for θ in self.angles]):
            output.append(self._tikz_draw_right_angles_marks())
        return output

    def tikz_points_labels(self):
        """Return the command to write the Points' labels."""
        if self.label_vertices:
            return '\n'.join([v.tikz_label() for v in self.vertices])
        return ''

    def tikz_label(self):
        """Not implemented yet. See issue #4."""
