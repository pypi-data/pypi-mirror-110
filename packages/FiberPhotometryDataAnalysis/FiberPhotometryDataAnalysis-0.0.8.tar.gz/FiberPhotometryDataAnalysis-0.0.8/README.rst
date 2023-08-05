========
Overview
========

A package for analysis of multi-fiber photmetry data and behaviour.

* Free software: MIT license

Installation
============

::

    pip install FiberPhotometryDataAnalysis

You can also install the in-development version with::

    pip install git+ssh://git@https://github.com/katemartian/FiberPhotometryDataAnalysis.git@master

Documentation
=============


https://FiberPhotometryDataAnalysis.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
