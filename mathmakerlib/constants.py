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
