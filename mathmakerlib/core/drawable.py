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

from decimal import Decimal, InvalidOperation
from abc import ABCMeta, abstractmethod

from mathmakerlib import required, colors_names
from mathmakerlib.core.printable import Printable
from mathmakerlib.calculus.tools import is_number
from mathmakerlib.calculus.number import Number


THICKNESS_VALUES = [None, 'thin', 'very thin', 'ultra thin', 'thick',
                    'very thick', 'ultra thick']


def check_color(value):
    if (value is None or value in colors_names.LATEX
        or value in colors_names.XCOLOR_BASE):
        # Base LaTeX colors do not need to be explicitely loaded.
        # As tikz package already loads xcolor base names, it's not
        # necessary to explicitely load them neither.
        pass
    elif value in colors_names.XCOLOR_DVIPSNAMES:
        required.package['xcolor'] = True
        if 'dvipsnames' not in required.options['xcolor']:
            required.options['xcolor'].append('dvipsnames')
    else:
        raise ValueError('Unknown color name: {}. Only colors from '
                         'xcolor\'s dvipsnames are yet supported.'
                         .format(value))


def check_scale(value, source_name):
    if not is_number(value):
        raise TypeError('The {}\'s scale must be a number.'
                        .format(source_name))


def tikz_approx_position(slope):
    if (Decimal('337.5') <= slope <= Decimal('360')
        or Decimal('0') <= slope < Decimal('22.5')):
        return 'right'
    elif Decimal('22.5') <= slope < Decimal('67.5'):
        return 'above right'
    elif Decimal('67.5') <= slope < Decimal('112.5'):
        return 'above'
    elif Decimal('112.5') <= slope < Decimal('157.5'):
        return 'above left'
    elif Decimal('157.5') <= slope < Decimal('202.5'):
        return 'left'
    elif Decimal('202.5') <= slope < Decimal('247.5'):
        return 'below left'
    elif Decimal('247.5') <= slope < Decimal('292.5'):
        return 'below'
    elif Decimal('292.5') <= slope < Decimal('337.5'):
        return 'below right'


def tikz_options_list(options_list, source=None):
    """
    Return '[opt1, opt2,...]' or '' (if all options are None).

    :param options_list: a str keyword (available so far: 'draw') or a list of
    strings (or None)
    :type options_list: list
    :param source: used if options_list is a keyword instead of a list
    :type source: if options_list is 'draw', source must be a Drawable
    :rtype: str
    """
    options = []
    if options_list == 'draw':
        if not isinstance(source, Drawable):
            raise TypeError('Expected a Drawable, found {}.'
                            .format(type(source)))
        options_list = source._tikz_draw_options()
    for o in options_list:
        if o is not None:
            options.append(o)
    if options:
        return '[{}]'.format(', '.join(options))
    else:
        return ''


class Colored(object, metaclass=ABCMeta):
    @property
    def color(self):
        if not hasattr(self, '_color'):
            return None
        else:
            return self._color

    @color.setter
    def color(self, value):
        check_color(value)
        setattr(self, '_color', value)


class HasRadius(object, metaclass=ABCMeta):
    @property
    def radius(self):
        if not hasattr(self, '_radius'):
            return None
        return self._radius

    @radius.setter
    def radius(self, value):
        from mathmakerlib.calculus.number import Number
        if is_number(value):
            self._radius = Number(value)
        else:
            raise TypeError('Expected a number as radius. Got {} instead.'
                            .format(str(type(value))))


class HasThickness(object, metaclass=ABCMeta):
    @property
    def thickness(self):
        if not hasattr(self, '_thickness'):
            return None
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        if value in THICKNESS_VALUES:
            self._thickness = value
        else:
            raise ValueError('Incorrect thickness value: \'{}\'. '
                             'Available values belong to: {}.'
                             .format(str(value), str(THICKNESS_VALUES)))


class Drawable(Colored, metaclass=ABCMeta):

    def draw(self):
        """
        Return the LaTeX (tikz) string of the object.

        The drawing must be made based on the object's properties, no extra
        argument is required. First, setup the object (at initialization, or
        modify it later), once it's ready, draw it.
        """
        required.package['tikz'] = True
        picture_format = {'header': self.tikz_header(),
                          'declaring_comment': self.tikz_declaring_comment(),
                          'declarations': self.tikz_declarations(),
                          'labeling_comment': self.tikz_labeling_comment(),
                          'labels': self.tikz_points_labels()}
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
        boundingbox_section = ''
        if self.boundingbox is not None:
            boundingbox_section = '\n\n' \
                + (r'\useasboundingbox ({},{}) rectangle ({},{});'
                   .format(*self.boundingbox))

        picture_format.update({'boundingbox_section': boundingbox_section})
        return r"""
\begin{{tikzpicture}}{pic_options}{header}
{declaring_comment}
{declarations}

{drawing_section}
{labeling_comment}
{labels}{boundingbox_section}
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

    @abstractmethod
    def tikz_points_labels(self):
        """Return the command to write the object's points' labels."""

    @property
    def drawn(self):
        """self.drawn is same as self.draw() (no arguments)."""
        return self.draw()

    @property
    def label_value(self):
        return self._label_value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        if value in ['', None]:
            self._label = self._label_value = None
        elif isinstance(value, Printable):
            self._label = value.uiprinted
            self._label_value = value
        else:
            self._label = self._label_value = str(value)

    @property
    def scale(self):
        if not hasattr(self, '_scale'):
            return 1
        else:
            return self._scale

    @scale.setter
    def scale(self, value):
        check_scale(value, 'picture')
        setattr(self, '_scale', value)

    @property
    def baseline(self):
        if not hasattr(self, '_baseline'):
            return None
        else:
            return self._baseline

    @baseline.setter
    def baseline(self, value):
        if value is not None:
            setattr(self, '_baseline', str(value))

    @property
    def boundingbox(self):
        if not hasattr(self, '_boundingbox'):
            return None
        else:
            return self._boundingbox

    @boundingbox.setter
    def boundingbox(self, value):
        if value is not None:
            if not isinstance(value, tuple):
                raise TypeError('Expected a tuple, found a {} instead.'
                                .format(type(value).__name__))
            if len(value) != 4:
                raise ValueError('Expected a tuple of 4 elements, found {} '
                                 'elements instead.'.format(len(value)))
            for v in value:
                try:
                    Number(v)
                except (TypeError, InvalidOperation):
                    raise TypeError('Expected a tuple containing only '
                                    'numbers. Found a {} instead.'
                                    .format(type(v).__name__))
            setattr(self, '_boundingbox', tuple(Number(v) for v in value))
