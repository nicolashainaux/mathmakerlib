#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
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

import math
from decimal import Decimal

ANGLE = 35
MOD = 2.5
RADIAL_DISTANCE = '5.9cm'
SHORTEN = '3.4cm'

BISECTOR_START = 0
BISECTOR_END = 360
STEP = 5

ARMS_LENGTH = 6
RADIUS = '1cm'

TEXDOC = \
    r'''\RequirePackage{luatex85}
\documentclass[a4paper, fleqn, 12pt]{article}

\usepackage{lxfonts}
\usepackage{amsmath}
\usepackage{eurosym}

\usepackage[no-math]{fontspec}

%%% fixes in order to use lxfonts only for math
\let\savedrmdefault\rmdefault
\let\savedsfdefault\sfdefault
\let\savedttdefault\itdefault
\let\saveditdefault\itdefault
\let\savedsldefault\sldefault
\let\savedbxdefault\bxdefault
\AtEndPreamble{% undo the nonmath settings by lxfonts
  \let\rmdefault\savedrmdefault
  \let\sfdefault\savedsfdefault
  \let\ttdefault\saveditdefault
  \let\itdefault\saveditdefault
  \let\sldefault\savedsldefault
  \let\bxdefault\savedbxdefault
  \setmainfont{Ubuntu}[NFSSFamily=fontid]%
}
%%%

\DeclareSymbolFont{mynumbers}      {TU}{fontid}{m}{n}
\SetSymbolFont    {mynumbers}{bold}{TU}{fontid}{bx}{n}

\AtBeginDocument{
\DeclareMathSymbol{0}{\mathalpha}{mynumbers}{`0}
\DeclareMathSymbol{1}{\mathalpha}{mynumbers}{`1}
\DeclareMathSymbol{2}{\mathalpha}{mynumbers}{`2}
\DeclareMathSymbol{3}{\mathalpha}{mynumbers}{`3}
\DeclareMathSymbol{4}{\mathalpha}{mynumbers}{`4}
\DeclareMathSymbol{5}{\mathalpha}{mynumbers}{`5}
\DeclareMathSymbol{6}{\mathalpha}{mynumbers}{`6}
\DeclareMathSymbol{7}{\mathalpha}{mynumbers}{`7}
\DeclareMathSymbol{8}{\mathalpha}{mynumbers}{`8}
\DeclareMathSymbol{9}{\mathalpha}{mynumbers}{`9}
\DeclareMathSymbol{.}{\mathord}{mynumbers}{`.}
\DeclareMathSymbol{,}{\mathpunct}{mynumbers}{`,}
}

\usepackage{polyglossia}
\setmainlanguage{french}

\usepackage{siunitx}[=v2]
\newfontfamily\configfont{Ubuntu}

\AtBeginDocument{
\sisetup{mode=text, locale=FR, text-rm=\configfont}
}

\usepackage[dvipsnames]{xcolor}

\usepackage{tikz}
\usetikzlibrary{angles}
\usetikzlibrary{quotes}
\usetikzlibrary{arrows,scopes}
\usepackage[dvipsnames]{xcolor}
\usetikzlibrary{shapes.geometric, shapes.callouts, arrows.meta, positioning}

\tikzset{
callout_style1/.style={
rectangle callout, rounded corners=0.4cm,
minimum height=1.2cm, minimum width=1.6cm,
inner xsep=0.3cm, inner ysep=0.1cm}
}

\usepackage{array}

\usepackage{ulem}

\usepackage{geometry}

\geometry{hmargin=0.75cm, vmargin=0.75cm}
\setlength{\parindent}{0cm}
\setlength{\arrayrulewidth}{0.02pt}
\pagestyle{empty}
\newcounter{n}
\newcommand{\exercise}{\noindent \hspace{-.25cm} \stepcounter{n} '''\
    r'''\normalsize \textbf{Exercice \arabic{n}}
\newline \normalsize }
\newcommand{\razcompteur}{\setcounter{n}{0}}

\renewcommand{\parallel}{\mathbin{/\negthickspace/}}

\begin{document}
CONTENT
\end{document}'''


TEMPLATE = r'''\begin{tikzpicture}
% Declare Points
\coordinate (X) at (XX,XY);
\coordinate (O) at (0,0);
\coordinate (Y) at (YX,YY);

% Draw Angle
\draw pic[OliveGreen, fill=OliveGreen!30, draw, thick, '''\
    r'''angle radius=RADIUS] {angle = X--O--Y};
\draw [thick,round cap-round cap] (X) -- (O) -- (Y);
\node [callout absolute pointer=(O), callout_style1, '''\
    r'''callout pointer shorten=SHORTEN, fill=OliveGreen!20] '''\
    r'''at (POLAR_ANGLE:RADIAL_DISTANCE) {NUMBER° : \dots\dots\dots '''\
    r'''\vrule width 0pt height 0.5cm};
\end{tikzpicture}
'''

template = TEMPLATE.replace('RADIUS', RADIUS).replace('SHORTEN', SHORTEN)\
    .replace('RADIAL_DISTANCE', RADIAL_DISTANCE)
pictures = ''

alpha = ANGLE / 2
L = ARMS_LENGTH
table = []

# theta = bisector angle
for (i, theta) in enumerate(range(BISECTOR_START, BISECTOR_END + STEP, STEP)):
    xx = str(round(Decimal(str(L * math.cos(math.radians(theta - alpha)))), 3))
    xy = str(round(Decimal(str(L * math.sin(math.radians(theta - alpha)))), 3))
    yx = str(round(Decimal(str(L * math.cos(math.radians(theta + alpha)))), 3))
    yy = str(round(Decimal(str(L * math.sin(math.radians(theta + alpha)))), 3))
    # import sys
    # sys.stderr.write(f'\n{theta = }\n')
    mod_theta = theta - MOD * math.sin(math.radians(2 * theta))
    # if 0 <= theta % 90 < 45:
    #     mod_theta = theta - MOD \
    #         * math.pow(math.sin(math.radians(2 * theta % 90)), 0.33)
    # elif 45 <= theta % 90 < 90:
    #     mod_theta = theta + MOD \
    #         * math.pow(math.sin(math.radians(2 * (theta % 90 - 45))), 0.33)
    # mod_theta = theta - ((MOD / 45) * (45 - abs(theta % 90 - 45)))
    # mod_theta = theta -
    # # math.pow(((MOD / 45) * (45 - abs(theta % 90 - 45))), 2)
    table.append((theta, mod_theta))
    sep = r'\hspace{2cm}' if i % 2 else '\n'
    pictures += template.replace('XX', xx).replace('XY', xy).replace('YX', yx)\
        .replace('YY', yy).replace('POLAR_ANGLE', str(mod_theta))\
        .replace('NUMBER', str(theta)) + sep

print(TEXDOC.replace('CONTENT', pictures))

# import sys
# sys.stderr.write('\n'.join([f'{t[0]} {t[1]}' for t in table]))
