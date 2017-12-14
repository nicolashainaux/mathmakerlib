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

from mathmakerlib.core.drawable import check_scale, Drawable, HasThickness
from mathmakerlib.core.drawable import tikz_approx_position, tikz_options_list
from mathmakerlib.geometry.pointspair import PointsPair
from mathmakerlib.calculus.number import Number
from mathmakerlib.geometry.point import OPPOSITE_LABEL_POSITIONS

LABEL_MASK_VALUES = [None, ' ', '?']


class LineSegment(Drawable, HasThickness, PointsPair):

    def __init__(self, *points, thickness='thick', label=None, label_mask=None,
                 label_position='anticlockwise', label_scale=None,
                 draw_endpoints=True, label_endpoints=True, color=None,
                 mark=None, mark_scale=Number('0.5'),
                 locked_label=False):
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
        :param label_scale: the label's scale
        :type label_scale: None or anything that is accepted to create a Number
        :param draw_endpoints: whether or not actually draw the endpoints.
        Defaults to True.
        :type draw_endpoints: bool
        :param label_endpoints: whether or not label the endpoints.
        Defaults to True.
        :type label_endpoints: bool
        :param mark: the mark to print on the line segment
        :type mark: str
        :param mark_scale: the scale (size) of the mark. Defaults to 0.5
        :type mark_scale: any number
        :param locked_label: to allow or prevent, by default, modifications of
        the LineSegment's label.
        :type locked_label: bool
        """
        if len(points) != 2:
            raise TypeError('Two Points are required to create a '
                            'LineSegment. Got {} object(s) instead.'
                            .format(len(points)))
        PointsPair.__init__(self, *points)
        self._label = None
        self._thickness = None
        self._label_mask = None
        self._label_position = None
        self._label_scale = None
        self._draw_endpoints = None
        self._label_endpoints = None
        self._locked_label = False  # Only temporary, in order to be able to
        self.label = label          # use the label setter.
        self.label_mask = label_mask
        self.label_scale = label_scale
        self.thickness = thickness
        self.draw_endpoints = draw_endpoints
        self.label_endpoints = label_endpoints
        self.mark = mark
        self.mark_scale = mark_scale
        self.endpoints[1].label_position = tikz_approx_position(self.slope360)
        self.endpoints[0].label_position = \
            OPPOSITE_LABEL_POSITIONS[self.endpoints[1].label_position]
        if label_position == 'anticlockwise':
            if self.deltax >= 0:
                self.label_position = 'below'
            else:
                self.label_position = 'above'
        elif label_position == 'clockwise':
            if self.deltax >= 0:
                self.label_position = 'above'
            else:
                self.label_position = 'below'
        else:
            self.label_position = label_position
        if color is not None:
            self.color = color
        self._comment_designation = 'Line Segment'
        if not isinstance(locked_label, bool):
            raise TypeError('Expected bool type for \'locked_label\' keyword '
                            'argument. Found {}.'.format(type(locked_label)))
        self._locked_label = locked_label

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
    def locked_label(self):
        """Tell if the LineSegment's label can be changed."""
        return self._locked_label

    def lock_label(self):
        """Forbid modifications of LineSegment's label."""
        self._locked_label = True

    def unlock_label(self):
        """Allow modifications of LineSegment's label."""
        self._locked_label = False

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        if self.locked_label:
            raise TypeError('This LineSegments\' label is locked. '
                            'If you\'re using this LineSegment embedded in '
                            'another object (e.g. a Polygon), please use the '
                            'setup_labels() method of this object. Otherwise, '
                            'first explicitely unlock the LineSegment.')
        else:
            super(LineSegment, self.__class__).label.fset(self, value)

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
    def mark(self):
        return self._mark

    @mark.setter
    def mark(self, value):
        if value is not None:
            self._mark = str(value)
        else:
            self._mark = None

    @property
    def mark_scale(self):
        return self._mark_scale

    @mark_scale.setter
    def mark_scale(self, value):
        check_scale(value, 'LineSegment\'s mark')
        self._mark_scale = Number(value)

    @property
    def label_position(self):
        return self._label_position

    @label_position.setter
    def label_position(self, value):
        self._label_position = str(value)

    @property
    def label_scale(self):
        return self._label_scale

    @label_scale.setter
    def label_scale(self, value):
        if value is None:
            self._label_scale = None
        else:
            self._label_scale = Number(value)

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

    def _tikz_label_options(self):
        options = ['midway', self.label_position, 'sloped']
        if self.label_scale is not None:
            options.append('scale={}'.format(self.label_scale))
        return options

    def tikz_label(self):
        lbl = ''
        if self.label_mask is None and self.label is not None:
            lbl = self.label
        elif self.label_mask is not None and self.label_mask != ' ':
            lbl = self.label_mask
        if lbl != '':
            return ' node{} {}'\
                .format(tikz_options_list(self._tikz_label_options()),
                        '{' + lbl + '}')
        else:
            return lbl

    def _tikz_ls_mark(self):
        if self.mark is not None:
            return ' node[midway, sloped, scale={}] {}'\
                .format(self.mark_scale, '{' + self.mark + '}')
        else:
            return ''

    def tikz_draw_section(self):
        return '-- ({}){}{}'.format(self.endpoints[1].name,
                                    self.tikz_label(),
                                    self._tikz_ls_mark())

    def tikz_draw(self):
        """Return the command to actually draw the LineSegment."""
        output = self._tikz_draw_endpoints()
        output.append(r'\draw{} ({}) {};'
                      .format(tikz_options_list('draw', self),
                              self.endpoints[0].name,
                              self.tikz_draw_section()))
        return output

    def tikz_points_labels(self):
        """Return the command to write the labels."""
        output = ''
        if self.label_endpoints:
            output = '{}\n{}'.format(self.endpoints[0].tikz_label(),
                                     self.endpoints[1].tikz_label())
        return output
