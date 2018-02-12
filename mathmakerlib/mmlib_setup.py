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

# To change default mathmakerlib's settings:
# from mathmakerlib import mmlib_setup

# Then in your main module:
# mmlib_setup.init()

# example of usage to change a value:
# mmlib_setup.polygons.DEFAULT_WINDING = 'clockwise'

# from decimal import Decimal

from mathmakerlib.core.oriented import check_winding
from mathmakerlib.calculus.number import Number, is_number


class PolygonsSetup(object):

    def __init__(self):
        # default_winding can be set to either 'clockwise', 'anticlockwise' or
        # None. If it is left to None, the polygons' winding won't be forced
        # to a default value (if not overriden by the user at Polygon's
        # initialization), but deduced from the given vertices' order.
        # Use with caution: when you force the winding to be 'clockwise' by
        # default and give anticlockwise oriented vertices to build a Polygon,
        # the vertices' names' order in the final created Polygon WILL NOT be
        # the same as the given one (it cannot be the same). Yet setup_labels()
        # and setup_marks() WILL remember the order you gave the vertices to
        # create the Polygon (this places the marks and labels at expected
        # places...). By default, a warning will raise if the winding is forced
        # to the opposite warning of given Points when building a Polygon.
        self.DEFAULT_WINDING = None
        self.ENABLE_MISMATCH_WINDING_WARNING = True

    @property
    def DEFAULT_WINDING(self):
        return self._DEFAULT_WINDING

    @DEFAULT_WINDING.setter
    def DEFAULT_WINDING(self, value):
        if value is not None:
            check_winding(value)
        self._DEFAULT_WINDING = value

    @property
    def ENABLE_MISMATCH_WINDING_WARNING(self):
        return self._ENABLE_MISMATCH_WINDING_WARNING

    @ENABLE_MISMATCH_WINDING_WARNING.setter
    def ENABLE_MISMATCH_WINDING_WARNING(self, value):
        if value:
            self._ENABLE_MISMATCH_WINDING_WARNING = True
        else:
            self._ENABLE_MISMATCH_WINDING_WARNING = False


class AnglesSetup(object):

    def __init__(self):
        self.DEFAULT_ARMSPOINTS_POSITION = Number('0.8')

    @property
    def DEFAULT_ARMSPOINTS_POSITION(self):
        return self._DEFAULT_ARMSPOINTS_POSITION

    @DEFAULT_ARMSPOINTS_POSITION.setter
    def DEFAULT_ARMSPOINTS_POSITION(self, value):
        if not is_number(value):
            raise TypeError('DEFAULT_ARMSPOINTS_POSITION must be a number, '
                            'found {} instead.'.format(type(value)))
        self._DEFAULT_ARMSPOINTS_POSITION = value


SUPPORTED_LANGUAGES = ['en', 'en_US', 'en_GB', 'fr', 'fr_FR']


def init():
    global polygons, angles, language

    polygons = PolygonsSetup()
    angles = AnglesSetup()
    language = 'en'
