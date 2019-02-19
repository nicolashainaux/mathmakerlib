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

from .equilateral import Equilateral
from .polygon import Polygon, shoelace_formula
from .triangle import Triangle
from .righttriangle import RightTriangle
from .equilateraltriangle import EquilateralTriangle
from .isoscelestriangle import IsoscelesTriangle
from .quadrilateral import Quadrilateral
from .rectangle import Rectangle
from .rhombus import Rhombus
from .square import Square

__all__ = ['Equilateral', 'Polygon', 'shoelace_formula',
           'Triangle', 'RightTriangle', 'EquilateralTriangle',
           'IsoscelesTriangle',
           'Quadrilateral', 'Rectangle', 'Rhombus', 'Square']
