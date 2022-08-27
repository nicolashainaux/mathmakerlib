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


def init():
    global package, options, tikz_library, tikzset
    global required_initialized

    try:
        required_initialized
    except NameError:
        required_initialized = False

    if not required_initialized:
        required_initialized = True
        # It's difficult to track amssymb, that could show up almost anywhere.
        # This is left to mathmakerlib's user. A (yet short) list of symbols is
        # provided in LaTeX module.
        package = {pkg_name: False
                   for pkg_name in ['tikz', 'siunitx', 'xcolor', 'eurosym',
                                    'amsmath', 'stackengine', 'scalerel',
                                    'cancel', 'multicol', 'placeins', 'ulem',
                                    'textcomp', 'array', 'graphicx',
                                    'epstopdf', 'textpos', 'fancyvrb']}
        options = {'xcolor': set(), 'textpos': set()}
        tikz_library = {'angles': False,
                        'decorations.markings': False,
                        'quotes': False}
        tikzset = {'singledash_hatchmark': False,
                   'doubledash_hatchmark': False,
                   'tripledash_hatchmark': False}
        # hack = {'rightangle_mark': False}
