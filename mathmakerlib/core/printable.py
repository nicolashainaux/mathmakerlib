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

from abc import ABCMeta, abstractmethod


class Printable(object, metaclass=ABCMeta):

    @abstractmethod
    def imprint(self, start_expr=True, variant='latex'):
        """
        Return the LaTeX (or user input version) string of the object.
        """

    @property
    def printed(self):
        """
        self.printed is same as self.imprint(start_expr=True, variant='latex').
        """
        return self.imprint(start_expr=True, variant='latex')

    @property
    def uiprinted(self):
        """
        Shortcut for self.imprint(start_expr=True, variant='user_input').
        """
        return self.imprint(start_expr=True, variant='user_input')
