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


class AttrList(object):

    def __init__(self, *attrlist, braces='{}'):
        if all([o is None for o in attrlist]):
            attrlist = None
        if (attrlist is not None and len(attrlist) == 1
            and isinstance(attrlist[0], AttrList)):
            self._content = attrlist[0]._content
            self._braces = attrlist[0]._braces
        else:
            self._content = attrlist
            self._braces = braces

    def __str__(self):
        if self._content is None or not len(self._content):
            return ''
        built_content = []
        for o in self._content:
            if isinstance(o, (tuple, list)):
                built_content.append('{}={}'.format(str(o[0]), str(o[1])))
            else:
                built_content.append(str(o))
        return '{}{}{}'.format(self._braces[0],
                               ', '.join(built_content),
                               self._braces[1])


class OptionsList(AttrList):

    def __init__(self, *options):
        super().__init__(*options, braces='[]')
