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

import random
from typing import Tuple, Optional

from mathmakerlib import required
from mathmakerlib.core.drawable import Drawable, Fillable
from mathmakerlib.core import parse_layout_descriptor


class RectangleGrid(Drawable, Fillable):

    def __init__(self, layout='2×2', fill='0×0',
                 fillcolor='lightgray', startvertex='random'):
        """
        Initialize a RectangleGrid object.

        If the fill parameter exceeds the layout (e.g. layout='3×6' and
        fill='4×5'), all cells will be colored.
        If the fill rectangle fits into layout (e.g. layout='3×6' and
        fill='2×5'), it will be reproduced.
        If it does not (e.g. layout='3×6' and fill='4×4'), the cells will be
        colored one after the other.

        :param layout: string of the form 'rows×columns' specifying the grid
                       dimensions
        :type layout: str
        :param fill: string of the form 'rows×columns' specifying the
                     dimensions of the colored area
        :param fill: str
        :param fillcolor: string specifying the color to use for the filled
                          area
        :param fillcolor: str
        :param startvertex: string specifying the vertex where the colored area
                            starts.
                            Must be one of 'topleft', 'topright', 'bottomleft',
                            'bottomright', 'random'
        """
        # bottomleft_corner is directly hardcoded in the pattern since there's
        # no obvious reason to set it anywhere else
        # self.bottomleft_corner = (0, 0)

        # step is also directly hardcoded in the pattern; changing the scale
        # seems to be more practical and enough
        # step = '1 cm'

        # self.pattern = r'\draw[step=1cm] (0, 0) grid ({width}, {height});'
        # self.fillpattern = r'\draw[fill={fillcolor}] '\
        #     r'({x0}, {y0}) rectangle ({x1}, {y1});'

        # Parse layout and fill descriptors
        self.rows, self.cols = parse_layout_descriptor(layout, min_row=1,
                                                       min_col=1)
        self.fill_rows, self.fill_cols = parse_layout_descriptor(fill)
        self.fillcolor = fillcolor

        # Handle startvertex
        if startvertex == 'random':
            startvertex = random.choice(['topleft', 'topright', 'bottomleft',
                                         'bottomright'])
        self.startvertex = startvertex

        # Adjust the fill dimensions if necessary
        self._adjust_fill_dimensions()

    def _adjust_fill_dimensions(self):
        """
        Adjust the fill dimensions to fit within the grid while preserving
        the number of cells.
        """
        # If fill dimensions are 0×0, nothing to adjust
        if self.fill_rows == 0 and self.fill_cols == 0:
            self.fill_strategy = "none"
            return

        # Calculate number of cells to fill
        fill_cells = self.fill_rows * self.fill_cols
        grid_cells = self.rows * self.cols

        # If fill_cells exceeds grid_cells, fill the entire grid
        if fill_cells >= grid_cells:
            self.fill_rows = self.rows
            self.fill_cols = self.cols
            self.fill_strategy = "full"
            return

        # Check if the fill rectangle fits directly
        if self.fill_rows <= self.rows and self.fill_cols <= self.cols:
            self.fill_strategy = "direct"
            return

        # Check if swapping dimensions would work
        if self.fill_cols <= self.rows and self.fill_rows <= self.cols:
            self.fill_rows, self.fill_cols = self.fill_cols, self.fill_rows
            self.fill_strategy = "direct"
            return

        # Try to find alternative dimensions for the fill
        possible_dimensions = []
        for i in range(1, fill_cells + 1):
            if fill_cells % i == 0:
                j = fill_cells // i
                if i <= self.rows and j <= self.cols:
                    possible_dimensions.append((i, j))

        if possible_dimensions:
            # Choose the dimensions that are closest to the original
            self.fill_rows, self.fill_cols = possible_dimensions[0]
            self.fill_strategy = "direct"
            return

        # If no direct solution, use the complement strategy
        self.fill_strategy = "complement"
        self.complement_cells = grid_cells - fill_cells

        # Find dimensions for the white rectangle (the complement)
        possible_complements = []
        for i in range(1, self.complement_cells + 1):
            if self.complement_cells % i == 0:
                j = self.complement_cells // i
                if i <= self.rows and j <= self.cols:
                    perimeter = 2 * (i + j)
                    possible_complements.append((i, j, perimeter))

        # Sort by perimeter (smaller is better)
        possible_complements.sort(key=lambda x: x[2])
        if possible_complements:
            self.complement_rows, self.complement_cols, _ = \
                possible_complements[0]
        # else:
        #     # Fallback: find the best approximation
        #     self.complement_rows = min(self.rows, self.complement_cells)
        #     self.complement_cols = \
        #         self.complement_cells // self.complement_rows

    def _get_filled_rectangle_coordinates(self) -> Tuple[int, int, int, int]:
        """
        Calculate coordinates for the filled rectangle based on startvertex.
        Returns (x1, y1, x2, y2) where (x1, y1) is one corner and (x2, y2) is
        the opposite corner.
        """
        if self.fill_strategy == "none":
            return (0, 0, 0, 0)

        if self.fill_strategy in ["direct", "full"]:
            if self.startvertex == 'topleft':
                return (0, self.rows, self.fill_cols,
                        self.rows - self.fill_rows)
            elif self.startvertex == 'topright':
                return (self.cols, self.rows, self.cols - self.fill_cols,
                        self.rows - self.fill_rows)
            elif self.startvertex == 'bottomleft':
                return (0, 0, self.fill_cols, self.fill_rows)
            elif self.startvertex == 'bottomright':
                return (self.cols, 0, self.cols - self.fill_cols,
                        self.fill_rows)

        # For complement strategy, always fill the whole grid first
        return (0, 0, self.cols, self.rows)

    def _get_complement_rectangle_coordinates(self) -> Optional[Tuple[
            int, int, int, int]]:
        """
        Calculate coordinates for the white rectangle in the complement
        strategy.
        Returns (x1, y1, x2, y2) or None if not using complement strategy.
        """
        if self.fill_strategy != "complement":
            return None

        # The white rectangle should be in the opposite corner from startvertex
        if self.startvertex == 'topleft':
            return (self.cols, 0, self.cols - self.complement_cols,
                    self.complement_rows)
        elif self.startvertex == 'topright':
            return (0, 0, self.complement_cols, self.complement_rows)
        elif self.startvertex == 'bottomleft':
            return (self.cols, self.rows, self.cols - self.complement_cols,
                    self.rows - self.complement_rows)
        elif self.startvertex == 'bottomright':
            return (0, self.rows, self.complement_cols,
                    self.rows - self.complement_rows)

    def draw(self) -> str:
        """
        Generate TikZ code for the grid with the colored area.
        """
        required.package['tikz'] = True
        tikz_code = [r"\begin{tikzpicture}"]

        # Add colored rectangle if needed
        if self.fill_strategy != "none":
            x1, y1, x2, y2 = self._get_filled_rectangle_coordinates()
            if not (x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0):
                pattern = r"  \draw[fill={fillcolor}] "\
                    r"({x1}, {y1}) rectangle ({x2}, {y2});"
                tikz_code.append(pattern.format(fillcolor=self.fillcolor,
                                                x1=x1, y1=y1, x2=x2, y2=y2))

        # Add white rectangle for complement strategy
        if self.fill_strategy == "complement":
            x1, y1, x2, y2 = self._get_complement_rectangle_coordinates()
            pattern = r"  \draw[fill=white] "\
                r"({x1}, {y1}) rectangle ({x2}, {y2});"
            tikz_code.append(pattern.format(x1=x1, y1=y1, x2=x2, y2=y2))

        # Add the grid
        pattern = r"  \draw[step=1cm] (0, 0) grid ({cols}, {rows});"
        tikz_code.append(pattern.format(cols=self.cols, rows=self.rows))

        # Close tikzpicture environment
        tikz_code.append(r"\end{tikzpicture}")

        return "\n".join(tikz_code)

    def _tikz_draw_options(self):
        pass

    def tikz_declarations(self):
        pass

    def tikz_draw(self):
        pass

    def tikz_drawing_comment(self):
        pass

    def tikz_label(self):
        return ''

    def tikz_points_labels(self):
        pass
