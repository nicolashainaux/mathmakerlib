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

from math import atan2, degrees

from mathmakerlib import required, config
from mathmakerlib.LaTeX import MATHEMATICAL_NOTATIONS
from mathmakerlib.exceptions import ZeroVector
from mathmakerlib.core.oriented import Oriented
from mathmakerlib.core.oriented import check_winding, shoelace_formula
from mathmakerlib.core.drawable import Colored, HasThickness, HasRadius
from mathmakerlib.core.drawable import Labeled, HasArrowTips
from mathmakerlib.core.drawable import tikz_options_list, Drawable
from mathmakerlib.core.drawable import tikz_approx_position
from mathmakerlib.core.dimensional import Dimensional
from mathmakerlib.geometry.point import Point
from mathmakerlib.geometry.vector import Vector
from mathmakerlib.geometry.bipoint import Bipoint
from mathmakerlib.calculus.number import Number, is_number

AVAILABLE_NAMING_MODES = ['from_endpoints', 'from_armspoints', 'from_vertex']


class AngleDecoration(Labeled, Colored, HasThickness, HasRadius, HasArrowTips):

    def __init__(self, color=None, thickness='thick', label='default',
                 radius=Number('0.25', unit='cm'), variety='single',
                 gap=Number('0.4', unit='cm'), eccentricity='automatic',
                 hatchmark=None, do_draw=True, arrow_tips=None):
        self.do_draw = do_draw
        self.arrow_tips = arrow_tips
        self.color = color
        self.thickness = thickness
        self.label = label
        self.radius = radius
        self.gap = gap
        if gap is None:
            self.gap = None
        else:
            u = self.radius.unit if isinstance(self.radius, Number) else None
            self.gap = Number(gap, unit=u)
        # Eccentricity must be set *after* radius, in order to be able to
        # calculate a reasonable default eccentricity based on the radius
        self.eccentricity = eccentricity
        self.variety = variety
        self.hatchmark = hatchmark

    def __repr__(self):
        return 'AngleDecoration(variety={}; hatchmark={}; label={}; '\
            'color={}; thickness={}; radius={}; eccentricity={})'\
            .format(self.variety, self.hatchmark, self.label, self.color,
                    self.thickness, str(self.radius), self.eccentricity)

    @property
    def do_draw(self):
        return self._do_draw

    @do_draw.setter
    def do_draw(self, value):
        if isinstance(value, bool):
            self._do_draw = value
        else:
            raise TypeError('do_draw must be a boolean; '
                            'got {} instead.'.format(type(value)))

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if is_number(value):
            self._radius = Number(value)
        elif value is None:
            self._radius = None
        else:
            raise TypeError('Expected a number as radius. Got {} instead.'
                            .format(str(type(value))))
        if hasattr(self, '_eccentricity') and hasattr(self, '_gap'):
            self.eccentricity = 'automatic'

    @property
    def eccentricity(self):
        return self._eccentricity

    @eccentricity.setter
    def eccentricity(self, value):
        if value == 'automatic':
            if self.gap is None:
                raise ValueError('Cannot calculate the eccentricity if gap '
                                 'is None.')
            value = (self.gap / self.radius + 1)\
                .rounded(Number('0.01')).standardized()
        if not (value is None or is_number(value)):
            raise TypeError('The eccentricity of an AngleDecoration must be '
                            'None or a Number. Found {} instead.'
                            .format(type(value)))
        self._eccentricity = value

    @property
    def variety(self):
        return self._variety

    @variety.setter
    def variety(self, value):
        if value not in [None, 'single', 'double', 'triple']:
            raise TypeError('AngleDecoration\'s variety can be None, '
                            '\'single\', \'double\' or \'triple\'. '
                            'Found {} instead (type: {}).'
                            .format(repr(value), type(value)))
        self._variety = value

    @property
    def gap(self):
        return self._gap

    @gap.setter
    def gap(self, value):
        if not (is_number(value) or value is None):
            raise TypeError('The gap value must be None or a number. '
                            'Found {} instead (type: {}).'
                            .format(repr(value), type(value)))
        if value is None:
            self._gap = None
        else:
            self._gap = Number(value)

    @property
    def hatchmark(self):
        return self._hatchmark

    @hatchmark.setter
    def hatchmark(self, value):
        if value not in [None, 'singledash', 'doubledash', 'tripledash']:
            raise TypeError('AngleDecoration\'s hatchmark can be None, '
                            '\'singledash\', \'doubledash\' or '
                            '\'tripledash\'. Found {} instead (type: {}).'
                            .format(repr(value), type(value)))
        self._hatchmark = value

    def tikz_attributes(self, radius_coeff=1, do_label=True):
        if not is_number(radius_coeff):
            raise TypeError('radius_coeff must be a number, found {} instead.'
                            .format(type(radius_coeff)))
        attributes = []
        if do_label and self.label not in [None, 'default']:
            required.tikz_library['quotes'] = True
            attributes.append('"{}"'.format(self.label))
            if self.eccentricity is not None:
                attributes.append('angle eccentricity={}'
                                  .format(self.eccentricity))
        if self.variety is not None:
            if self.do_draw:
                attributes.append('draw')
            if self.arrow_tips is not None:
                attributes.append(self.arrow_tips)
            if self.thickness is not None:
                attributes.append(self.thickness)
            if self.radius is not None:
                attributes.append('angle radius = {}'
                                  .format((self.radius * radius_coeff)
                                          .rounded(Number('0.01')).uiprinted))
            if self.hatchmark is not None:
                attributes.append(self.hatchmark)
                required.tikz_library['decorations.markings'] = True
                required.tikzset[self.hatchmark + '_hatchmark'] = True
        if (self.variety is not None
            or (do_label and self.label not in [None, 'default'])):
            if self.color is not None:
                attributes.append(self.color)
        return '[{}]'.format(', '.join(attributes))

    def generate_tikz(self, *points_names):
        if not len(points_names) == 3:
            raise RuntimeError('Three Points\' names must be provided to '
                               'generate the AngleDecoration. Found {} '
                               'arguments instead.'.format(len(points_names)))
        last_layer = {None: 1, 'single': 1, 'double': 2,
                      'triple': 3}[self.variety]
        pic_attr = self.tikz_attributes(do_label=last_layer == 1)
        if pic_attr == '[]':
            return ''
        required.tikz_library['angles'] = True
        deco = ['pic {} {{angle = {}--{}--{}}}'
                .format(pic_attr, *points_names)]
        if self.variety in ['double', 'triple']:
            space_sep = Number('0.16')
            deco.append('pic {} {{angle = {}--{}--{}}}'
                        .format(self.tikz_attributes(
                                radius_coeff=1 + space_sep,
                                do_label=last_layer == 2),
                                *points_names))
            if self.variety == 'triple':
                deco.append('pic {} {{angle = {}--{}--{}}}'
                            .format(self.tikz_attributes(
                                    radius_coeff=1 + 2 * space_sep,
                                    do_label=last_layer == 3),
                                    *points_names))
        return deco


class Angle(Drawable, Oriented, HasThickness, Dimensional):

    def __init__(self, point, vertex, point_or_measure, decoration=None,
                 mark_right=False, second_point_name='auto', label=None,
                 color=None, thickness='thick', armspoints=None,
                 label_vertex=False, draw_vertex=False,
                 label_armspoints=False, draw_armspoints=False,
                 label_endpoints=False, draw_endpoints=False,
                 naming_mode='from_endpoints', decoration2=None):
        """
        :param point: a Point of an arm of the Angle
        :type point: Point
        :param vertex: the Angle's vertex
        :type vertex: Point
        :param point_or_measure: either a Point of the other arm of the Angle,
        or the measure of the Angle
        :type point_or_measure: Point or number
        :param decoration: the decoration of the Angle
        :type decoration: None or AngleDecoration
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
        :param naming_mode: how to build the name. Possible modes are:
        'from_endpoints', 'from_armspoints', 'from_vertex'. Note that if no
        armspoints are defined, then trying to get the Angle.name will raise an
        error
        :type naming_mode: str
        """
        self.color = color
        self.thickness = thickness
        self.naming_mode = naming_mode
        self.decoration = decoration
        self.decoration2 = decoration2
        # The label must be set *after* the possible decoration, because it
        # will actually be handled by self.decoration
        if (self.decoration is None
            or self.decoration.label in [None, 'default']):
            self.label = label
        else:
            if label is not None:
                raise ValueError('The label has been set twice, as Angle\'s '
                                 'keyword argument ({}) and as its '
                                 'AngleDecoration\'s keyword argument ({}).'
                                 .format(repr(label),
                                         repr(self.decoration.label_value)))
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

        if any([p.three_dimensional for p in self._points]):
            self._three_dimensional = True
        else:
            self._three_dimensional = False

        # Measure of the angle:
        if self._three_dimensional:
            u = Vector(self.points[1], self.points[0])
            v = Vector(self.points[1], self.points[2])
            self._measure = Number(str(degrees(atan2(u.cross(v).length,
                                                     u.dot(v)))))
        else:  # 2D angles measure
            p0 = Point(self._points[0].x - self._points[1].x,
                       self._points[0].y - self._points[1].y,
                       None)
            p2 = Point(self._points[2].x - self._points[1].x,
                       self._points[2].y - self._points[1].y,
                       None)
            α0 = Number(str(degrees(atan2(p0.y, p0.x))))
            α2 = Number(str(degrees(atan2(p2.y, p2.x))))
            self._measure = α2 - α0

        if self._measure < 0:
            self._measure += 360

        # This is not like the matching Triangle!
        if shoelace_formula(*self.points) > 0:
            self.winding = 'clockwise'
        else:
            self.winding = 'anticlockwise'

        arm0 = Bipoint(self._points[1], self._points[0])
        arm1 = Bipoint(self._points[1], self._points[2])
        self._arms = [arm0, arm1]
        self.armspoints = armspoints

        # Only 2D: labels positioning
        if not self.three_dimensional:
            # Vertex' label positioning
            bisector = Vector(self._points[0], self.vertex)\
                .bisector(Vector(self._points[2], self.vertex),
                          new_endpoint_name=None)
            try:
                self._points[1].label_position = \
                    tikz_approx_position(bisector.slope360)
            except ZeroVector:
                self._points[1].label_position = \
                    tikz_approx_position(
                        Bipoint(self.vertex,
                                self._points[0].rotate(self.vertex, -90,
                                                       rename=None)
                                ).slope360)

            # Endpoints labels positioning
            direction = 1 if self.winding == 'anticlockwise' else -1
            self.endpoints[0].label_position = \
                tikz_approx_position(arm0.slope360 - direction * 55)
            self.endpoints[1].label_position = \
                tikz_approx_position(arm1.slope360 + direction * 55)

    def __repr__(self):
        return 'Angle({}, {}, {})'\
            .format(self.points[0].name, self.points[1].name,
                    self.points[2].name)

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
                position = config.angles.DEFAULT_ARMSPOINTS_POSITION
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
                                     + xdir * direction * 60)

    @property
    def arms(self):
        return self._arms

    @property
    def measure(self):
        """Measure of the Angle."""
        return self._measure

    @property
    def label(self):
        """
        The label of an Angle is handled internally by its AngleDecoration.
        """
        if hasattr(self, '_decoration') and self.decoration is not None:
            return self.decoration.label
        else:
            return None

    @label.setter
    def label(self, value):
        """
        The label of an Angle is handled internally by its AngleDecoration.
        """
        if self.decoration is None:
            self.decoration = AngleDecoration(variety=None, label=value)
        else:
            self.decoration.label = value

    @property
    def decoration(self):
        return self._decoration

    @decoration.setter
    def decoration(self, deco):
        if not (deco is None or isinstance(deco, AngleDecoration)):
            raise TypeError('An angle decoration must be None or belong to '
                            'the AngleDecoration class. Got {} instead.'
                            .format(type(deco)))
        if deco is None:
            if not hasattr(self, '_decoration') or self.label is None:
                self._decoration = None
            else:
                self._decoration = AngleDecoration(variety=None,
                                                   label=self.label)
        else:  # deco is an AngleDecoration
            # If the label has been set prior to an additional decoration,
            # keep it:
            if deco.label == 'default':
                deco.label = self.label
            self._decoration = deco

    @property
    def decoration2(self):
        return self._decoration2

    @decoration2.setter
    def decoration2(self, deco):
        if not (deco is None or isinstance(deco, AngleDecoration)):
            raise TypeError('An angle decoration must be None or belong to '
                            'the AngleDecoration class. Got {} instead.'
                            .format(type(deco)))
        self._decoration2 = deco

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

    @property
    def naming_mode(self):
        return self._naming_mode

    @naming_mode.setter
    def naming_mode(self, value):
        if value not in AVAILABLE_NAMING_MODES:
            raise ValueError('naming_mode must belong to {}. Found {} instead.'
                             .format(AVAILABLE_NAMING_MODES, repr(value)))
        self._naming_mode = value

    @property
    def name(self):
        loc = None
        for lg in ['fr', 'en']:
            if config.language.startswith(lg):
                loc = lg
        if self.naming_mode == 'from_endpoints':
            content = '{}{}{}'.format(self.endpoints[0].name,
                                      self.vertex.name,
                                      self.endpoints[1].name)
        elif self.naming_mode == 'from_armspoints':
            if not self.armspoints:
                raise RuntimeError('The naming mode of this Angle is '
                                   '\'from_armspoints\' but the armspoints '
                                   'are not defined (empty list).')
            content = '{}{}{}'.format(self.armspoints[0].name,
                                      self.vertex.name,
                                      self.armspoints[1].name)
        elif self.naming_mode == 'from_vertex':
            content = self.vertex.name
        _name = MATHEMATICAL_NOTATIONS[loc]['angle_name']\
            .format(content=content)
        if 'stackon' in _name:
            required.package['stackengine'] = True
        if 'hstretch' in _name or 'vstretch' in _name:
            required.package['scalerel'] = True
        return _name

    def tikz_decorations(self):
        output_elements = []
        if not(self.decoration is None
               or (self.mark_right and self.label is None)):
            output_elements = \
                self.decoration.generate_tikz(self.points[0].name,
                                              self.vertex.name,
                                              self.points[2].name)
        if self.decoration2 is not None:
            output_elements += \
                self.decoration2.generate_tikz(self.points[0].name,
                                               self.vertex.name,
                                               self.points[2].name)
        return '\n'.join(output_elements)

    def tikz_rightangle_mark(self, winding='anticlockwise'):
        if self.decoration is None or not self.mark_right:
            return ''
        check_winding(winding)
        # Decimal numbers in TikZ must be written with a dot as decimal point.
        # As of now, there is no reliable way to temporarily change the
        # locale to 'C' (or 'en_US'), so here's a little patch that will
        # replace possibly other decimal points by a '.'.
        theta = Bipoint(self.vertex, self.points[0])\
            .slope.rounded(Number('0.01')).imprint(dot=True)
        rt = 'cm={{cos({θ}), sin({θ}), -sin({θ}), cos({θ}), ({v})}}' \
            .format(θ=theta, v=self.vertex.name)
        draw_options = tikz_options_list([self.decoration.thickness,
                                          self.decoration.color,
                                          rt])
        if winding == 'anticlockwise':
            rightangle_shape = '({R}, 0) -- ({R}, {R}) -- (0, {R})'\
                .format(R=self.decoration.radius.uiprinted)
        elif winding == 'clockwise':
            rightangle_shape = '({R}, 0) -- ({R}, -{R}) -- (0, -{R})'\
                .format(R=self.decoration.radius.uiprinted)
        return r'\draw' + '{} {};'.format(draw_options, rightangle_shape)

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
        if self.mark_right:
            comments.append('\n% Mark right angle')
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
        decoration = self.tikz_decorations()
        if decoration != '':
            decoration = '\n' + decoration
        commands = [r'\draw' + '{} ({}) -- ({}) -- ({}){};'
                    .format(tikz_options_list('draw', self),
                            *[p.name for p in self.points],
                            decoration)
                    ]
        if self.draw_vertex:
            commands.append(self._tikz_draw_vertex())
        if self.draw_armspoints and len(self.armspoints):
            commands.append(self._tikz_draw_armspoints())
        if self.draw_endpoints:
            commands.append(self._tikz_draw_endpoints())
        if self.mark_right:
            commands.append(self.tikz_rightangle_mark())
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
                               .format('; '.join([str(p) for p in points])))
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
        if any([θ.mark_right for θ in self.angles]):
            comments.append('% Mark right Angles')
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

    def _tikz_draw_right_angles_marks(self):
        return '\n'.join([θ.tikz_rightangle_mark(θ.winding)
                          for θ in self.angles
                          if θ.tikz_rightangle_mark(θ.winding) != ''])

    def tikz_draw(self):
        """
        Return the commands to actually draw the Angles.

        :rtype: list
        """
        angles_cmd = []
        for α in self.angles:
            decoration = α.tikz_decorations()
            if decoration != '':
                decoration = '\n' + decoration
            angles_cmd.append(r'\draw' + '{} ({}) -- ({}) -- ({}){};'
                              .format(tikz_options_list('draw', α),
                                      *[p.name for p in α.points],
                                      decoration))
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

        if any([θ.mark_right for θ in self.angles]):
            commands.append(self._tikz_draw_right_angles_marks())

        return commands
