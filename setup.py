#!/usr/bin/env python
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

import sys
import os
from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand

from mathmakerlib import __version__, __lib_name__, __licence__
from mathmakerlib import __author__, __author_email__, __url__


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


class CleanCommand(Command):
    """
    Custom clean command to tidy up the project root.

    Taken from http://stackoverflow.com/questions/3779915/why-does-python-
    setup-py-sdist-create-unwanted-project-egg-info-in-project-r
    """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info '
                  './*.egg')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


class Tox(TestCommand):
    # user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


setup(
    name=__lib_name__,
    version=__version__,
    url=__url__,
    license=__licence__,
    author=__author__,
    tests_require=['tox'],
    cmdclass={'test': PyTest,
              'tox': Tox,
              'clean': CleanCommand},
    author_email=__author_email__,
    description='Mathmaker Lib offers lualatex-printable mathematical '
    'objects. Geometric shapes are created using TikZ.',
    long_description=read('README.rst', 'CHANGELOG.rst', 'CONTRIBUTORS.rst'),
    packages=find_packages(exclude=['tests', 'docs']),
    include_package_data=True,
    platforms='any',
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: ' + __licence__,
        'Topic :: Education :: Computer Aided Instruction (CAI)',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX :: BSD :: FreeBSD'],
    extras_require={'testing': ['pytest']}
)
