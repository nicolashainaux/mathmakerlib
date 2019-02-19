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

import pytest

from mathmakerlib.geometry import Point, Polyhedron, Triangle, LineSegment


class Tetrahedron(Polyhedron):
    def _init_faces(self):
        self._faces = [Triangle(self.vertices[0], self.vertices[1],
                                self.vertices[2]),
                       Triangle(self.vertices[0], self.vertices[2],
                                self.vertices[3]),
                       Triangle(self.vertices[0], self.vertices[3],
                                self.vertices[1]),
                       Triangle(self.vertices[1], self.vertices[2],
                                self.vertices[3])
                       ]


def test_instanciation_errors():
    """Check errors when instanciating a new Polyhedron."""
    with pytest.raises(ValueError) as excinfo:
        Tetrahedron(Point(0, 0, 0), Point(1, 0, 0))
    assert str(excinfo.value) == 'At least four Points are required to be '\
        'able to build a Polyhedron. Found only 2 positional arguments, '\
        'though.'
    with pytest.raises(TypeError) as excinfo:
        Tetrahedron(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0),
                    'Point(0, 0, 1)')
    assert str(excinfo.value) == 'Only Points must be provided in order to '\
        'build a Polyhedron. Yet found <class \'str\'> as positional '\
        'argument #3.'
    Point.reset_names()
    with pytest.raises(TypeError) as excinfo:
        Tetrahedron(Point(0, 0), Point(1, 0, 0), Point(0, 1, 0),
                    Point(0, 0, 1))
    assert str(excinfo.value) == 'Points used to build a Polyhedron must '\
        'be three-dimensional Points. Found a two-dimensional Point '\
        'instead: Point A(0, 0).'
    with pytest.raises(TypeError) as excinfo:
        Tetrahedron(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0),
                    Point(0, 0, 1), name=1234)
    assert str(excinfo.value) == 'name must be a str, found 1234 instead.'
    with pytest.raises(ValueError) as excinfo:
        Tetrahedron(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0),
                    Point(0, 0, 1), name='ABCDE')
    assert str(excinfo.value) == 'A polyhedron\'s name must contain as many '\
        'letters as the polyhedron\'s number of vertices, yet found 5 '\
        'letters (name: \'ABCDE\') and 4 vertices.'
    with pytest.raises(TypeError) as excinfo:
        Tetrahedron(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0),
                    Point(0, 0, 1), draw_vertices=1)
    assert str(excinfo.value) == 'draw_vertices must be a boolean; ' \
        'got <class \'int\'> instead.'
    with pytest.raises(TypeError) as excinfo:
        Tetrahedron(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0),
                    Point(0, 0, 1), label_vertices=0)
    assert str(excinfo.value) == 'label_vertices must be a boolean; ' \
        'got <class \'int\'> instead.'


def test_instanciation():
    """Check new Polyhedrons instanciations."""
    Point.reset_names()
    t = Tetrahedron(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0),
                    Point(0, 0, 1))
    assert t.name == 'ABCD'
    assert t.label_vertices
    assert not t.draw_vertices
    assert t.vertices == [Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0),
                          Point(0, 0, 1)]
    assert t.edges == [LineSegment(Point(0, 0, 0), Point(1, 0, 0)),
                       LineSegment(Point(1, 0, 0), Point(0, 1, 0)),
                       LineSegment(Point(0, 1, 0), Point(0, 0, 0)),
                       LineSegment(Point(0, 1, 0), Point(0, 0, 1)),
                       LineSegment(Point(0, 0, 1), Point(0, 0, 0)),
                       LineSegment(Point(0, 0, 1), Point(1, 0, 0))]
    assert t.faces == [Triangle(Point(0, 0, 0, 'A'), Point(1, 0, 0, 'B'),
                                Point(0, 1, 0, 'C')),
                       Triangle(Point(0, 0, 0, 'A'), Point(0, 1, 0, 'C'),
                                Point(0, 0, 1, 'D')),
                       Triangle(Point(0, 0, 0, 'A'), Point(0, 0, 1, 'D'),
                                Point(1, 0, 0, 'B')),
                       Triangle(Point(1, 0, 0, 'B'), Point(0, 1, 0, 'C'),
                                Point(0, 0, 1, 'D'))]
    Point.reset_names()
    t = Tetrahedron(Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0),
                    Point(0, 0, 1), name='SABC')
    assert t.name == 'SABC'
    t = Tetrahedron(Point(0, 0, 0, label='?'), Point(1, 0, 0), Point(0, 1, 0),
                    Point(0, 0, 1), name='SABC')
