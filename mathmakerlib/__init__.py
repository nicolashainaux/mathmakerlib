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

from pathlib import Path

import toml

from . import required, exceptions, config, constants
from . import calculus, core, geometry, LaTeX

__all__ = ['required', 'config', 'LaTeX', 'exceptions', 'constants',
           'core', 'calculus', 'geometry']

with open(Path(__file__).parent.parent / 'pyproject.toml', 'r') as f:
    pp = toml.load(f)

__version__ = pp['tool']['poetry']['version']
__lib_name__ = pp['tool']['poetry']['name']

__release__ = __version__ + ' (alpha)'
__author__ = 'Nicolas Hainaux'
__author_email__ = 'nh.techn@gmail.com'
__licence__ = 'GNU General Public License v3 or later (GPLv3+)'
__url__ = 'https://gitlab.com/nicolas.hainaux/mathmakerlib/'
__copyright__ = 'Copyright 2006-2019'
__contact__ = '{author} <{author_email}>'\
              .format(author=__author__, author_email=__author_email__)
__licence_info__ = '{lib_ref} is free software. Its license is '\
                   '{lib_license}.'
__url_info__ = 'Further details on {lib_website}'
__info__ = '{lib_name} {r}\nLicense: {li}\n{c} {contact}'\
           .format(lib_name=__lib_name__,
                   r=__release__, li=__licence__, c=__copyright__,
                   contact=__contact__)

config.init()
required.init()
