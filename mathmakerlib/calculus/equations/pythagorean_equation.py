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

from decimal import Decimal
from gettext import translation

from .equation import Equation
from mathmakerlib.calculus.number import Number
from mathmakerlib.shared import ROOTDIR, L10N_DOMAIN, LOCALEDIR
from mathmakerlib import config


class PythagoreanEquation(Equation):

    def __init__(self, rt):
        """
        Initialize self.

        :param rt: the right triangle
        :type rt: RightTriangle
        """
        self.rt = rt

    def imprint(self, start_expr=True, variant='latex'):
        return r"\text{{{hyp}}}^{{2}}"\
            r"=\text{{{leg1}}}^{{2}}+\text{{{leg2}}}^{{2}}"\
            .format(hyp=self.rt.hypotenuse.length_name,
                    leg1=self.rt.sides[0].length_name,
                    leg2=self.rt.sides[1].length_name)

    def autosolve(self, unknown_side, show_squares_step=False,
                  shortcut_mode=True, required_rounding=None):
        """
        Print the complete resolution.

        :param unknown_side: which side is to calculate ('leg0', 'leg1'
                             or 'hyp')
        :type unknown_side: str
        """
        tr = translation(L10N_DOMAIN, LOCALEDIR, [config.language]).gettext
        sides_id = ['leg0', 'leg1', 'hyp']
        if unknown_side not in sides_id:
            raise ValueError(f'Expected a value belonging to {sides_id}; '
                             f'got {unknown_side} instead.')
        if required_rounding is None:
            required_rounding = Decimal('1.000')
        rounding_rank = Number(required_rounding).fracdigits_nb(
            ignore_trailing_zeros=False)
        detailed = '_detailed' if show_squares_step else ''
        shortcut = '_shortcut' \
            if shortcut_mode and not unknown_side == 'hyp' else ''
        template_fn = f'pythagorean_equation_calculate_{unknown_side}'\
            f'{shortcut}{detailed}.tex'
        template_path = ROOTDIR / 'calculus/equations/templates' / template_fn
        template = template_path.read_text()
        data = {'hypotenuse': self.rt.hyp.length_name,
                'leg0': self.rt.leg0.length_name,
                'leg1': self.rt.leg1.length_name}
        equal_sign = '='

        if unknown_side == 'hyp':
            leg0_length = Number(self.rt.leg0.label_value, unit=None)
            leg1_length = Number(self.rt.leg1.label_value, unit=None)
            square_legs_sum = leg0_length * leg0_length \
                + leg1_length * leg1_length
            explanation = ' ' \
                + tr('because {length_name} is positive.')\
                .format(length_name=self.rt.hyp.length_name)
            result = square_legs_sum.sqrt().standardized()
            if result.fracdigits_nb() > rounding_rank:
                result = result.rounded(required_rounding)
                equal_sign = r'\approx'
            result = Number(result, unit=self.rt.leg0.label_value.unit)
            data.update({'leg0_length': leg0_length.printed,
                         'leg1_length': leg1_length.printed,
                         'square_legs_sum': square_legs_sum.printed,
                         'explanation': explanation,
                         'equal_sign': equal_sign,
                         'hypotenuse_length_with_unit': result.printed})

        elif unknown_side == 'leg0':
            pass
            # same

        else:  # unknown_side == 'leg1'
            pass
            # same

        return template.format(**data)
