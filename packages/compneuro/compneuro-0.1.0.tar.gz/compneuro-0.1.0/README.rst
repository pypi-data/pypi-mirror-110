=========
CompNeuro
=========


.. .. image:: https://img.shields.io/pypi/v/compneuro.svg
..         :target: https://pypi.python.org/pypi/compneuro

.. .. image:: ./coverage.svg
..         :alt: PyTest Coverage

.. .. image:: https://readthedocs.org/projects/compneuro/badge/?version=latest
..         :target: https://compneuro.readthedocs.io/en/latest/?version=latest
..         :alt: Documentation Status


This Module provides source code for Book Chapters and Notebooks for 4020.


* Free software: BSD-3 license


Features
--------

* Utility functions for signal generation, spectral analysis, spike plotting, and other plotting functionalities
* CPU-based simulation and analysis of dynamical system models
* Interactive plotting of results using Bokeh.


Development
-----------

Before committing, use black_ to format the python code by running

.. code::

        black compneuro

For each utility function added, make sure you add a test function in the
`compneuro/tests` folder. All tests should be written using pytest_.

You can also run all tests by running:

.. code::

        py.test

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`black`: https://github.com/psf/black
.. _`pytest`: https://docs.pytest.org/