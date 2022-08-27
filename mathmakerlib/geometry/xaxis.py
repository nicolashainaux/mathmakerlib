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

from mathmakerlib import required
from mathmakerlib.calculus.number import Number
from mathmakerlib.calculus.fraction import Fraction
from mathmakerlib.core.drawable import Drawable, HasThickness
from mathmakerlib.geometry.point import Point
from mathmakerlib.geometry.bipoint import Bipoint


class XAxis(Drawable, HasThickness, Bipoint):

    def __init__(self, mini, maxi, allow_zero_length=False, length=8, step=1,
                 subdivisions=1, before=None, after=2, thickness='thick',
                 points_def=None):
        """
        Initialize XAxis.

        :param mini: the value of the first shown axis' graduation
        :type mini: any Number (int or whatever can be fed to Number())
        :param maxi: the value of the last shown axis' graduation
        :type maxi: any Number (int or whatever can be fed to Number())
        :param thickness: the XAxis' thickness. Available values are TikZ's
        ones.
        :type thickness: str
        :param step: the value between two main graduations
        :type step: any Number (int or whatever can be fed to Number())
        :param subdivisions: number of subdivisions between the main
        graduations. 1 means no subdivisions, 2 means the main graduations will
        be divided in halves, 3 in thirds etc.
        :type subdvisions: int >= 1
        :param before: number of subdivisions ahead of the first main
        graduation.
        :type before: int
        :param after: number of subdivisions after the first main graduation
        :type after: int
        :param length: the length of the axis
        :type length: any Number (int or whatever can be fed to Number())
        :param allow_zero_length: whether creation of a zero length axis is
        allowed or not (default False)
        :type allow_zero_length: bool
        :param points_def: a list of pairs (abscissa, name) of the points to be
        drawn on the axis. The abscissae to provide must match points of the
        axis. If an abscissa is outside [mini - before, maxi + after], it
        will be dropped with a warning.
        :type points_def: None or a list
        """
        mini = Number(mini)
        maxi = Number(maxi)
        step = Number(step)
        length = Number(length)
        # extra graduation that won't be drawn, to leave some space
        # between the last drawn graduation and the arrow
        after += 1
        endpoints = [Point(x=0, y=0), Point(x=length, y=0)]
        Bipoint.__init__(self, *endpoints, allow_zero_length=allow_zero_length)
        if before is None:
            if mini == 0:
                before = 0
            else:  # mini > 0
                if subdivisions in [1, 2]:
                    before = 2
                else:  # subdivisions >= 3
                    before = 3
        # mg = main graduations
        # sg = sub graduations
        mg_number = int((maxi - mini) / step)
        sg_number = int(before + mg_number * subdivisions + after)
        all_sg = self.dividing_points(n=sg_number)
        self._sg_abscissae = [p.x.rounded(Number('1.00')) for p in all_sg]
        sub_multiples = [i for i in range(sg_number) if not (i % subdivisions)]
        mg_indices = [n + before - 1 for n in sub_multiples]
        mg_indices = [i for i in mg_indices if i < len(all_sg)]
        if before == 0:
            all_sg.append(Point(0, 0))
        self._mg_abscissae = [all_sg[i].x.rounded(Number('1.00'))
                              for i in mg_indices]
        self._mg_labels = [Number(mini + n * step).printed
                           for n in range(mg_number + 1)]
        if points_def is None:
            points_def = []
        sg_step = step / subdivisions
        m = mini - before * sg_step
        # TODO: check there are no abscissae outside the drawn part of the axis
        abscissae = [x.evaluate()
                     if isinstance(x, Fraction) else Number(x).evaluate()
                     for (x, _) in points_def]
        abscissae = [(x.evaluate() - m) * length / (sg_step * sg_number)
                     for x in abscissae]
        names = [n for (_, n) in points_def]
        points_def = zip(abscissae, names)
        self._points = [Point(x=abscissa.rounded(Number('1.00')), y=0, name=n,
                              label_position='above')
                        for (abscissa, n) in points_def]
        self._length = Number(length)

    @property
    def template_fmt(self):
        sg_abscissae = ','.join([a.imprint(dot=True)
                                 for a in self._sg_abscissae])
        # do not leave commas in the labels to be printed, it will mess up
        # the axis (because TiKZ already uses commas to separate the values)
        if any([',' in label for label in self._mg_labels]):
            mg_abscissae_texts = \
                ','.join([f'{x}/{{{lab}}}'
                          for (x, lab) in zip(self._mg_abscissae,
                                              self._mg_labels)])
        else:
            mg_abscissae_texts = \
                ','.join([f'{x}/{lab}' for (x, lab) in zip(self._mg_abscissae,
                                                           self._mg_labels)])
        points_drawn = [(r'\draw[thick] ({x},0) node {{$\times$}} '
                         r'node[{lbl_pos}] {{{name}}};')
                        .format(x=p.x, lbl_pos=p.label_position, name=p.name)
                        for p in self._points]
        return {'__TIKZ_PICTURE_OPTIONS__': self.tikz_picture_options(),
                '__LENGTH__': self._length.imprint(dot=True),
                '__SG_ABSCISSAE__': '{' + sg_abscissae + '}',
                '__MG_ABSCISSAE_TEXTS__': '{' + mg_abscissae_texts + '}',
                '__POINTS_DRAWN__': '\n'.join(points_drawn)
                }

    def draw(self):
        required.package['tikz'] = True
        pic = (Path(__file__).parent / 'templates/xaxis.tex').read_text()
        for placeholder in self.template_fmt:
            pic = pic.replace(placeholder, self.template_fmt[placeholder])
        return pic

    def _tikz_draw_options(self):
        pass

    def tikz_declarations(self):
        pass

    def tikz_draw(self):
        pass

    def tikz_drawing_comment(self):
        pass

    def tikz_label(self):
        return ''

    def tikz_points_labels(self):
        pass
