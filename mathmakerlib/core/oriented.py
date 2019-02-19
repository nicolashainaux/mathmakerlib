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

from abc import ABCMeta


def shoelace_formula(*points):
    x = [v.x for v in points]
    y = [v.y for v in points]
    x.append(x[0])
    y.append(y[0])
    x.append(x[1])
    y.append(y[1])
    return sum(x[i] * (y[i + 1] - y[i - 1])
               for i in range(1, len(points) + 1)) / 2


def check_winding(value):
    if value not in ['clockwise', 'anticlockwise']:
        raise ValueError('Expect \'clockwise\' or \'anticlockwise\'. '
                         'Found \'{}\' instead.'.format(value))


class Oriented(object, metaclass=ABCMeta):
    @property
    def winding(self):
        """Tells whether the Oriented object is clockwise or anticlockwise."""
        return self._winding

    @winding.setter
    def winding(self, value):
        """The winding can be set only once (at object's initialization)."""
        if not hasattr(self, '_winding'):
            check_winding(value)
            setattr(self, '_winding', value)
        else:
            raise AttributeError('Cannot reset the winding of a {}.'
                                 .format(type(self).__name__))
