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

from abc import ABCMeta


def check_winding(value):
    if value not in ['clockwise', 'anticlockwise']:
        raise ValueError('Expect \'clockwise\' or \'anticlockwise\'. '
                         'Found \'{}\' instead.'.format(value))


class Oriented(object, metaclass=ABCMeta):
    @property
    def winding(self):
        return self._winding

    @winding.setter
    def winding(self, value):
        check_winding(value)
        setattr(self, '_winding', value)
