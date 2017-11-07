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

    def draw(self):
        """
        Return the LaTeX (tikz) string of the object.

        The drawing must be made based on the object's properties, no extra
        argument is required. First, setup the object (at initialization, or
        modify it later), once it's ready, draw it.
        """
        import sys
        pkg_required.tikz = True
        picture_format = {'header': self.tikz_header(),
                          'declaring_comment': self.tikz_declaring_comment(),
                          'declarations': self.tikz_declarations(),
                          'labeling_comment': self.tikz_labeling_comment(),
                          'labels': self.tikz_label()}
        drawing_section = ''
        for (i, (c, d)) in enumerate(zip(self.tikz_drawing_comment(),
                                         self.tikz_draw())):
            sys.stderr.write('\n1st step: {}\n'
                             .format('{{drawing_comment{}}}\n{{drawing{}}}\n'
                                     .format(i, i)))
            drawing_section += ('{{drawing_comment{}}}\n{{drawing{}}}\n'
                                .format(i, i))\
                .format(**{'drawing_comment{}'.format(i): c,
                           'drawing{}'.format(i): d})
        picture_format.update({'drawing_section': drawing_section})
        sys.stderr.write('\nfmt= {}\n'.format(picture_format))
        return r"""
\begin{{tikzpicture}}{header}
{declaring_comment}
{declarations}

{drawing_section}
{labeling_comment}
{labels}
\end{{tikzpicture}}
""".format(**picture_format)

    def tikz_header(self):
        r"""
        Can be overriden to define some setup here.

        Take care, if you actually override it, to start with a \n, to avoid
        starting displaying it right after the \begin.
        """
        return ''

    def tikz_declaring_comment(self):
        """
        Default declaring comment, '% Declare Points'.

        :rtype: str
        """
        return '% Declare Points'

    @abstractmethod
    def tikz_declarations(self):
        """
        Return the necessary declarations (e.g. Points declarations).

        :rtype: str
        """

    @abstractmethod
    def tikz_drawing_comment(self):
        """
        Return the comments matching each drawing category.

        :rtype: list
        """

    @abstractmethod
    def tikz_draw(self):
        """
        Return the commands to actually draw the object.

        They should be grouped in categories (the Points, the Segments etc.).
        Caution, this method must return a list (containing one string per
        category). tikz_drawing_comment() must return a list containing as many
        elements as this one.

        :rtype: list
        """

    def tikz_labeling_comment(self):
        """Default labeling comment, '% Label Points'."""
        return '% Label Points'

    @abstractmethod
    def tikz_label(self):
        """Return the command to write the object's label."""

    @property
    def drawn(self):
        """self.drawn is same as self.draw() (no arguments)."""
        return self.draw()

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, other):
        if other in ['', None]:
            self._label = None
        else:
            self._label = str(other)
