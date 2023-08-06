========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/scanpy-utils/badge/?style=flat
    :target: https://scanpy-utils.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/NUPulmonary/scanpy-utils.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/NUPulmonary/scanpy-utils

.. end-badges

Utility functions for `scanpy <https://scanpy.readthedocs.io>`_

* Free software: MIT license

Installation
============

::

    pip install scanpy-utils


Documentation
=============


See https://scanpy-utils.readthedocs.io/en/latest/reference/index.html


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
