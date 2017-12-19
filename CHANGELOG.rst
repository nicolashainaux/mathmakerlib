Changelog
=========

Version 0.4 (2017-12-19)
-------------------------

* Add more complex geometric objects: Polygon, Triangle, RightTriangle, EquilateralTriangle, IsoscelesTriangle, Quadrilateral, Rhombus, Rectangle, Square.
* Numbers can be "copied" using copy.copy() or copy.deepcopy().
* Add Point.rotate().
* Add the ability to change the size of Point's drawn shape (using Point.shape_scale).
* Add LineSegment.mark and the ability to change its size (using LineSegment.mark_scale).
* mathmakerlib.requires_pkg becomes mathmakerlib.required and will also handle required options and hacks.
* Add module mathmakerlib.mmlib_setup to configure the behaviour (default values etc.).

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
