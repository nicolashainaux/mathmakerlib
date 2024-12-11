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

from mathmakerlib import config
from mathmakerlib import required
from mathmakerlib.calculus.number import Number
from mathmakerlib.geometry.point import Point
from mathmakerlib.geometry.angle import AngleDecoration
from . import Triangle

TRIGO_SETUPS = ['cos_0_adj', 'cos_0_hyp', 'cos_2_adj', 'cos_2_hyp',
                'sin_0_opp', 'sin_0_hyp', 'sin_2_opp', 'sin_2_hyp',
                'tan_0_adj', 'tan_0_opp', 'tan_2_adj', 'tan_2_opp',
                'cos_0_angle', 'cos_2_angle', 'sin_0_angle', 'sin_2_angle',
                'tan_0_angle', 'tan_2_angle']


class RightTriangle(Triangle):
    """Right Triangles."""

    def __init__(self, start_vertex=None, name=None,
                 leg1_length=Number(2), leg2_length=Number(1),
                 mark_right_angle=True,
                 draw_vertices=False, label_vertices=True,
                 thickness='thick', color=None, rotation_angle=0,
                 winding=None, sloped_sides_labels=True):
        r"""
        Initialize Right Triangle

        :param start_vertex: the vertex to start to draw the Right Triangle
        (default (0; 0))
        :type start_vertex: Point
        :param name: the name of the Triangle, like ABC.
        Can be either None (the names will be automatically created), or a
        string of the letters to use to name the vertices. Only single letters
        are supported as Points' names so far (at Polygon's creation).
        See issue #3.
        :type name: None or str
        :param leg1_length: the leg1's length that will be used to calculate
        the coordinates of the vertices used to build the RightTriangle
        :type leg1_length: a number
        :param leg2_length: the leg2's length that will be used to calculate
        the coordinates of the vertices used to build the RightTriangle
        :type leg2_length: a number
        :param mark_right_angle: if True (default), the right angle will be
        automatically marked as right angle.
        :type mark_right_angle: bool
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
        if start_vertex is None:
            start_vertex = Point(0, 0)
        # Accepted type for leg1's and leg2's lengths is number, will be
        # checked at vertices' instanciations.
        v1 = Point(leg1_length + start_vertex.x, start_vertex.y)
        v2 = Point(leg1_length + start_vertex.x, leg2_length + start_vertex.y)
        if (winding == 'clockwise'
            or (winding is None
                and config.polygons.DEFAULT_WINDING == 'clockwise')):
            start_vertex, v2 = v2, start_vertex
        Triangle.__init__(self, start_vertex, v1, v2, name=name,
                          draw_vertices=draw_vertices,
                          label_vertices=label_vertices,
                          thickness=thickness, color=color,
                          rotation_angle=rotation_angle,
                          winding=winding,
                          sloped_sides_labels=sloped_sides_labels)
        self._type = 'RightTriangle'
        if mark_right_angle:
            self.right_angle.decoration = AngleDecoration(thickness=thickness)
            self.right_angle.mark_right = True
        self._trigo_setup = ''
        self.length_unit = ''

    @property
    def hypotenuse(self):
        return self._sides[2]

    @property
    def hyp(self):
        return self._sides[2]

    @property
    def leg0(self):
        return self._sides[0]

    @property
    def leg1(self):
        return self._sides[1]

    @property
    def right_angle(self):
        return self.angles[1]

    @property
    def trigo_setup(self):
        if self._trigo_setup in TRIGO_SETUPS:
            return self._trigo_setup
        return False

    def setup_for_trigonometry(self, angle_nb=None, trigo_fct=None,
                               angle_val=None,
                               up_length_val=None,
                               down_length_val=None,
                               only_mark_unknown_angle=False,
                               angle_decoration='default'):
        """
        Setup labels, determine subst_dict and stores configuration details.

        Exactly one parameter among the three *_val ones must be left to None.
        According to the chosen trigo_fct and this parameter, this method will
        create the correct subst_dict.

        :param angle_nb: must be either 0 or 2 (index of an acute angle)
        :type angle_nb: int
        :param trigo_fct: must belong to ['cos', 'sin', 'tan']
        :type trigo_fct: str
        :param angle_val: the angle's Number
        :type angle_val: Number (or leave it to None to use it as the unknown
            value to calculate)
        :param up_length_val: the length's Number of the side that's at the
            numerator of the trigonometric formula
        :type up_length_val: Number (or leave it to None to use it as the
            unknown value to calculate)
        :param down_length_val: the length's Number of the side that's at the
            denominator of the trigonometric formula
        :type down_length_val: Number (or leave it to None to use it as the
            unknown value to calculate)
        """
        if [angle_val, up_length_val, down_length_val].count(None) != 1:
            raise ValueError('Exactly one of the optional arguments '
                             '(angle_val, up_length_val, down_length_val)'
                             ' must be None.')
        if angle_nb not in [0, 2]:
            raise ValueError(f'angle_nb must be 0 or 2 (got {angle_nb}'
                             f' instead)')
        if trigo_fct not in ['cos', 'sin', 'tan']:
            raise ValueError(f"trigo_fct must be either 'cos', 'sin' "
                             f"or 'tan', got '{trigo_fct} instead.")
        if angle_decoration == 'default':
            angle_decoration = AngleDecoration()
        side_nb = {'cos': {0: {'up': 0, 'down': 2},
                           2: {'up': 1, 'down': 2}},
                   'sin': {0: {'up': 1, 'down': 2},
                           2: {'up': 0, 'down': 2}},
                   'tan': {0: {'up': 1, 'down': 0},
                           2: {'up': 0, 'down': 1}}}
        upside_nb = side_nb[trigo_fct][angle_nb]['up']
        downside_nb = side_nb[trigo_fct][angle_nb]['down']
        labels = [None, None, None]
        self.angles[angle_nb].decoration = angle_decoration
        to_calculate = 'angle'
        if angle_val is None:
            self.length_unit = str(up_length_val.unit)
            if not only_mark_unknown_angle:
                self.angles[angle_nb].label = '?'
            else:
                self.angles[angle_nb].label = ''
        else:
            self.angles[angle_nb].label = Number(angle_val, unit=r'\degree')
            required.package['gensymb'] = True
        if up_length_val is None:
            self.length_unit = str(down_length_val.unit)
            labels[upside_nb] = '?'
            to_calculate = {'cos': 'adj', 'sin': 'opp',
                            'tan': 'opp'}[trigo_fct]
        else:
            labels[upside_nb] = Number(up_length_val, unit=self.length_unit)
        if down_length_val is None:
            self.length_unit = str(up_length_val.unit)
            labels[downside_nb] = '?'
            to_calculate = {'cos': 'hyp', 'sin': 'hyp',
                            'tan': 'adj'}[trigo_fct]
        else:
            labels[downside_nb] = Number(down_length_val,
                                         unit=self.length_unit)
        self.setup_labels(labels)
        self._trigo_setup = f'{trigo_fct}_{angle_nb}_{to_calculate}'
