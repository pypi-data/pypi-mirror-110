======
monist
======


.. image:: https://img.shields.io/pypi/v/monist.svg
        :target: https://pypi.python.org/pypi/monist

.. image:: https://img.shields.io/travis/datagazing/monist.svg
        :target: https://travis-ci.com/datagazing/monist

.. image:: https://readthedocs.org/projects/monist/badge/?version=latest
        :target: https://monist.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



Simple singleton to share variables across modules

Features
--------

* Use the basic module namespace functionality

Examples
--------

.. code-block:: python

  import monist
  dispatch = eval(monist.dispatch())

  # set singleton value
  monist.thing = 1

  # access singleton value with fallback
  # if monist.thing exists, return it, otherwise return some_default
  asdf = dispatch('thing', some_default)

Importing monist as another name works also:

.. code-block:: python

  import monist as stage
  stage.something = 2

Limitations
-----------

* Almost certainly not thread-safe, appropriate for concurrency, etc.

License
-------

* Free software: MIT license

Documentation
-------------

* https://monist.readthedocs.io/

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
