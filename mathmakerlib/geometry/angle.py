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

import sys
from math import acos, degrees

from mathmakerlib import required, mmlib_setup
from mathmakerlib.core.oriented import check_winding, shoelace_formula
from mathmakerlib.core.drawable import Colored, HasThickness, HasRadius
from mathmakerlib.core.drawable import tikz_options_list, Drawable
from mathmakerlib.core.drawable import tikz_approx_position
from mathmakerlib.geometry.point import Point
from mathmakerlib.geometry.pointspair import PointsPair
from mathmakerlib.geometry.vector import Vector
from mathmakerlib.calculus.number import Number, is_number

LOCALE_US = 'en' if sys.platform.startswith('win') else 'en_US.UTF-8'


class AngleMark(Colored, HasThickness, HasRadius):

    def __init__(self, color=None, thickness='thick',
                 radius=Number('0.25', unit='cm'), variety='single',
                 decoration=None):
        self.color = color
        self.thickness = thickness
        self.radius = radius
        self.variety = variety
        self.decoration = decoration

    @property
    def variety(self):
        return self._variety

    @variety.setter
    def variety(self, value):
        if value not in ['single', 'double', 'triple']:
            raise TypeError('AngleMark\'s variety can be \'single\', '
                            '\'double\' or \'triple\'. Found {} instead ('
                            'type: {}).'
                            .format(repr(value), type(value)))
        self._variety = value

    @property
    def decoration(self):
        return self._decoration

    @decoration.setter
    def decoration(self, value):
        if value not in [None, 'singledash', 'doubledash', 'tripledash']:
            raise TypeError('AngleMark\'s decoration can be None, '
                            '\'singledash\', \'doubledash\' or '
                            '\'tripledash\'. Found {} instead (type: {}).'
                            .format(repr(value), type(value)))
        self._decoration = value

    def tikz_mark_attributes(self, radius_coeff=1, label=None,
                             eccentricity=None):
        if not is_number(radius_coeff):
            raise TypeError('radius_coeff must be a number, found {} instead.'
                            .format(type(radius_coeff)))
        attributes = []
        if label is not None:
            attributes.append('"{}"'.format(label))
            if eccentricity is not None:
                attributes.append('angle eccentricity={}'.format(eccentricity))
        attributes.append('draw')
        for attr in [self.decoration, self.color, self.thickness]:
            if attr is not None:
                attributes.append(attr)
        if self.decoration is not None:
            required.tikz_library['decorations.markings'] = True
            required.tikzset[self.decoration + '_decoration'] = True
        if self.radius is not None:
            attributes.append('angle radius = {}'
                              .format((self.radius * radius_coeff)
                                      .standardized().uiprinted))
        return '[{}]'.format(', '.join(attributes))


class Angle(Drawable, HasThickness):

    def __init__(self, point, vertex, point_or_measure, mark=None,
                 mark_right=False, second_point_name='auto', label=None,
                 color=None, thickness='thick', armspoints=None,
                 eccentricity=Number('2.15'),
                 label_vertex=False, draw_vertex=False,
                 label_armspoints=False, draw_armspoints=False,
                 label_endpoints=False, draw_endpoints=False,):
        """
        :param point: a Point of an arm of the Angle
        :type point: Point
        :param vertex: the Angle's vertex
        :type vertex: Point
        :param point_or_measure: either a Point of the other arm of the Angle,
        or the measure of the Angle
        :type point_or_measure: Point or number
        :param mark: the mark of the Angle
        :type mark: None or AngleMark
        :param mark_right: to tell whether to mark the angle as a right angle
        :type mark_right: bool
        :param second_point_name: Only used if point_or_measure is a measure,
        this is the name of the 2d arm's Point. If set to 'auto', then the name
        of the first Point will be used, concatenated to a '.
        :type second_point_name: str
        :param thickness: the Angle's arms' thickness. Available values are
        TikZ's ones.
        :type thickness: str
        :param color: the color of the Angle's arms.
        :type color: str
        """
        self.color = color
        self.label = label
        self.eccentricity = eccentricity
        self.thickness = thickness
        self.mark = mark
        self.mark_right = mark_right
        self.label_vertex = label_vertex
        self.label_endpoints = label_endpoints
        self.draw_endpoints = draw_endpoints
        self.label_armspoints = label_armspoints
        self.draw_armspoints = draw_armspoints
        self.draw_vertex = draw_vertex
        if not (isinstance(point, Point)
                and isinstance(vertex, Point)
                and (isinstance(point_or_measure, Point)
                     or is_number(point_or_measure))):
            raise TypeError('Three Points, or two Points and the measure of '
                            'the angle are required to build an Angle. '
                            'Found instead: {}, {} and {}.'
                            .format(type(point), type(vertex),
                                    type(point_or_measure)))
        self._points = [point, vertex]
        if isinstance(point_or_measure, Point):
            self._points.append(point_or_measure)
        else:
            self._points.append(point.rotate(vertex, point_or_measure,
                                             rename=second_point_name))
        # Measure of the angle:
        arm0 = PointsPair(self._points[1], self._points[0])
        arm1 = PointsPair(self._points[1], self._points[2])
        pp2 = PointsPair(self._points[2], self._points[0])
        n = arm0.length ** 2 + arm1.length ** 2 - pp2.length ** 2
        d = 2 * arm0.length * arm1.length
        self._measure = Number(str(degrees(acos(n / d))))

        # This is not like the matching Triangle!
        if shoelace_formula(*self.points) > 0:
            self.winding = 'clockwise'
        else:
            self.winding = 'anticlockwise'

        self._arms = [arm0, arm1]
        self.armspoints = armspoints

        # Vertex' label positioning
        bisector = Vector(self._points[0], self.vertex)\
            .bisector_vector(Vector(self._points[2], self.vertex))
        self._points[1].label_position = \
            tikz_approx_position(bisector.slope360)

        # Endpoints labels positioning
        direction = 1 if self.winding == 'anticlockwise' else -1
        self.endpoints[0].label_position = \
            tikz_approx_position(arm0.slope360 - direction * 55)
        self.endpoints[1].label_position = \
            tikz_approx_position(arm1.slope360 + direction * 55)

    @property
    def vertex(self):
        return self._points[1]

    @property
    def points(self):
        return self._points

    @property
    def endpoints(self):
        return [self._points[0], self._points[2]]

    @property
    def armspoints(self):
        return self._armspoints

    @armspoints.setter
    def armspoints(self, value):
        self._armspoints = []
        if value is None:
            value = []
        if not isinstance(value, list):
            raise TypeError('A list must be provided to setup armspoints. '
                            'Found {} instead.'.format(type(value)))
        if len(value) > len(self.arms):
            raise ValueError('More values are provided ({}) then available '
                             'arms ({}).'.format(len(value), len(self.arms)))
        for i, p in enumerate(value):
            if not isinstance(p, tuple):
                raise TypeError('Each arm\'s point must be defined by a '
                                'tuple. Found {} instead.'.format(type(p)))
            if len(p) > 2:
                raise TypeError('Each arm\'s point must be defined by a '
                                'tuple of 1 or 2 elements. '
                                'Found {} elements instead.'.format(len(p)))
            if p[0] in [None, '']:
                name = 'automatic'
            else:
                name = p[0]
            try:
                position = p[1]
            except IndexError:
                position = mmlib_setup.angles.DEFAULT_ARMSPOINTS_POSITION
            self._armspoints.append(self.arms[i].point_at(position, name))
        if len(self._armspoints):
            self.label_armspoints = True
            self.draw_armspoints = True

        # Armspoints labels positioning
        direction = 1 if self.winding == 'anticlockwise' else -1
        for i, ap in enumerate(self.armspoints):
            xdir = -1 if i == 0 else 1
            self.armspoints[i].label_position = \
                tikz_approx_position(self.arms[i].slope360
                                     + xdir * direction * 55)

    @property
    def arms(self):
        return self._arms

    @property
    def measure(self):
        """Measure of the Angle."""
        return self._measure

    @property
    def eccentricity(self):
        return self._eccentricity

    @eccentricity.setter
    def eccentricity(self, value):
        if not is_number(value):
            raise TypeError('The eccentricity of an Angle must be a Number. '
                            'Found {} instead.'.format(type(value)))
        self._eccentricity = value

    @property
    def mark(self):
        return self._mark

    @mark.setter
    def mark(self, value):
        if not (value is None or isinstance(value, AngleMark)):
            raise TypeError('An angle mark must belong to the AngleMark class.'
                            ' Got {} instead.'.format(type(value)))
        self._mark = value

    @property
    def mark_right(self):
        return self._mark_right

    @mark_right.setter
    def mark_right(self, value):
        if not isinstance(value, bool):
            raise TypeError('\'mark_right\' must be a boolean')
        self._mark_right = value

    @property
    def draw_vertex(self):
        return self._draw_vertex

    @draw_vertex.setter
    def draw_vertex(self, value):
        if isinstance(value, bool):
            self._draw_vertex = value
        else:
            raise TypeError('draw_vertex must be a boolean; '
                            'got {} instead.'.format(type(value)))

    @property
    def draw_endpoints(self):
        return self._draw_endpoints

    @draw_endpoints.setter
    def draw_endpoints(self, value):
        if isinstance(value, bool):
            self._draw_endpoints = value
        else:
            raise TypeError('draw_endpoints must be a boolean; '
                            'got {} instead.'.format(type(value)))

    @property
    def draw_armspoints(self):
        return self._draw_armspoints

    @draw_armspoints.setter
    def draw_armspoints(self, value):
        if isinstance(value, bool):
            self._draw_armspoints = value
        else:
            raise TypeError('draw_armspoints must be a boolean; '
                            'got {} instead.'.format(type(value)))

    @property
    def label_vertex(self):
        return self._label_vertex

    @label_vertex.setter
    def label_vertex(self, value):
        if isinstance(value, bool):
            self._label_vertex = value
        else:
            raise TypeError('label_vertex must be a boolean; '
                            'got {} instead.'.format(type(value)))

    @property
    def label_endpoints(self):
        return self._label_endpoints

    @label_endpoints.setter
    def label_endpoints(self, value):
        if isinstance(value, bool):
            self._label_endpoints = value
        else:
            raise TypeError('label_endpoints must be a boolean; '
                            'got {} instead.'.format(type(value)))

    @property
    def label_armspoints(self):
        return self._label_armspoints

    @label_armspoints.setter
    def label_armspoints(self, value):
        if isinstance(value, bool):
            self._label_armspoints = value
        else:
            raise TypeError('label_armspoints must be a boolean; '
                            'got {} instead.'.format(type(value)))

    def tikz_angle_mark_and_label(self):
        if (self.mark is None or self.mark_right) and self.label is None:
            return ''
        required.tikz_library['angles'] = True
        if self.mark is None or self.mark_right:
            mark_and_or_label = '["{}", angle eccentricity={}]'\
                .format(self.label, self.eccentricity)
        else:
            mark_and_or_label = self.mark.tikz_mark_attributes(
                label=self.label, eccentricity=self.eccentricity)
        marks = ['pic {} {{angle = {}--{}--{}}}'
                 .format(mark_and_or_label,
                         self.points[0].name,
                         self.vertex.name,
                         self.points[2].name)]
        if self.mark is not None:
            space_sep = Number('0.16')
            if self.mark.variety in ['double', 'triple']:
                marks.append('pic {} {{angle = {}--{}--{}}}'
                             .format(self.mark.tikz_mark_attributes(
                                     radius_coeff=1 + space_sep),
                                     self.points[0].name,
                                     self.vertex.name,
                                     self.points[2].name))
            if self.mark.variety == 'triple':
                marks.append('pic {} {{angle = {}--{}--{}}}'
                             .format(self.mark.tikz_mark_attributes(
                                     radius_coeff=1 + 2 * space_sep),
                                     self.points[0].name,
                                     self.vertex.name,
                                     self.points[2].name))
        return '\n'.join(marks)

    def tikz_rightangle_mark(self, winding='anticlockwise'):
        if self.mark is None or not self.mark_right:
            return ''
        check_winding(winding)
        rt = 'cm={{cos({θ}), sin({θ}), -sin({θ}), cos({θ}), ({v})}}' \
            .format(θ=PointsPair(self.vertex, self.points[0])
                    .slope.imprint(mod_locale=LOCALE_US),
                    v=self.vertex.name)
        draw_options = tikz_options_list([self.mark.thickness,
                                          self.mark.color,
                                          rt])
        if winding == 'anticlockwise':
            rightangle_shape = '({R}, 0) -- ({R}, {R}) -- (0, {R})'\
                .format(R=self.mark.radius.uiprinted)
        elif winding == 'clockwise':
            rightangle_shape = '({R}, 0) -- ({R}, -{R}) -- (0, -{R})'\
                .format(R=self.mark.radius.uiprinted)
        return '\draw{} {};'.format(draw_options, rightangle_shape)

    def tikz_declarations(self):
        """Return the Points declarations."""
        points = self.points
        if len(self.armspoints):
            points = points + self.armspoints
        return '\n'.join([v.tikz_declarations() for v in points])

    def _tikz_draw_options(self):
        """
        The list of possible options for draw command.

        :rtype: list
        """
        return [self.thickness, self.color]

    def _tikz_draw_vertex(self):
        return self.vertex.tikz_draw()[0]

    def _tikz_draw_armspoints(self, nb=None):
        if nb is None:
            nb = [n for n in range(len(self.armspoints))]
        return '\n'.join([self.armspoints[n].tikz_draw()[0] for n in nb])

    def _tikz_draw_endpoints(self, nb=None):
        if nb is None:
            nb = [0, 1]
        return '\n'.join([self.endpoints[n].tikz_draw()[0] for n in nb])

    def tikz_drawing_comment(self):
        """
        Return the comments matching each drawing category.

        :rtype: list
        """
        comments = ['% Draw Angle']
        if self.draw_vertex:
            comments.append('% Draw Vertex')
        if self.draw_armspoints and len(self.armspoints):
            comments.append('% Draw Arms\' Points')
        if self.draw_endpoints:
            comments.append('% Draw End Points')
        return comments

    def tikz_draw(self):
        """
        Return the commands to actually draw the object.

        If enabled, the vertex is drawn;
        if enabled the end Points are drawn;
        if enabled the arms' Points are drawn.
        The Angle is always drawn.

        :rtype: list
        """
        mark_and_label = self.tikz_angle_mark_and_label()
        if mark_and_label != '':
            mark_and_label = '\n' + mark_and_label
        commands = ['\draw{} ({}) -- ({}) -- ({}){};'
                    .format(tikz_options_list('draw', self),
                            *[p.name for p in self.points],
                            mark_and_label)
                    ]
        if self.draw_vertex:
            commands.append(self._tikz_draw_vertex())
        if self.draw_armspoints and len(self.armspoints):
            commands.append(self._tikz_draw_armspoints())
        if self.draw_endpoints:
            commands.append(self._tikz_draw_endpoints())
        return commands

    def tikz_label(self):
        """The Angle's label is included in its draw command."""

    def tikz_points_labels(self):
        """Return the command to write the object's points' labels."""
        labels = []
        if self.label_vertex:
            labels.append(self.vertex.tikz_label())
        if self.label_endpoints:
            labels.append(self.endpoints[0].tikz_label())
            labels.append(self.endpoints[1].tikz_label())
        if self.label_armspoints:
            labels.append(self.armspoints[0].tikz_label())
            labels.append(self.armspoints[1].tikz_label())
        return '\n'.join(labels)


class AnglesSet(Drawable):

    def __init__(self, *angles):
        self.angles = angles

    @property
    def angles(self):
        return self._angles

    @angles.setter
    def angles(self, angles):
        for α in angles:
            if not isinstance(α, Angle):
                raise TypeError('Any element of an AnglesSet must be an '
                                'Angle. Found {} instead.'.format(type(α)))
        self._angles = angles

    def tikz_declarations(self):
        """
        Return the necessary declarations (e.g. Points declarations).

        :rtype: str
        """
        points = []
        for α in self.angles:
            if α.vertex not in points:
                points.append(α.vertex)
            for p in α.endpoints:
                if p not in points:
                    points.append(p)
            for p in α.armspoints:
                if p not in points:
                    if α.draw_armspoints or α.label_armspoints:
                        points.append(p)
        points_names = [p.name for p in points]
        if len(points_names) != len(set(points_names)):
            raise RuntimeError('Two different Points have been provided the '
                               'same name in this list: {}'
                               .format(';'.join([str(p) for p in points])))
        return '\n'.join([p.tikz_declarations() for p in points])

    def _tikz_draw_options(self):
        """
        Each Angle will have its own options, so nothing to return.

        :rtype: list
        """
        return []

    def tikz_drawing_comment(self):
        """
        Return the comments matching each drawing category.

        :rtype: list
        """
        comments = ['% Draw Angles']
        vertices_to_draw = len([α.draw_vertex
                                for α in self.angles if α.draw_vertex])
        if vertices_to_draw:
            if vertices_to_draw == 1:
                comments.append('% Draw Vertex')
            else:
                comments.append('% Draw Vertices')
        if any([α.draw_armspoints and len(α.armspoints)
                for α in self.angles]):
            comments.append('% Draw Arms\' Points')
        if any([α.draw_endpoints for α in self.angles]):
            comments.append('% Draw End Points')
        return comments

    def tikz_label(self):
        """All labels are included in the Angles' draw commands."""

    def tikz_points_labels(self):
        """Return the command to write the Angles' points' labels."""
        labels = []
        labeled_points_names = []
        for α in self.angles:
            if α.label_vertex and α.vertex.name not in labeled_points_names:
                labels.append(α.vertex.tikz_label())
                labeled_points_names.append(α.vertex.name)
            if α.label_endpoints:
                for p in α.endpoints:
                    if p.name not in labeled_points_names:
                        labels.append(p.tikz_label())
                        labeled_points_names.append(p.name)
            if α.label_armspoints:
                for p in α.armspoints:
                    if p.name not in labeled_points_names:
                        labels.append(p.tikz_label())
                        labeled_points_names.append(p.name)
        return '\n'.join(labels)

    def tikz_draw(self):
        """
        Return the commands to actually draw the Angles.

        :rtype: list
        """
        angles_cmd = []
        for α in self.angles:
            mark_and_label = α.tikz_angle_mark_and_label()
            if mark_and_label != '':
                mark_and_label = '\n' + mark_and_label
            angles_cmd.append('\draw{} ({}) -- ({}) -- ({}){};'
                              .format(tikz_options_list('draw', α),
                                      *[p.name for p in α.points],
                                      mark_and_label))
        commands = ['\n'.join(angles_cmd)]

        labeled_points_names = []
        vertices_cmd = []
        for α in self.angles:
            if α.draw_vertex and α.vertex.name not in labeled_points_names:
                vertices_cmd.append(α._tikz_draw_vertex())
                labeled_points_names.append(α.vertex.name)
        vertices_cmd = '\n'.join(vertices_cmd)
        if vertices_cmd != '':
            commands.append(vertices_cmd)

        armspoints_cmd = []
        for α in self.angles:
            if α.draw_armspoints and len(α.armspoints):
                nb = []
                for i, p in enumerate(α.armspoints):
                    if p.name not in labeled_points_names:
                        nb.append(i)
                        labeled_points_names.append(p.name)
                armspoints_cmd.append(α._tikz_draw_armspoints(nb=nb))
        armspoints_cmd = '\n'.join(armspoints_cmd)
        if armspoints_cmd != '':
            commands.append(armspoints_cmd)

        endpoints_cmd = []
        for α in self.angles:
            if α.draw_endpoints and len(α.endpoints):
                nb = []
                for i, p in enumerate(α.endpoints):
                    if p.name not in labeled_points_names:
                        nb.append(i)
                        labeled_points_names.append(p.name)
                endpoints_cmd.append(α._tikz_draw_endpoints(nb=nb))
        endpoints_cmd = '\n'.join(endpoints_cmd)
        if endpoints_cmd != '':
            commands.append(endpoints_cmd)

        return commands
