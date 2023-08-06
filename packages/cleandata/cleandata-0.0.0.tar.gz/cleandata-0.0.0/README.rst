========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/cleandata/badge/?style=flat
    :target: https://cleandata.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/rinman24/cleandata.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/rinman24/cleandata

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/rinman24/cleandata?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/rinman24/cleandata

.. |requires| image:: https://requires.io/github/rinman24/cleandata/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/rinman24/cleandata/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/rinman24/cleandata/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/rinman24/cleandata

.. |version| image:: https://img.shields.io/pypi/v/cleandata.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/cleandata

.. |wheel| image:: https://img.shields.io/pypi/wheel/cleandata.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/cleandata

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/cleandata.svg
    :alt: Supported versions
    :target: https://pypi.org/project/cleandata

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/cleandata.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/cleandata

.. |commits-since| image:: https://img.shields.io/github/commits-since/rinman24/cleandata/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/rinman24/cleandata/compare/v0.0.0...master



.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: MIT license

Installation
============

::

    pip install cleandata

You can also install the in-development version with::

    pip install https://github.com/rinman24/cleandata/archive/master.zip


Documentation
=============


https://cleandata.readthedocs.io/


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
