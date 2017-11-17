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

from mathmakerlib import requires_pkg

LATEX = ['white', 'black', 'red', 'green', 'blue', 'cyan', 'magenta', 'yellow']

# Colors' names from xcolor package
XCOLOR_BASE = ['black', 'blue', 'brown', 'cyan', 'darkgray', 'gray', 'green',
               'lightgray', 'lime', 'magenta', 'olive', 'orange', 'pink',
               'purple', 'red', 'teal', 'violet', 'white', 'yellow']
XCOLOR_DVIPSNAMES = ['Apricot', 'Aquamarine', 'Bittersweet', 'Black', 'Blue',
                     'BlueGreen', 'BlueViolet', 'BrickRed', 'Brown',
                     'BurntOrange', 'CadetBlue', 'CarnationPink', 'Cerulean',
                     'CornflowerBlue', 'Cyan', 'Dandelion', 'DarkOrchid',
                     'Emerald', 'ForestGreen', 'Fuchsia', 'Goldenrod', 'Gray',
                     'Green', 'GreenYellow', 'JungleGreen', 'Lavender',
                     'LimeGreen', 'Magenta', 'Mahogany', 'Maroon', 'Melon',
                     'MidnightBlue', 'Mulberry', 'NavyBlue', 'OliveGreen',
                     'Orange', 'OrangeRed', 'Orchid', 'Peach', 'Periwinkle',
                     'PineGreen', 'Plum', 'ProcessBlue', 'Purple', 'RawSienna',
                     'Red', 'RedOrange', 'RedViolet', 'Rhodamine', 'RoyalBlue',
                     'RoyalPurple', 'RubineRed', 'Salmon', 'SeaGreen', 'Sepia',
                     'SkyBlue', 'SpringGreen', 'Tan', 'TealBlue', 'Thistle',
                     'Turquoise', 'Violet', 'VioletRed', 'White',
                     'WildStrawberry', 'Yellow', 'YellowGreen', 'YellowOrange']


def check(value):
    if value in LATEX or value in XCOLOR_BASE:
        # Base LaTeX colors do not need to be explicitely loaded.
        # As tikz package already loads xcolor base names, it's not
        # necessary to explicitely load them neither.
        pass
    elif value in XCOLOR_DVIPSNAMES:
        requires_pkg.xcolor = True
        if 'dvipsnames' not in requires_pkg.xcolor_options:
            requires_pkg.xcolor_options.append('dvipsnames')
    else:
        raise ValueError('Unknown color name: {}. Only colors from '
                         'xcolor\'s dvipsnames are yet supported.'
                         .format(value))
