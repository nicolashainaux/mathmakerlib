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

from mathmakerlib import required
from mathmakerlib.core.oriented import check_winding
from mathmakerlib.core.drawable import Colored, HasThickness, HasRadius
from mathmakerlib.core.drawable import tikz_options_list
from mathmakerlib.geometry.point import Point
from mathmakerlib.geometry.pointspair import PointsPair
from mathmakerlib.calculus.number import Number, is_number

LOCALE_US = 'en' if sys.platform.startswith('win') else 'en_US.UTF-8'


class AngleMark(Colored, HasThickness, HasRadius):

    def __init__(self, color=None, thickness='thick',
                 radius=Number('0.25', unit='cm')):
        self.color = color
        self.thickness = thickness
        self.radius = radius

    def tikz_mark_attributes(self):
        attributes = ['draw']
        for attr in [self.color, self.thickness]:
            if attr is not None:
                attributes.append(attr)
        if self.radius is not None:
            attributes.append('angle radius = {}'
                              .format(self.radius.uiprinted))
        return '[{}]'.format(', '.join(attributes))


class Angle(Colored):
    """Angles. Not Drawable neither publicly available yet."""

    def __init__(self, point, vertex, point_or_measure, mark=None,
                 mark_right=False, second_point_name='auto'):
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
        """
        self.mark = mark
        self.mark_right = mark_right
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
        pp0 = PointsPair(self._points[0], self._points[1])
        pp1 = PointsPair(self._points[1], self._points[2])
        pp2 = PointsPair(self._points[2], self._points[0])
        n = pp0.length ** 2 + pp1.length ** 2 - pp2.length ** 2
        d = 2 * pp0.length * pp1.length
        self._measure = Number(str(degrees(acos(n / d))))

    @property
    def vertex(self):
        return self._points[1]

    @property
    def points(self):
        return self._points

    @property
    def measure(self):
        """Measure of the Angle."""
        return self._measure

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

    def tikz_angle_mark(self):
        if self.mark is None or self.mark_right:
            return ''
        required.tikz_library['angles'] = True
        return 'pic {} {{angle = {}--{}--{}}}'\
            .format(self.mark.tikz_mark_attributes(),
                    self.points[0].name,
                    self.vertex.name,
                    self.points[2].name)

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
