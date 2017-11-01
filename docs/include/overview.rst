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
    >>>

You can also play with units. Basic operations are available:

::

    >>> n = Number(4, unit='cm')
    >>> n
    Number('4 cm')
    >>> str(n)
    '4 cm'
    >>> n.unit
    Unit('cm')
    >>> n.printed
    '\\SI{4}{cm}'
    >>> n + Number(6, unit='kg')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/nico/dev/mathmaker/mathmakerlib/mathmakerlib/calculus/number.py", line 177, in __add__
        other_unit))
    ValueError: Cannot add two Numbers having different Units (cm and kg).
    >>> n * Number(6, unit='cm')
    Number('24 cm^2')
    >>>


Contribute
==========

Before submitting a PR, please ensure you've had a look at the mathmaker's `writing rules <http://mathmaker.readthedocs.io/en/dev/dev_doc.html#writing-rules>`_.

So far, more details can be found in the `documentation for developers of mathmaker <http://mathmakerlib.readthedocs.io/en/dev/dev_index.html>`__.

Any question can be sent to nh dot techn (hosted at gmail dot com).

.. include:: ../CONTRIBUTORS.rst

.. include:: ../CHANGELOG.rst
