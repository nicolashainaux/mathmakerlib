Overview
========

Mathmaker Lib offers python objects to create mathematical expressions or
geometric figures to print as LaTeX. These objects can also be used to create
detailed calculations, like equations resolutions or expressions expansions.

`License <https://github.com/nicolashainaux/mathmakerlib/blob/master/LICENSE>`__

Quickstart
==========

Install
-------

OS requirement: Linux, FreeBSD or Windows.

The required python version to use Mathmaker Lib is python>=3.6.
You'll need to install it if it's not already on your system.

::

    $ pip3 install mathmakerlib

Basic use
---------

::

    >>> from mathmakerlib.calculus.number import Number
    >>> Number('5.807')
    Number('5.807')
    >>> Number('5.807').atomized()
    [Number('5'), Number('0.8'), Number('0.007')]
    >>> Number('150').is_power_of_10()
    False
    >>> Number('0.001').is_power_of_10()
    True


Contribute
==========

Before submitting a PR, please ensure you've had a look at the mathmaker's `writing rules <http://mathmaker.readthedocs.io/en/dev/dev_doc.html#writing-rules>`_.

So far, more details can be found in the `documentation for developers of mathmaker <http://mathmakerlib.readthedocs.io/en/dev/dev_index.html>`__.

Any question can be sent to nh dot techn (hosted at gmail dot com).

.. include:: ../CONTRIBUTORS.rst

.. include:: ../CHANGELOG.rst
