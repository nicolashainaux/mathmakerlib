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

from .point import Point
from .pointspair import PointsPair
from .linesegment import LineSegment
from .dividedlinesegment import DividedLineSegment
from .polygons import Polygon, shoelace_formula
from .polygons import Triangle, RightTriangle, EquilateralTriangle
from .polygons import IsoscelesTriangle
from .polygons import Quadrilateral, Rectangle, Rhombus, Square
from .angle import AngleDecoration, Angle, AnglesSet

__all__ = ['Point', 'PointsPair', 'LineSegment', 'DividedLineSegment',
           'Polygon', 'shoelace_formula',
           'Triangle', 'RightTriangle', 'EquilateralTriangle',
           'IsoscelesTriangle',
           'Quadrilateral', 'Rectangle', 'Rhombus', 'Square',
           'AngleDecoration', 'Angle', 'AnglesSet']
