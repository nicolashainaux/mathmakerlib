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

import math
import warnings

from mathmakerlib.core.drawable import Drawable
from mathmakerlib.calculus.number import Number
from mathmakerlib.geometry.point import Point, OPPOSITE_LABEL_POSITIONS

THICKNESS_VALUES = [None, '', 'thin', 'very thin', 'ultra thin', 'thick',
                    'very thick', 'ultra thick']
LABEL_MASK_VALUES = [None, '', '?']


class LineSegment(Drawable):

    def __init__(self, *points, thickness=None, label=None, label_mask=None,
                 label_position='anticlockwise',
                 draw_endpoints=True, label_endpoints=True):
        """
        Initialize LineSegment

        :param points: either one LineSegment to copy, or two Points
        :type points: another LineSegment or a list or tuple of two Points
        :param thickness: the LineSegment's thickness. Available values are
        TikZ's ones.
        :type thickness: str
        :param label: what will be written along the LineSegment, about its
        middle. The default value will leave the label blank.
        :type label: None or str
        :param label_mask: if not None, hide the label with nothing or with a
        '?'
        :type label_mask: None or '' or '?'
        :param label_position: tells where to put the LineSegment's label.
        Can be a value used by TikZ or 'clockwise' or 'anticlockwise'.
        'anticlockwise' (default) will automatically set the label_position to
        'above' if deltax < 0 and to 'below' if deltax > 0. This is useful to
        put all LineSegments' labels outside a Polygon that is drawn in an
        anticlockwise manner. Same for 'clockwise', in the reversed direction.
        :type label_position: str
        :param draw_endpoints: whether or not actually draw the endpoints.
        Defaults to True.
        :type draw_endpoints: bool
        :param label_endpoints: whether or not label the endpoints.
        Defaults to True.
        :type label_endpoints: bool
        """
        if len(points) == 1:
            if not isinstance(points[0], LineSegment):
                raise TypeError('If only one argument is provided, it must '
                                'be another LineSegment. Got a {} instead.'
                                .format(type(points)))
            if label is not None or thickness is not None:
                warnings.warn('LineSegment copy: ignoring parameter (label '
                              'or thickness).')
            ls = points[0]
            LineSegment.__init__(self, ls.endpoints[0], ls.endpoints[1],
                                 label=ls.label, thickness=ls.thickness,
                                 label_mask=ls.label_mask,
                                 draw_endpoints=ls.draw_endpoints,
                                 label_endpoints=ls.label_endpoints)
        elif len(points) == 2:
            if not isinstance(points[0], Point):
                raise TypeError('Both arguments should be Points, got a {} '
                                'as first argument instead.'
                                .format(type(points[0])))
            if not isinstance(points[1], Point):
                raise TypeError('Both arguments should be Points, got a {} '
                                'as second argument instead.'
                                .format(type(points[1])))
            if points[0].coordinates == points[1].coordinates:
                raise ValueError('Cannot instantiate a LineSegment if both '
                                 'endpoints have the same coordinates: '
                                 '({}; {}).'.format(points[0].x, points[0].y))
            self._endpoints = [Point(points[0]), Point(points[1])]
            self._label = None
            self._thickness = None
            self._label_mask = None
            self._label_position = None
            self._draw_endpoints = None
            self._label_endpoints = None
            self.label = label
            self.label_mask = label_mask
            if thickness is None:
                thickness = 'thick'
            self.thickness = thickness
            self.draw_endpoints = draw_endpoints
            self.label_endpoints = label_endpoints
            self._deltax = self.endpoints[1].x - self.endpoints[0].x
            self._deltay = self.endpoints[1].y - self.endpoints[0].y
            s = self.slope
            if (Number('337.5') <= s <= Number('360')
                or Number('0') <= s < Number('22.5')):
                self.endpoints[1].label_position = 'right'
            elif Number('22.5') <= s < Number('67.5'):
                self.endpoints[1].label_position = 'above right'
            elif Number('67.5') <= s < Number('112.5'):
                self.endpoints[1].label_position = 'above'
            elif Number('112.5') <= s < Number('157.5'):
                self.endpoints[1].label_position = 'above left'
            elif Number('157.5') <= s < Number('202.5'):
                self.endpoints[1].label_position = 'left'
            elif Number('202.5') <= s < Number('247.5'):
                self.endpoints[1].label_position = 'below left'
            elif Number('247.5') <= s < Number('292.5'):
                self.endpoints[1].label_position = 'below'
            elif Number('292.5') <= s < Number('337.5'):
                self.endpoints[1].label_position = 'below right'
            self.endpoints[0].label_position = \
                OPPOSITE_LABEL_POSITIONS[self.endpoints[1].label_position]
            if label_position == 'anticlockwise':
                if self.deltax > 0:
                    self.label_position = 'below'
                else:
                    self.label_position = 'above'
            elif label_position == 'clockwise':
                if self.deltax > 0:
                    self.label_position = 'above'
                else:
                    self.label_position = 'below'
            else:
                self.label_position = label_position
        else:
            raise ValueError('One LineSegment, or two Points are required to '
                             'create a LineSegment. Got {} objects instead.'
                             .format(len(points)))

    def __repr__(self):
        return 'LineSegment({}, {})'.format(repr(self.endpoints[0]),
                                            repr(self.endpoints[1]))

    def __eq__(self, other):
        if isinstance(other, LineSegment):
            return (self.endpoints[0] == other.endpoints[0]
                    and self.endpoints[1] == other.endpoints[1])
        else:
            return False

    def __ne__(self, other):
        if isinstance(other, LineSegment):
            return (self.endpoints[0] != other.endpoints[0]
                    or self.endpoints[1] != other.endpoints[1])
        else:
            return True

    @property
    def deltax(self):
        return self._deltax

    @property
    def deltay(self):
        return self._deltay

    @property
    def draw_endpoints(self):
        return self._draw_endpoints

    @draw_endpoints.setter
    def draw_endpoints(self, value):
        if value in [True, False]:
            self._draw_endpoints = value
        else:
            raise ValueError('draw_endpoints must be True or False; '
                             'got \'{}\' instead.'.format(value))

    @property
    def endpoints(self):
        return self._endpoints

    # @property
    # def name(self):
    #     return '[' + self.endpoints[0].name + self.endpoints[1].name + ']'

    @property
    def label_endpoints(self):
        return self._label_endpoints

    @label_endpoints.setter
    def label_endpoints(self, value):
        if value in [True, False]:
            self._label_endpoints = value
        else:
            raise ValueError('label_endpoints must be True or False; '
                             'got \'{}\' instead.'.format(value))

    @property
    def label_mask(self):
        return self._label_mask

    @label_mask.setter
    def label_mask(self, value):
        if value in LABEL_MASK_VALUES:
            self._label_mask = value
        else:
            raise ValueError('label_mask must be in {}; got \'{}\' instead.'
                             .format(LABEL_MASK_VALUES, value))

    @property
    def label_position(self):
        return self._label_position

    @label_position.setter
    def label_position(self, value):
        self._label_position = str(value)

    @property
    def length(self):
        """LineSegment's length."""
        return Number(self.deltax ** 2 + self.deltay ** 2).sqrt()

    # The automatic naming of the midpoint is a problem.
    # It will require to add a mean to generate new points names automatically.
    # With same convention as in geogebra for instance: A, B, C... A_1, B_1,...
    # @property
    # def midpoint(self):
    #     """LineSegment's midpoint."""
    #     return Point('M',
    #                  (self.endpoints[0].x + self.endpoints[1].x) / 2,
    #                  (self.endpoints[0].y + self.endpoints[1].y) / 2)

    @property
    def slope(self):
        """LineSegment's slope."""
        theta = Number(str(math.degrees(math.acos(self.deltax / self.length))))
        return theta if self.deltay >= 0 else Number('360') - theta

    def tikz_declarations(self):
        """Return the LineSegment's Points' declarations."""
        return '{}\n{}'\
            .format(self.endpoints[0].tikz_declarations(),
                    self.endpoints[1].tikz_declarations())

    def tikz_drawing_comment(self):
        """Return the comments preceding the LineSegment's drawings."""
        if self.draw_endpoints:
            return ['% Draw Points', '% Draw LineSegment']
        else:
            return ['% Draw LineSegment']

    def tikz_draw(self):
        """Return the command to actually draw the LineSegment."""
        output = []
        if self.draw_endpoints:
            output.append('{}\n{}\n'
                          .format(self.endpoints[0].tikz_draw()[0],
                                  self.endpoints[1].tikz_draw()[0]))
        if self.thickness is None:
            thickness = ''
        else:
            thickness = '[{}]'.format(self.thickness)
        lslabel = ''
        if self.label_mask is None:
            if self.label is not None:
                lslabel = ' node[midway, {}, sloped] {}'\
                    .format(self.label_position, '{' + self.label + '}')
        else:
            lslabel = ' node[midway, {}, sloped] {}'\
                .format(self.label_position, '{' + self.label_mask + '}')
        output.append(r'\draw{} ({}) -- ({}){};'.format(thickness,
                                                        self.endpoints[0].name,
                                                        self.endpoints[1].name,
                                                        lslabel))
        return output

    def tikz_label(self):
        """Return the command to write the labels."""
        output = ''
        if self.label_endpoints:
            output = '{}\n{}'.format(self.endpoints[0].tikz_label(),
                                     self.endpoints[1].tikz_label())
        return output

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        if value in THICKNESS_VALUES:
            if value == '':
                value = None
            self._thickness = value
        else:
            raise ValueError('Cannot use \'{}\' as thickness for a '
                             'LineSegment. Available values are in: {}.'
                             .format(str(value), str(THICKNESS_VALUES)))
