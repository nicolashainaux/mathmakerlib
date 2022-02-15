Changelog
=========

Version 0.7 (2018-06-18)
------------------------

* Now Points, as well as other basic geometric objects, may be 2D or 3D.
* Add first three-dimensional objects: Polyhedron and RightCuboid.
* Add first flat representation of polyhedra: ObliqueProjection
* Extend units conversions to areas, volumes and conversions between capacities and volumes (from m³ to mm³).
* Add ClockTime object to easily deal with times.
* Accept floats to initialize Numbers (the float being converted to str).

Patches 0.7.1, 0.7.2, 0.7.3 and 0.7.4 (2018-11-16, 2018-11-20, 2019-02-20 and 2019-02-22)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Fix Number.rounded() for precisions greater than 10 (e.g. 10, 100, 1000 etc.)
* Add Number.highest_digitplace() and Number.estimation()
* Add 'siunitx' variant keyword value to Number.imprint() (in order to print numbers as \\num{...})
* Modify ClockTime object's context.
* Include a logo.
* Bugfix.

Patches 0.7.5 to 0.7.8 (2022-02-11 and 2022-02-15)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Add XAxis object.
* Some cleanup.

Version 0.6 (2018-04-12)
------------------------

* A standalone Angle or AnglesSet can be drawn. Enrich Angles' decorations (hatch marks, labeling, second decoration etc.).
* An integer Number can be split as a sum of integers ± 0.5 (or ± 0.25)
* Add Number.lowest_nonzero_digit_index()
* Patch Number.split() to get a consistent behaviour for integers too (default split will be done at lowest non zero digit place: 500 will be split as 100 + 400, or 200 + 300 etc. and with dig=1, it will be split as 10 + 490, or 20 + 480 etc.).
* Fix: Numbers with an angle's unit should be displayed as \\ang{...} rather than \\SI{...}{\\textdegree}.
* Add basic classes to handle LaTeX commands and options' lists.

Patches 0.6.1 to 0.6.4 (2018-04-13, 2018-04-30, 2018-05-02 and 2018-05-05)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Add a constant in LaTeX module
* Add Number.digits_sum()
* Add Number.digits and Number.digit()
* Add some amsmath symbols.

Version 0.5 (2018-01-10)
------------------------

* Add Number.quantize().
* A Number can be converted into a another unit of the same physical quantity.
* Accept int as exponent (or even content) of an Exponented.
* Fractions can be created from a decimal Number.
* Fractions become Evaluable and can be compared to other numbers.
* Standalone Units will be printed using siunitx (e.g. as '\\si{cm}').
* Fix bug: current locale is ignored when printing a number having a unit.
* Do not automatically remove possible trailing zeros when printing a Number.
* Add the tonne (t) as mass unit.
* An optional patch allow Polygons to be drawn to the first vertex again instead of only cycling (default behaviour).


Version 0.4 (2017-12-19)
------------------------

* Add more complex geometric objects: Polygon, Triangle, RightTriangle, EquilateralTriangle, IsoscelesTriangle, Quadrilateral, Rhombus, Rectangle, Square.
* Numbers can be "copied" using copy.copy() or copy.deepcopy().
* Add Point.rotate().
* Add the ability to change the size of Point's drawn shape (using Point.shape_scale).
* Add LineSegment.mark and the ability to change its size (using LineSegment.mark_scale).
* mathmakerlib.requires_pkg becomes mathmakerlib.required and will also handle required options and hacks.
* Add module mathmakerlib.mmlib_setup to configure the behaviour (default values etc.).

Patch 0.4.1 (2018-01-01)
^^^^^^^^^^^^^^^^^^^^^^^^

* Fix the locale monkey patch.

Version 0.3 (2017-11-17)
------------------------

* Add basic geometric objects: Point, LineSegment and DividedLineSegment.
* Add Fraction.
* Add module mathmakerlib.requires_pkg that tells which LaTeX packages will be required to compile the document (like tikz, xcolor, siunitx...).

Version 0.2 (2017-11-01)
------------------------

* Add Sign, Exponented and Unit classes.
* Numbers are now Signed objects and may be assigned a Unit.

Patches 0.2.1 and 0.2.2 (2017-11-02)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Bring back Numbers' hashability.
* Add physical_quantity() in unit module.

Initial version 0.1 (2017-10-24)
---------------------------------

* Number class and decimal numbers' related functions.
