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

from abc import ABCMeta, abstractmethod

from mathmakerlib import pkg_required


class Drawable(object, metaclass=ABCMeta):

    def draw(self, **kwargs):
        """
        Return the LaTeX (tikz) string of the object.
        """
        pkg_required.tikz = True
        return r"""
\begin{{tikzpicture}}{header}
% Definitions
{definition}

% Drawing
{drawing}

% Labels
{label}
\end{{tikzpicture}}
""".format(header=self.tikz_header(**kwargs),
           definition=self.tikz_definition(**kwargs),
           drawing=self.tikz_draw(**kwargs),
           label=self.tikz_label(**kwargs))

    def tikz_header(self, **kwargs):
        r"""
        Can be overriden to defined some setup here.

        Take care, if you actually override it, to start with a \n, to avoid
        starting displaying it right after the \begin.
        """
        return ''

    @abstractmethod
    def tikz_definition(self, **kwargs):
        """Return the necessary definitions (e. g. Points)."""

    @abstractmethod
    def tikz_draw(self, **kwargs):
        """Return the command to actually draw the object."""

    @abstractmethod
    def tikz_label(self, **kwargs):
        """Return the command to write the object's label."""

    @property
    def drawn(self):
        """self.drawn is same as self.draw() (no arguments)."""
        return self.draw()

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, L):
        self._label = str(L)
