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
# from mathmakerlib.calculus.number import Number
# from mathmakerlib.shared import ROOTDIR, L10N_DOMAIN, LOCALEDIR
# from mathmakerlib import config

EQUALITIES = \
    {'cos': r'\[cos(\widehat{{\text{{{angle}}}}})='
            r'\frac{{\text{{{adj}}}}}{{\text{{{hyp}}}}}\]',
     'sin': r'\[sin(\widehat{{\text{{{angle}}}}})='
            r'\frac{{\text{{{opp}}}}}{{\text{{{hyp}}}}}\]',
     'tan': r'\[tan(\widehat{{\text{{{angle}}}}})='
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
        else:
            raise ValueError(f'The provided object (expected: RightTriangle, '
                             f'provided: {type(rt).__name__}) has not been '
                             f'set up for trigonometry.')

    def setup_hyp_adj_opp(self, trigo_fct, angle_nb):
        adj = opp = hyp = ''
        if trigo_fct == 'cos':
            adj = {0: self.rt.leg0.length_name,
                   2: self.rt.leg1.length_name[::-1]}[angle_nb]
            hyp = {0: self.rt.hyp.length_name[::-1],
                   2: self.rt.hyp.length_name}[angle_nb]
        elif trigo_fct == 'sin':
            opp = {0: self.rt.leg1.length_name[::-1],
                   2: self.rt.leg0.length_name}[angle_nb]
            hyp = {0: self.rt.hyp.length_name,
                   2: self.rt.hyp.length_name[::-1]}[angle_nb]
        else:  # trigo_fct == 'tan'
            adj = {0: self.rt.leg0.length_name[::-1],
                   2: self.rt.leg1.length_name}[angle_nb]
            opp = {0: self.rt.leg1.length_name,
                   2: self.rt.leg0.length_name[::-1]}[angle_nb]
        return (hyp, adj, opp)

    def imprint(self, neq=False, start_expr=True, variant='latex'):
        trigo_fct, angle_nb = self.rt.trigo_setup.split('_')
        angle_nb = int(angle_nb)
        template = EQUALITIES[trigo_fct]
        hyp, adj, opp = self.setup_hyp_adj_opp(trigo_fct, angle_nb)
        data = {'angle': self.rt.angles[angle_nb].name,
                'hyp': hyp, 'adj': adj, 'opp': opp}
        return template.format(**data)

    def autosolve(self, ):
        """
        Print the complete resolution.
        """
        # tr = translation(L10N_DOMAIN, LOCALEDIR, [config.language]).gettext
        # data = self.setup_data(trigo_fct, angle_nb)
        # template =
        # return f'{self.printed}\n{template.format(**data)}'
