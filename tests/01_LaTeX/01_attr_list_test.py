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

from mathmakerlib.LaTeX import OptionsList, AttrList


def test_str():
    """Check turning options into str."""
    assert str(AttrList()) == ''
    assert str(OptionsList()) == ''
    assert str(OptionsList(None)) == ''
    assert str(OptionsList('usenames', 'dvipsnames'))\
        == '[usenames, dvipsnames]'
    assert str(OptionsList('20pt',
                           {'xcolor': AttrList('usenames', 'dvipsnames')}))\
        == '[20pt, xcolor={usenames, dvipsnames}]'
    assert str(OptionsList('a4paper', 'fleqn', '12pt'))\
        == '[a4paper, fleqn, 12pt]'
    ol = OptionsList('a4paper')
    ol.append('fleqn')
    assert str(ol) == '[a4paper, fleqn]'
    al = AttrList('usenames', 'dvipsnames')
    al2 = AttrList(al)
    assert str(al2) == '{usenames, dvipsnames}'
    al2.append('svgnames')
    assert str(al2) == '{usenames, dvipsnames, svgnames}'
