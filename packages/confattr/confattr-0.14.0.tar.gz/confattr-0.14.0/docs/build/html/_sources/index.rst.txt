.. confattr documentation master file, created by
   sphinx-quickstart on Sun Nov 20 08:25:23 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. py:currentmodule:: confattr


===================================
Welcome to confattr's documentation
===================================

:mod:`confattr` (config attributes) is a python library which has the primary use case to read and write config files [:ref:`example <exp-config>`]
but it can also be used to parse the input from a command line and provide auto completion for it [:ref:`example for prompt_toolkit <exp-auto-completion-with-prompt-toolkit>`/:ref:`example for urwid <exp-auto-completion-with-urwid>`].
This library has the following features:

- Static type checking of the code is possible with e.g. `mypy <https://mypy-lang.org/>`_.
- Values are checked and if the config file contains invalid syntax, unknown keys or invalid values a useful error messages is given to the user via a callback registered with :meth:`ConfigFile.set_ui_callback() <confattr.configfile.ConfigFile.set_ui_callback>`.
- It is possible to create a default config file with comments giving help and allowed values via :meth:`ConfigFile.save() <confattr.configfile.ConfigFile.save>`. :ref:`[example] <exp-save>`
- It is possible to generate a help via :meth:`ConfigFile.write_help() <confattr.configfile.ConfigFile.write_help>` and :meth:`ConfigFile.get_help() <confattr.configfile.ConfigFile.get_help>`. :ref:`[example] <exp-generating-help>`
- Settings can be changed via environment variables, too. :ref:`[example] <exp-env>`
- It is possible to use the values of settings and environment variables when assigning a new value to a setting. :ref:`[example] <exp-expansion>`
- It is easy to integrate into existing projects, just replace an existing attribute with a :class:`~confattr.config.Config` instance.
  For example, assume a class has the attribute :python:`color = 'red'`.
  Replace it with :python:`color = Config('color', 'red', allowed_values=['red', 'green', 'blue'])` and call :meth:`ConfigFile.load() <confattr.configfile.ConfigFile.load>` (after the attribute has been created but before it's value is used).
  Then a user can create a config file in the :meth:`expected location() <confattr.configfile.ConfigFile.iter_config_paths>` and can change the attribute with ``set color=green``.
  You don't need to change the usage of the attribute because :class:`~confattr.config.Config` implements the `descriptor protocol <https://docs.python.org/3/reference/datamodel.html#implementing-descriptors>`_.
- It is easy to add custom commands by subclassing :class:`~confattr.configfile.ConfigFileCommand`. :ref:`[example] <exp-extend>`
- It is well documented.
- Includes an example for test automation. :ref:`[example] <exp-pytest>`
- `Test coverage: 100% branch coverage <coverage/index.html>`_  (tested on Python 3.11.3 and Python 3.6.15)


Introduction and examples
=========================

.. toctree::
   :maxdepth: 2

   intro


Installation
============

You can install this library manually with `pip <https://pip.pypa.io/en/stable/>`_

.. code-block:: bash

   $ pip install confattr

or, if you intend to use it in an installable package, just add it to the `dependencies <https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#dependencies-optional-dependencies>`_ of `pyproject.toml <https://packaging.python.org/en/latest/specifications/declaring-project-metadata/>`_

.. code-block:: toml

    [project]
    dependencies = [
        "confattr >= 0.10.0",
    ]


Reference
=========

.. toctree::
   :maxdepth: 2

   confattr
   confattr.config
   confattr.configfile
   confattr.formatters
   confattr.subprocess_pipe
   confattr.types
   confattr.utils


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Links
=====

* `Source code <https://gitlab.com/erzo/confattr>`_
* `Bug tracker <https://gitlab.com/erzo/confattr/-/issues>`_
* `Change log <https://gitlab.com/erzo/confattr/-/tags>`_
* `PyPI <https://pypi.org/project/confattr/>`_
