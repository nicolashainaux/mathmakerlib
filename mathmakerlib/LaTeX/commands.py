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

from . import AttrList, OptionsList


class Command(object):

    def __init__(self, name, content=None, options=None):
        self._name = str(name)
        if isinstance(content, (tuple, list)):
            self._content = AttrList(*content)
        else:
            self._content = AttrList(content)
        if isinstance(options, (tuple, list)):
            self._options = OptionsList(*options)
        else:
            self._options = OptionsList(options)

    def __str__(self):
        return r'\{name}{options}{content}'.format(name=self._name,
                                                   options=str(self._options),
                                                   content=str(self._content))

    @property
    def content(self):
        return self._content

    @property
    def options(self):
        return self._options


class DocumentClass(Command):

    def __init__(self, content=None, options=None):
        super().__init__('documentclass', content=content, options=options)


class UsePackage(Command):

    def __init__(self, content=None, options=None):
        super().__init__('usepackage', content=content, options=options)


class UseTikzLibrary(Command):

    def __init__(self, content=None, options=None):
        super().__init__('usetikzlibrary', content=content, options=options)
