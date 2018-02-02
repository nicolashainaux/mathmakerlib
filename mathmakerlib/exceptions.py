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


class MathmakerLibError(Exception):
    """Basic exception for errors raised by Mathmaker Lib."""
    def __init__(self, msg=None):
        if msg is None:
            # Set some default useful error message
            msg = 'An error occured in Mathmaker Lib'
        super().__init__(msg)


class StopCalculation(MathmakerLibError):
    """When no further calculation can be made."""
    def __init__(self, o, msg=None):
        if msg is None:
            msg = 'No further calculation can be done on {}.'.format(repr(o))
        super().__init__(msg=msg)


class StopFractionReduction(StopCalculation):
    """When no further reduction can be made."""
    def __init__(self, f, msg=None):
        super().__init__(f,
                         msg='{} can no further be reduced.'.format(repr(f)))


class ZeroLengthPointsPair(MathmakerLibError):
    """In case of abusive use of a zero-length PointsPair."""
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Abusive use of a zero-length PointsPair.'
        super().__init__(msg=msg)


class ZeroLengthLineSegment(ZeroLengthPointsPair):
    """In case of abusive use of a zero-length LineSegment."""
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Abusive use of a zero-length LineSegment.'
        super().__init__(msg=msg)


class ZeroVector(ZeroLengthPointsPair):
    """In case of abusive use of a zero Vector."""
    def __init__(self, msg=None):
        if msg is None:
            msg = 'Abusive use of a zero Vector.'
        super().__init__(msg=msg)


ZERO_OBJECTS_ERRORS = {'PointsPair': ZeroLengthPointsPair,
                       'LineSegment': ZeroLengthLineSegment,
                       'Vector': ZeroVector}
