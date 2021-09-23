========
Overview
========

py-dss-tools is a python framewor that focus on ...

* Free software: MIT license

Installation
============

::

    pip install py-dss-tools

You can also install the in-development version with::

    pip install git+ssh://git@https://github.com/PauloRadatz/py_dss_tools/py_dss_tools/py-dss-tools.git@master

Documentation
=============


https://py-dss-tools.readthedocs.io/


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
