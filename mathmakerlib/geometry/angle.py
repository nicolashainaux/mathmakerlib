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

from math import acos, degrees

from mathmakerlib import required
from mathmakerlib.core.drawable import Colored, HasThickness, HasRadius
from mathmakerlib.geometry.point import Point
from mathmakerlib.geometry.pointspair import PointsPair
from mathmakerlib.calculus.number import Number
# from mathmakerlib.calculus.tools import is_number

RIGHT_ANGLES_MARK_HACK = \
    r"""% Hack to mark right angles, taken almost unmodified from
% https://tex.stackexchange.com/a/154357/81138
\makeatletter
\tikzset{
  pics/squared angle/.style = {
    setup code  = \tikz@lib@angle@parse#1\pgf@stop,
    background code = \tikz@lib@angle@background#1\pgf@stop,
    foreground code = \tikz@lib@squaredangle@foreground#1\pgf@stop,},
  angle eccentricity/.initial=.6,
  angle radius/.initial=5mm
}

\def\tikz@lib@squaredangle@foreground#1--#2--#3\pgf@stop{%
  \path [name prefix ..] [pic actions]
  ([shift={(\tikz@start@angle@temp:\tikz@lib@angle@rad pt)}]#2.center)
    |-
  ([shift={(\tikz@end@angle@temp:\tikz@lib@angle@rad pt)}]#2.center);
  \ifx\tikzpictext\relax\else%
    \def\pgf@temp{\node()[name prefix
      ..,at={([shift={({.5*\tikz@start@angle@temp+.5*\tikz@end@angle@temp}:
                       \pgfkeysvalueof{/tikz/angle eccentricity}
                       *\tikz@lib@angle@rad pt)
                      }]#2.center)}]}
    \expandafter\pgf@temp\expandafter[\tikzpictextoptions]{\tikzpictext};%
  \fi
}
\makeatother
"""


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

    def __init__(self, *points, mark=None, mark_right=False):
        if not len(points) == 3:
            raise ValueError('Three Points are required to build an Angle. '
                             'Got {} positional arguments instead.'
                             .format(len(points)))
        self._points = []
        for i, p in enumerate(points):
            if not isinstance(p, Point):
                raise TypeError('Three Points are required to build an Angle. '
                                'Positional argument #{} is {} instead.'
                                .format(i, type(p)))
            self._points.append(p)

        self.mark = mark
        self.mark_right = mark_right
        # requires.rightangle_mark_hack is only set when it is used

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
        if self.mark is None:
            return ''
        required.tikz_library['angles'] = True
        if self.mark_right:
            right = 'squared '
            required.hack['rightangle_mark'] = True
        else:
            right = ''
        return 'pic {} {{{}angle = {}--{}--{}}}'\
            .format(self.mark.tikz_mark_attributes(),
                    right,
                    self.points[0].name,
                    self.vertex.name,
                    self.points[2].name)
