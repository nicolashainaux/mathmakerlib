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

# from decimal import Decimal
# from gettext import translation

from .equation import Equation
from mathmakerlib.calculus.number import Number
from mathmakerlib.shared import ROOTDIR  # , L10N_DOMAIN, LOCALEDIR
from mathmakerlib import required

EQUALITIES = \
    {'cos': r'\[cos(\text{{{angle}}})='
            r'\frac{{\text{{{adj}}}}}{{\text{{{hyp}}}}}\]',
     'sin': r'\[sin(\text{{{angle}}})='
            r'\frac{{\text{{{opp}}}}}{{\text{{{hyp}}}}}\]',
     'tan': r'\[tan(\text{{{angle}}})='
            r'\frac{{\text{{{opp}}}}}{{\text{{{adj}}}}}\]'}


class TrigonometricEquation(Equation):

    def __init__(self, rt):
        """
        Initialize self.

        :param rt: the right triangle
        :type rt: RightTriangle
        """
        if rt.trigo_setup:
            self.rt = rt
            self.trigo_fct, angle_nb, t = self.rt.trigo_setup.split('_')
            self.angle_nb = int(angle_nb)
            self.to_calculate = t
        else:
            raise ValueError(f'The provided object (expected: RightTriangle, '
                             f'provided: {type(rt).__name__}) has not been '
                             f'set up for trigonometry. rt._trigo_setup == '
                             f"'{rt._trigo_setup}'")

    def setup_hyp_adj_opp(self):
        adj = opp = hyp = ''
        if self.trigo_fct == 'cos':
            adj = {0: self.rt.leg0.length_name,
                   2: self.rt.leg1.length_name[::-1]}[self.angle_nb]
            hyp = {0: self.rt.hyp.length_name[::-1],
                   2: self.rt.hyp.length_name}[self.angle_nb]
        elif self.trigo_fct == 'sin':
            opp = {0: self.rt.leg1.length_name[::-1],
                   2: self.rt.leg0.length_name}[self.angle_nb]
            hyp = {0: self.rt.hyp.length_name,
                   2: self.rt.hyp.length_name[::-1]}[self.angle_nb]
        else:  # trigo_fct == 'tan'
            adj = {0: self.rt.leg0.length_name[::-1],
                   2: self.rt.leg1.length_name}[self.angle_nb]
            opp = {0: self.rt.leg1.length_name,
                   2: self.rt.leg0.length_name[::-1]}[self.angle_nb]
        return (hyp, adj, opp)

    def imprint(self, neq=False, start_expr=True, variant='latex'):
        template = EQUALITIES[self.trigo_fct]
        hyp, adj, opp = self.setup_hyp_adj_opp()
        data = {'angle': self.rt.angles[self.angle_nb].name,
                'hyp': hyp, 'adj': adj, 'opp': opp}
        return template.format(**data)

    def setup_template_values(self, required_rounding):
        rounding_rank = Number(required_rounding).fracdigits_nb(
            ignore_trailing_zeros=False)
        angle_measure = Number(
            self.rt.angles[self.angle_nb].decoration.label_value)
        adj_side = {0: self.rt.leg0, 2: self.rt.leg1}[self.angle_nb]
        opp_side = {0: self.rt.leg1, 2: self.rt.leg0}[self.angle_nb]
        hyp, adj, opp = self.setup_hyp_adj_opp()
        adj_length = opp_length = hyp_length = ''
        equal_sign = '='
        result = ''
        unit = r'\degree' if self.to_calculate == 'angle' else ''

        if self.trigo_fct == 'cos':
            if self.to_calculate == 'adj':
                hyp_length = Number(self.rt.hyp.label_value, unit=None)
                unit = self.rt.hyp.label_value.unit
                result = angle_measure.cos() * hyp_length
            elif self.to_calculate == 'hyp':
                adj_length = Number(adj_side.label_value, unit=None)
                unit = adj_side.label_value.unit
                result = adj_length / angle_measure.cos()
            else:  # self.to_calculate == 'angle'
                hyp_length = Number(self.rt.hyp.label_value, unit=None)
                adj_length = Number(adj_side.label_value, unit=None)
                result = (adj_length / hyp_length).acos()

        elif self.trigo_fct == 'sin':
            if self.to_calculate == 'opp':
                hyp_length = Number(self.rt.hyp.label_value, unit=None)
                unit = self.rt.hyp.label_value.unit
                result = angle_measure.sin() * hyp_length
            elif self.to_calculate == 'hyp':
                opp_length = Number(opp_side.label_value, unit=None)
                unit = opp_side.label_value.unit
                result = opp_length / angle_measure.sin()
            else:  # self.to_calculate == 'angle'
                hyp_length = Number(self.rt.hyp.label_value, unit=None)
                opp_length = Number(opp_side.label_value, unit=None)
                result = (opp_length / hyp_length).asin()

        else:  # trigo_fct == 'tan'
            if self.to_calculate == 'opp':
                adj_length = Number(adj_side.label_value, unit=None)
                unit = adj_side.label_value.unit
                result = angle_measure.tan() * adj_length
            elif self.to_calculate == 'adj':
                opp_length = Number(opp_side.label_value, unit=None)
                unit = opp_side.label_value.unit
                result = opp_length / angle_measure.tan()
            else:  # self.to_calculate == 'angle'
                adj_length = Number(adj_side.label_value, unit=None)
                opp_length = Number(opp_side.label_value, unit=None)
                result = (opp_length / adj_length).atan()

        if result.fracdigits_nb() > rounding_rank:
            result = result.rounded(required_rounding)
            equal_sign = r'\approx '

        if isinstance(hyp_length, Number):
            hyp_length = hyp_length.printed
        if isinstance(opp_length, Number):
            opp_length = opp_length.printed
        if isinstance(adj_length, Number):
            adj_length = adj_length.printed

        return {'angle': self.rt.angles[self.angle_nb].name,
                'angle_measure': angle_measure.printed,
                'hyp': hyp, 'adj': adj, 'opp': opp,
                'hyp_length': hyp_length, 'adj_length': adj_length,
                'opp_length': opp_length,
                'equal_sign': equal_sign,
                'result_with_unit': Number(result, unit=unit).printed}

    def autosolve(self, required_rounding):
        """
        Print the complete resolution.
        """
        required.package['gensymb'] = True
        data = self.setup_template_values(required_rounding)
        template_fn = f'trigonometric_equation_calculate_' \
            f'{self.to_calculate}_{self.trigo_fct}.tex'
        template_path = ROOTDIR / 'calculus/equations/templates' / template_fn
        template = template_path.read_text()
        return f'{self.printed}\n{template.format(**data)}'
