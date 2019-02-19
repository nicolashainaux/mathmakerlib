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

from mathmakerlib.LaTeX import Command, DocumentClass, UsePackage
from mathmakerlib.LaTeX import UseTikzLibrary, AttrList


def test_Command_class():
    """Check turning commands into str."""
    assert str(Command('RequirePackage', 'luatex85'))\
        == r'\RequirePackage{luatex85}'
    assert str(Command('sisetup',
                       content={'locale': 'FR', 'mode': 'text'}))\
        == r'\sisetup{locale=FR, mode=text}'
    assert str(Command('command',
                       content=['content1', 'content2']))\
        == r'\command{content1, content2}'
    assert str(Command('setkeys',
                       options=AttrList({'variant': 'british'}),
                       content='en'))\
        == r'\setkeys{variant=british}{en}'


def test_preset_commands():
    """Check turning preset commands into str."""
    dc = DocumentClass('article', options=('a4paper', 'fleqn', '12pt'))
    assert str(dc) == r'\documentclass[a4paper, fleqn, 12pt]{article}'
    assert str(dc.content) == '{article}'
    assert str(dc.options) == '[a4paper, fleqn, 12pt]'
    dc.options.append('landscape')
    assert str(dc.options) == '[a4paper, fleqn, 12pt, landscape]'
    assert str(UsePackage('lxfonts')) == r'\usepackage{lxfonts}'
    assert str(UsePackage('fontspec', options='no-math'))\
        == r'\usepackage[no-math]{fontspec}'
    assert str(UseTikzLibrary('calc')) == r'\usetikzlibrary{calc}'
    dc = DocumentClass('beamer', options='20pt')
    dc.options.append({'xcolor': AttrList(*['dvipsnames', 'svgnames'])})
    assert str(dc) == r'\documentclass[20pt, xcolor={dvipsnames, svgnames}]'\
        '{beamer}'
