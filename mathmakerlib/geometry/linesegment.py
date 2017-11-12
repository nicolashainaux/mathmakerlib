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

import copy

from mathmakerlib.geometry.pointspair import PointsPair
from mathmakerlib.calculus.number import Number
from mathmakerlib.geometry.point import Point, OPPOSITE_LABEL_POSITIONS

THICKNESS_VALUES = [None, 'thin', 'very thin', 'ultra thin', 'thick',
                    'very thick', 'ultra thick']
LABEL_MASK_VALUES = [None, ' ', '?']


class LineSegment(PointsPair):

    def __init__(self, *points, thickness='thick', label=None, label_mask=None,
                 label_position='anticlockwise',
                 draw_endpoints=True, label_endpoints=True, color=None):
        """
        Initialize LineSegment

        :param points: either one LineSegment to copy, or two Points
        :type points: another LineSegment or a list or tuple of two Points
        :param thickness: the LineSegment's thickness. Available values are
        TikZ's ones.
        :type thickness: str
        :param label: what will be written along the LineSegment, about its
        middle. A None value will disable the LineSegment's labeling.
        :type label: None or str
        :param label_mask: if not None (default), hide the label with ' '
        or '?'
        :type label_mask: None or str (' ' or '?')
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
        if len(points) == 2:
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
            self._points = [copy.deepcopy(points[0]), copy.deepcopy(points[1])]
            self._label = None
            self._thickness = None
            self._label_mask = None
            self._label_position = None
            self._draw_endpoints = None
            self._label_endpoints = None
            self.label = label
            self.label_mask = label_mask
            self.thickness = thickness
            self.draw_endpoints = draw_endpoints
            self.label_endpoints = label_endpoints
            PointsPair.__init__(self)
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
            if color is not None:
                self.color = color
            self._comment_designation = 'Line Segment'
        else:
            raise TypeError('Two Points are required to create a '
                            'LineSegment. Got {} object(s) instead.'
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
        return self._points

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

    def tikz_declarations(self):
        """Return the LineSegment's Points' declarations."""
        return '{}\n{}'\
            .format(self.endpoints[0].tikz_declarations(),
                    self.endpoints[1].tikz_declarations())

    def tikz_drawing_comment(self):
        """Return the comments preceding the LineSegment's drawings."""
        ls_draw_comment = '% Draw {}'.format(self._comment_designation)
        if self.draw_endpoints:
            return ['% Draw Points', ls_draw_comment]
        else:
            return [ls_draw_comment]

    def _tikz_draw_options(self):
        return [self.thickness, self.color]

    def _tikz_draw_endpoints(self):
        if self.draw_endpoints:
            return ['{}\n{}\n'.format(self.endpoints[0].tikz_draw()[0],
                                      self.endpoints[1].tikz_draw()[0])]
        else:
            return []

    def _tikz_ls_label(self):
        lslabel = ''
        if self.label_mask is None:
            if self.label is not None:
                lslabel = ' node[midway, {}, sloped] {}'\
                    .format(self.label_position, '{' + self.label + '}')
        else:
            lslabel = ' node[midway, {}, sloped] {}'\
                .format(self.label_position, '{' + self.label_mask + '}')
        return lslabel

    def tikz_draw(self):
        """Return the command to actually draw the LineSegment."""
        output = self._tikz_draw_endpoints()
        output.append(r'\draw{} ({}) -- ({}){};'
                      .format(self.tikz_options_list('draw'),
                              self.endpoints[0].name,
                              self.endpoints[1].name,
                              self._tikz_ls_label()))
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
            self._thickness = value
        else:
            raise ValueError('Cannot use \'{}\' as thickness for a '
                             'LineSegment. Available values are in: {}.'
                             .format(str(value), str(THICKNESS_VALUES)))
