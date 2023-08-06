=============
disambigufile
=============


.. image:: https://img.shields.io/pypi/v/disambigufile.svg
        :target: https://pypi.python.org/pypi/disambigufile

.. image:: https://img.shields.io/travis/datagazing/disambigufile.svg
        :target: https://travis-ci.com/datagazing/disambigufile

.. image:: https://readthedocs.org/projects/disambigufile/badge/?version=latest
        :target: https://disambigufile.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status



Class with file-like interface to a file found in provided search path

Features
--------

* Search a path for a file that matches a pattern
* Search a path for a file inside directories that match a pattern
* Basic file-like interfaces:
    * DisFile(...).open()
    * with DisFile(...) as f: ...
* Get path from config file (if optini module installed)

Examples
--------

Simple usage:

.. code-block:: python

  from disambigufile import DisFile
  path = '/bin:/usr/bin:/usr/local/bin'
  try:
      print(DisFile('^ls', path=path))
  except Exception as e:
      print(f"unable to disambiguate file; exception: {e}")

Using a `with` statement to open the disambiguated file:

.. code-block:: python

  from disambigufile import DisFile
  path = 'path1:path2'
  try:
      with DisFile(r'^asdf', path=path) as f:
          print(f.read())
  except Exception as e:
      print(f"unable to disambiguate file; exception: {e}")

With more specific exception handling:

.. code-block:: python

  from disambigufile import DisFile
  import disambigufile
  path = '/bin:/usr/bin:/usr/local/bin'
  try:
      print(DisFile('^ls', path=path))
  except disambigufile.Error as e:
      # will only catch module-specific exceptions
      print(f"unable to disambiguate file; exception: {e}")

Match a file inside of a matched directory:

.. code-block:: python

  from disambigufile import DisFile
  # search for unique file matching ~/Datasets/*2019-08-19*/data*
  path='~/Datasets'
  try:
      hit = DisFile(
          pattern='2019-08-19',
          path=path,
          subpattern='^data',
      )
      print(hit)
  except disambigufile.Error as e:
      print(f"unable to disambiguate file; exception: {e}")

License
-------

* Free software: MIT license

Documentation
-------------

* https://disambigufile.readthedocs.io/



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
