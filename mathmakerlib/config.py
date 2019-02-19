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

# To change default mathmakerlib's settings:

# import mathmakerlib.config
# mathmakerlib.config.polygons.DEFAULT_WINDING = 'clockwise'

from decimal import Decimal

from mathmakerlib.LaTeX import DASHPATTERN_VALUES
from mathmakerlib.core.oriented import check_winding
from mathmakerlib.calculus.number import Number, is_number
from mathmakerlib.geometry.projections.oblique_projection \
    import DIRECTION_VALUES
from mathmakerlib.calculus.clocktime import check_clocktime_context
from mathmakerlib.calculus.clocktime import DEFAULT_CLOCKTIME_CONTEXT


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


class PointsSetup(object):

    def __init__(self):
        self.DEFAULT_POSITION_PRECISION = Decimal('1.000')

    @property
    def DEFAULT_POSITION_PRECISION(self):
        return self._DEFAULT_POSITION_PRECISION

    @DEFAULT_POSITION_PRECISION.setter
    def DEFAULT_POSITION_PRECISION(self, value):
        if not is_number(value):
            raise TypeError('DEFAULT_POSITION_PRECISION must be a number, '
                            'found {} instead.'.format(type(value)))
        self._DEFAULT_POSITION_PRECISION = value


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


class ClockTimeSetup(object):

    def __init__(self):
        self._CONTEXT = DEFAULT_CLOCKTIME_CONTEXT

    @property
    def CONTEXT(self):
        return self._CONTEXT

    @CONTEXT.setter
    def CONTEXT(self, context):
        check_clocktime_context(context)
        self._CONTEXT.update(context)


class ObliqueProjectionSetup(object):

    def __init__(self):
        self.RECEDING_AXIS_ANGLE = Number(45)
        self.RATIO = Number(0.67)
        self.DASHPATTERN = 'dashed'
        self.DIRECTION = 'top-right'

    @property
    def RECEDING_AXIS_ANGLE(self):
        return self._RECEDING_AXIS_ANGLE

    @RECEDING_AXIS_ANGLE.setter
    def RECEDING_AXIS_ANGLE(self, value):
        if not is_number(value):
            raise TypeError('RECEDING_AXIS_ANGLE must be a number, '
                            'found {} instead.'.format(repr(value)))
        self._RECEDING_AXIS_ANGLE = value

    @property
    def RATIO(self):
        return self._RATIO

    @RATIO.setter
    def RATIO(self, value):
        if not is_number(value):
            raise TypeError('RATIO must be a number, found {} instead.'
                            .format(repr(value)))
        self._RATIO = value

    @property
    def DASHPATTERN(self):
        return self._DASHPATTERN

    @DASHPATTERN.setter
    def DASHPATTERN(self, value):
        if value not in DASHPATTERN_VALUES:
            raise ValueError('Incorrect dashpattern value: \'{}\'. '
                             'Available values belong to: {}.'
                             .format(str(value), str(DASHPATTERN_VALUES)))
        self._DASHPATTERN = value

    @property
    def DIRECTION(self):
        return self._DIRECTION

    @DIRECTION.setter
    def DIRECTION(self, value):
        if value in DIRECTION_VALUES:
            self._direction = value
        else:
            raise ValueError('Incorrect direction value: \'{}\'. '
                             'Available values belong to: {}.'
                             .format(str(value), str(DIRECTION_VALUES)))
        self._DIRECTION = value


SUPPORTED_LANGUAGES = ['en', 'en_US', 'en_GB', 'fr', 'fr_FR']


def init():
    global polygons, angles, oblique_projection, language, points, clocktime
    global initialized

    try:
        initialized
    except NameError:
        initialized = False

    if not initialized:
        initialized = True
        polygons = PolygonsSetup()
        points = PointsSetup()
        angles = AnglesSetup()
        oblique_projection = ObliqueProjectionSetup()
        clocktime = ClockTimeSetup()
        language = 'en'
