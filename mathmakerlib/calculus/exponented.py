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

"""
Exponented objects are any calculable objects that have an exponent, like in
7³ or x².
"""


import copy

from mathmakerlib.core.printable import Printable
from mathmakerlib.core.signed import Signed


class Exponented(Printable):
    """
    Exponented objects are any calculable objects that have an exponent, like
    in 7³ or x². The lower part is called content, the higher part is the
    exponent.
    """

    def __init__(self, content, exponent=None):
        self._content = None
        self.content = content
        self._exponent = None
        self.exponent = exponent

    def __repr__(self):
        if self.exponent is None:
            return 'Exponented({})'.format(repr(self.content))
        else:
            return 'Exponented({}^{})'.format(repr(self.content),
                                              repr(self.exponent))

    def __str__(self):
        if self.exponent is not None:
            return str(self.content) + '^' + str(self.exponent)
        else:
            return str(self.content)

    @property
    def content(self):
        """The lower part of the Exponented object."""
        return self._content

    @content.setter
    def content(self, content):
        if isinstance(content, int):
            from mathmakerlib.calculus import Number
            content = Number(content)
        if not isinstance(content, Printable):
            raise TypeError('The content of an Exponented must be a Printable '
                            'object. An int would be '
                            'accepted (turned into Number). Got {} instead.'
                            .format(str(type(content))))
        self._content = copy.deepcopy(content)

    @property
    def exponent(self):
        """The exponent part of the Exponented object."""
        return self._exponent

    @exponent.setter
    def exponent(self, exponent):
        if isinstance(exponent, int):
            from mathmakerlib.calculus import Number
            exponent = Number(exponent)
        if not (exponent is None or isinstance(exponent, Printable)):
            raise TypeError('The exponent of an Exponented must be either '
                            'None or a Printable object. An int would be '
                            'accepted (turned into Number). Got {} instead.'
                            .format(str(type(exponent))))
        self._exponent = copy.deepcopy(exponent)

    def imprint(self, start_expr=True, variant='latex'):
        if self.exponent is None:
            return self.content.imprint(start_expr=start_expr, variant=variant)
        else:
            open_brace = close_brace = ''
            if isinstance(self.content, Signed) and self.content.sign == '-':
                open_brace = '('
                close_brace = ')'
            open_curly = '{'
            close_curly = '}'
            if variant == 'user_input':
                open_curly = close_curly = ''
            return open_brace \
                + self.content.imprint(start_expr=start_expr, variant=variant)\
                + close_brace + '^' + open_curly \
                + self.exponent.imprint(start_expr=True, variant=variant) \
                + close_curly
