======
optini
======


.. image:: https://img.shields.io/pypi/v/optini.svg
        :target: https://pypi.org/project/optini/

.. image:: https://img.shields.io/travis/datagazing/optini.svg
        :target: https://travis-ci.com/datagazing/optini

.. image:: https://readthedocs.org/projects/optini/badge/?version=latest
        :target: https://optini.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Python class to get options from command line and config file


* Free software: MIT license
* Documentation: https://optini.readthedocs.io.


Features
--------

* Get options from command line, config file, or defaults
* Simple intuitive way to specify options
* Provide reasonable logging defaults as an option (-v, -d, etc.)
* Use conventions as defaults where possible

Examples
--------

.. code-block:: python

  import optini
  spec = {
      # boolean flag is the default type
      'someopt': {
          'help': 'set a flag',
      },
      'Another': {
          'help': 'this option takes a string arg',
          'type': str,
      },
  }
  # implies -s and --someopt command line options
  # implies -A and --Another command line options
  confobj = optini.Config(appname="myapp", spec=spec, file=True)
  # defaults to ~/.myapp.ini as config file
  if optini.opt.someopt:
      print("someopt flag is set")
  print(optini.opt)

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
