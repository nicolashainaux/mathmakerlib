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
# from mathmakerlib import config

# Then in your main module:
# config.init()

# and where you need to change values:
# config.MY_VALUE = ...


def init():
    global DEFAULT_POLYGON_WINDING

    # This can be set to either 'clockwise', 'anticlockwise' or None.
    # If it is left to None, the polygons' winding won't be forced to a default
    # value (if not overriden by the user at Polygon's initialization),
    # but deduced from the given vertices' order.
    DEFAULT_POLYGON_WINDING = None
