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

"""Constants and LaTeX-related stuff."""


from .attr_list import AttrList, OptionsList
from .commands import Command, DocumentClass, UsePackage, UseTikzLibrary
from .environment import Environment, TikZPicture

DEFAULT_FONT_SIZES = [r'\tiny', r'\scriptsize', r'\footnotesize', r'\small',
                      r'\normalsize', r'\large', r'\Large', r'\LARGE',
                      r'\huge', r'\Huge']

DEFAULT_COLOR_NAMES = ['white', 'black', 'red', 'green', 'blue', 'cyan',
                       'magenta', 'yellow']

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

TIKZSET = {'singledash_hatchmark': r"""
\tikzset{singledash/.style={decoration={ markings, mark= at position 0.5
with { \draw (0pt,-2.5pt) -- (0pt,2.5pt);
} }, pic actions/.append code=\tikzset{postaction=decorate}}}""",
           'doubledash_hatchmark': r"""
\tikzset{doubledash/.style={decoration={ markings, mark= at position 0.5
with { \draw (-1pt,-2.5pt) -- (-1pt,2.5pt);
       \draw (1pt,-2.5pt) -- (1pt,2.5pt);
} }, pic actions/.append code=\tikzset{postaction=decorate}}}""",
           'tripledash_hatchmark': r"""
\tikzset{tripledash/.style={decoration={ markings, mark= at position 0.5
with { \draw (-2pt,-2.5pt) -- (-2pt,2.5pt);
       \draw (0pt,-2.5pt) -- (0pt,2.5pt);
       \draw (2pt,-2.5pt) -- (2pt,2.5pt);
} }, pic actions/.append code=\tikzset{postaction=decorate}}}"""
           }

MATHEMATICAL_NOTATIONS = \
    {'en': {'angle_name': r'\angle {content}'},
     'fr': {'angle_name': r'\stackon[-5pt]{{{content}}}{{\vstretch{{1.5}}'
                          r'{{\hstretch{{1.6}}{{\widehat{{\phantom{{\;\;\;\;'
                          r'}}}}}}}}}}'}
     }

KNOWN_AMSSYMB_SYMBOLS = [r'\triangle', r'\square', r'\lozenge', r'\bigstar']
KNOWN_AMSMATH_SYMBOLS = [r'\text{', r'\negthickspace', r'\dfrac', r'\tfrac',
                         r'\mathstrut']

KNOWN_TEXTCOMP_SYMBOLS = [r'\textdegree', r'\textdollar', r'\textsterling']

THICKNESS_VALUES = [None, 'thin', 'very thin', 'ultra thin', 'thick',
                    'very thick', 'ultra thick']

ARROW_TIPS = [None, '<->', '<-', '->', '-']

DASHPATTERN_VALUES = ['solid', 'dotted', 'densely dotted', 'loosely dotted',
                      'dashed', 'densely dashed', 'loosely dashed',
                      'dash dot', 'densely dash dot', 'loosely dash dot',
                      'dash dot dot', 'densely dash dot dot',
                      'loosely dash dot dot']

__all__ = [AttrList, OptionsList, Command, DocumentClass, UsePackage,
           UseTikzLibrary, Environment, TikZPicture]
