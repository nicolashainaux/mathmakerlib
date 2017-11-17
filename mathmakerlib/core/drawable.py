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

from mathmakerlib import requires_pkg, colors_names
from mathmakerlib.calculus.tools import is_number


class Drawable(object, metaclass=ABCMeta):

    def draw(self):
        """
        Return the LaTeX (tikz) string of the object.

        The drawing must be made based on the object's properties, no extra
        argument is required. First, setup the object (at initialization, or
        modify it later), once it's ready, draw it.
        """
        requires_pkg.tikz = True
        picture_format = {'header': self.tikz_header(),
                          'declaring_comment': self.tikz_declaring_comment(),
                          'declarations': self.tikz_declarations(),
                          'labeling_comment': self.tikz_labeling_comment(),
                          'labels': self.tikz_label()}
        drawing_section = ''
        for (i, (c, d)) in enumerate(zip(self.tikz_drawing_comment(),
                                         self.tikz_draw())):
            drawing_section += ('{{drawing_comment{}}}\n{{drawing{}}}\n'
                                .format(i, i))\
                .format(**{'drawing_comment{}'.format(i): c,
                           'drawing{}'.format(i): d})
        picture_format.update({'drawing_section': drawing_section})
        # Prepare possible picture's options
        scale_option = ''
        if self.scale != 1:
            scale_option = 'scale={}'.format(self.scale)
        baseline_option = ''
        if self.baseline is not None:
            baseline_option = 'baseline={}'.format(self.baseline)
        pic_options_list = [_
                            for _ in [baseline_option, scale_option]
                            if _ != '']
        pic_options = ', '.join(pic_options_list)
        if pic_options:
            pic_options = '[{}]'.format(pic_options)
        picture_format.update({'pic_options': pic_options})
        return r"""
\begin{{tikzpicture}}{pic_options}{header}
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
    def _tikz_draw_options(self):
        """
        The list of possible options for draw command.

        :rtype: list
        """

    def tikz_options_list(self, options_list):
        """
        Return '[opt1, opt2,...]' or '' (if all options are None).

        :rtype: str
        """
        options = []
        if options_list == 'draw':
            options_list = self._tikz_draw_options()
        for o in options_list:
            if o is not None:
                options.append(o)
        if options:
            return '[{}]'.format(', '.join(options))
        else:
            return ''

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

    @property
    def scale(self):
        if not hasattr(self, '_scale'):
            return 1
        else:
            return self._scale

    @scale.setter
    def scale(self, other):
        if not is_number(other):
            raise TypeError('The scale must be a number.')
        setattr(self, '_scale', other)

    @property
    def baseline(self):
        if not hasattr(self, '_baseline'):
            return None
        else:
            return self._baseline

    @baseline.setter
    def baseline(self, value):
        setattr(self, '_baseline', str(value))

    @property
    def color(self):
        if not hasattr(self, '_color'):
            return None
        else:
            return self._color

    @color.setter
    def color(self, value):
        colors_names.check(value)
        setattr(self, '_color', value)
