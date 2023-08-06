.. py:currentmodule:: confattr

=========================
Introduction and examples
=========================

.. _exp-config:
.. _exp-save:

Config and ConfigFile
=====================

:mod:`confattr` (config attributes) is a python library to make applications configurable.
This library defines the :class:`~confattr.config.Config` class to create attributes which can be changed in a config file.
It uses the `descriptor protocol <https://docs.python.org/3/reference/datamodel.html#implementing-descriptors>`__ to return it's value when used as an instance attribute.

.. literalinclude:: examples/config_and_configfile/example.py
   :language: python
   :start-after: # ------- start -------
   :end-before: # ------- 01 -------

If you want to access the Config object itself you need to access it as a class attribute:

.. literalinclude:: examples/config_and_configfile/example.py
   :language: python
   :start-after: # ------- 01 -------
   :end-before: # ------- 02 -------

You load a config file with a :class:`~confattr.configfile.ConfigFile` object.
You should provide a callback function with :meth:`~confattr.configfile.ConfigFile.set_ui_callback` which informs the user if the config file contains invalid lines.
This callback function takes a :class:`~confattr.configfile.Message` object as argument.
You can format it automatically by converting it to a str, e.g. with ``str(msg)``.
Among other attributes this object also has a :attr:`~confattr.configfile.Message.notification_level` (or :attr:`~confattr.configfile.Message.lvl` for short) which should be used to show messages of different severity in different colors.
By default only :const:`~confattr.configfile.NotificationLevel.ERROR` messages are reported but you should pass a :class:`~confattr.config.Config` to :paramref:`~confattr.configfile.ConfigFile.notification_level` when instantiating a :class:`~confattr.configfile.ConfigFile` object so that the users of your application can change that.
When you load a config file with :meth:`ConfigFile.load() <confattr.configfile.ConfigFile.load>` all :class:`~confattr.config.Config` objects which are set in the config file are updated automatically.

It is recognized automatically that the setting ``traffic-law.speed-limit`` has an integer value.
A value given in a config file is therefore automatically parsed to an integer.
If the parsing fails the user interface callback function is called.

.. literalinclude:: examples/config_and_configfile/example.py
   :language: python
   :start-after: # ------- 02 -------
   :end-before: # ------- 02-end -------

Given the following config file (the location of the config file is determined by :meth:`ConfigFile.iter_config_paths() <confattr.configfile.ConfigFile.iter_config_paths>`):

.. literalinclude:: examples/config_and_configfile/config

The script will give the following output:

.. literalinclude:: examples/config_and_configfile/output.txt
   :language: text

You can save the current configuration with :meth:`ConfigFile.save() <confattr.configfile.ConfigFile.save>` if you want to write it to the default location
or with :meth:`ConfigFile.save_file() <confattr.configfile.ConfigFile.save_file>` if you want to specify the path yourself.

.. literalinclude:: examples/config_and_configfile/example.py
   :language: python
   :start-after: # ------- 03-begin -------

This will write the following file:

.. literalinclude:: examples/config_and_configfile/exported-config


.. _exp-expansion:

Using the values of settings or environment variables
=====================================================

Consider the following example:

.. literalinclude:: examples/expansion/example.py
   :language: python
   :start-after: # ------- start -------
   :end-before: # ------- 1 -------

To simplify the writing of this example I will directly pass the lines that I would otherwise write into a config file to :meth:`ConfigFile.parse_line() <confattr.configfile.ConfigFile.parse_line>`.

You can use the value of a setting in the ``set`` command by wrapping the key of the setting in percent characters.
You can also specify a `format_spec <https://docs.python.org/3/library/string.html#formatspec>`__.

.. literalinclude:: examples/expansion/example.py
   :language: python
   :start-after: # ------- 1 -------
   :end-before: # ------- 2 -------

If you want to apply the format spec to the string representation of the value instead of on the value itself put an exclamation mark in front of the colon.
You can also use ``!r``, ``!s`` and ``!a`` like in an `f-string <https://docs.python.org/3/reference/lexical_analysis.html#f-strings>`__.

.. literalinclude:: examples/expansion/example.py
   :language: python
   :start-after: # ------- 2 -------
   :end-before: # ------- 3 -------

You can use a format_spec to convert a bool to an int.

.. literalinclude:: examples/expansion/example.py
   :language: python
   :start-after: # ------- 3 -------
   :end-before: # ------- 4 -------

The values are expanded when executing the set command so the order in which you set the settings is important.

.. literalinclude:: examples/expansion/example.py
   :language: python
   :start-after: # ------- 4 -------
   :end-before: # ------- 5 -------

You can use the expansion of settings to add new values to a collection.

.. literalinclude:: examples/expansion/example.py
   :language: python
   :start-after: # ------- 5 -------
   :end-before: # ------- 6 -------

And you can use the format_spec defined in the :meth:`List() <confattr.formatters.List.expand_value>`, :meth:`Set() <confattr.formatters.AbstractCollection.expand_value>` and  :meth:`Dict() <confattr.formatters.Dict.expand_value>` classes to remove elements from collections.
(Exceptions raised by :meth:`~confattr.formatters.AbstractFormatter.expand_value` are caught in :class:`~confattr.configfile.ConfigFile` and reported via the callback registered with :meth:`ConfigFile.set_ui_callback() <confattr.configfile.ConfigFile.set_ui_callback>`.)

.. literalinclude:: examples/expansion/example.py
   :language: python
   :start-after: # ------- 6 -------
   :end-before: # ------- 7 -------

If you want to insert a literal percent sign use ``%%``.
Alternatively, if you don't want to expand any settings or environment variables, you can insert the flag ``--raw`` (or ``-r`` for short) before the key.

.. literalinclude:: examples/expansion/example.py
   :language: python
   :start-after: # ------- 7 -------
   :end-before: # ------- 8 -------

You can access environment variables like in a POSIX shell, although not all expansion features are supported and the curly braces are mandatory.
For more information see the description of :meth:`ConfigFile.expand_env_match() <confattr.configfile.ConfigFile.expand_env_match>`.

.. literalinclude:: examples/expansion/example.py
   :language: python
   :start-after: # ------- 8 -------


Config file syntax
==================

I have looked at the config files of different applications trying to come up with a syntax as intuitive as possible.
Two extremes which have heavily inspired me are the config files of `vim <https://www.vim.org/>`__ and `ranger <https://ranger.github.io/>`__.

I am using :func:`shlex.split(line, comments=True) <shlex.split>` to split the lines so quoting and inline comments work similar to bash
although there are minor differences, e.g. a ``#`` in an argument must be escaped or quoted.

Lines starting with a ``"`` or ``#`` are ignored.

The ``set`` command has two different forms.
I recommend to *not* mix them in order to improve readability.
Both forms support the expansion of settings and environment variables in the value, see the :ref:`previous example <exp-expansion>`.

- ``set key1=val1 [key2=val2 ...]`` |quad| (inspired by vimrc)

  ``set`` takes an arbitrary number of arguments, each argument sets one setting.

  Has the advantage that several settings can be changed at once.
  This is useful if you want to bind a set command to a key and process that command with :meth:`ConfigFile.parse_line() <confattr.configfile.ConfigFile.parse_line>` if the key is pressed.

  If the value contains one or more spaces it must be quoted.
  ``set greeting='hello world'`` and ``set 'greeting=hello world'`` are equivalent.

- ``set key [=] val`` |quad| (inspired by ranger config)

  ``set`` takes two arguments, the key and the value.
  Optionally a single equals character may be added in between as third argument.

  Has the advantage that key and value are separated by one or more spaces which can improve the readability of a config file.

  If the value contains one or more spaces it must be quoted:
  ``set greeting 'hello world'`` and ``set greeting = 'hello world'`` are equivalent.

I recommend to not use spaces in key names so that they don't need to be wrapped in quotes.


Further commands:

- ``include filename``

  Load another config file.
  If ``filename`` is a relative path it is relative to the directory of the config file it appears in.

  This command is explained in more detail in :ref:`this example <exp-include>`.

- ``echo message``

  Display a message.
  Settings and environment variables in the message are expanded just like in the value of a ``set`` command (see the :ref:`previous example <exp-expansion>`).

- ``help [command]``

  Display a list of available commands if no arguments are given
  or the help for the specified command if an argument is passed.

  Just like the other commands the output is passed to the callback registered with :meth:`ConfigFile.set_ui_callback() <confattr.configfile.ConfigFile.set_ui_callback>`.


Allowed key names
=================

As first argument of any :class:`~confattr.config.Config` instance you must provide a :paramref:`~confattr.config.Config.key` which is used to specify the setting in a config file.

This key must *not* contain an ``=`` sign because that is used to separate the value from the key in the :class:`set <confattr.configfile.Set>` command.

I recommend to stick to the following characters:

- letters
- digits
- hyphens
- dots to group several settings together

I recommend to *not* use spaces and other special characters to avoid the need to wrap the key in quotes.

I recommend to *not* internationalize the keys so that config files do not break if a user changes the language.
This also gives users of different languages the possibility to exchange their config files.

I recommend to name the keys in English.


.. _exp-multi:

Different values for different objects
======================================

A :class:`~confattr.config.Config` object always returns the same value, regardless of the owning object it is an attribute of:

.. literalinclude:: examples/config_same_value/example.py
   :language: python
   :start-after: # ------- start -------

Output:

.. literalinclude:: examples/config_same_value/output.txt
   :language: text



If you want to have different values for different objects you need to use :class:`~confattr.config.MultiConfig` instead.
This requires the owning object to have a special attribute called :attr:`~confattr.configfile.ConfigFile.config_id`.
All objects which have the same :attr:`~confattr.configfile.ConfigFile.config_id` share the same value.
All objects which have different :attr:`~confattr.configfile.ConfigFile.config_id` can have different values (but don't need to have different values).

.. literalinclude:: examples/multiconfig/example.py
   :language: python
   :start-after: # ------- start -------

Given the following config file:

.. literalinclude:: examples/multiconfig/config

It creates the following output:

.. literalinclude:: examples/multiconfig/output.txt
   :language: text



``another-car`` gets the default color black as it is not set in the config file.
You can change this default color in the config file by setting it before specifying a config id or after specifying the special config id ``general`` (:attr:`Config.default_config_id <confattr.config.Config.default_config_id>`).
Note how this adds ``general`` to :attr:`MultiConfig.config_ids <confattr.config.MultiConfig.config_ids>`.

.. literalinclude:: examples/multiconfig/config2

Creates the following output:

.. literalinclude:: examples/multiconfig/output2.txt
   :language: text



.. _exp-multi-config-reset:

MultiConfig.reset
=================

For normal :class:`~confattr.config.Config` instances you can restore a certain state of settings by calling :meth:`ConfigFile.save(comments=False) <confattr.configfile.ConfigFile.save>` (when you have the state that you want to restore later on) and :meth:`ConfigFile.load() <confattr.configfile.ConfigFile.load>` (where you want to restore the saved state).

This is not enough when you are using :class:`~confattr.config.MultiConfig` instances.
Consider the following example:

.. literalinclude:: examples/multiconfig_reset/example.py
   :language: python
   :start-after: # ------- start -------

The last assert fails because when saving the config no value for ``w1`` has been set yet.
It is just falling back to the default value "hello world".
The saved config file is therefore:

.. literalinclude:: examples/multiconfig_reset/expected-config

After the config was saved the value for ``w1`` is changed to "hey you".
When loading the config the default value is restored to ``hello world`` (which makes no difference because it has never been changed)
but the value for ``w1`` is not changed because there is no value for ``w1`` in the config file.

The solution is to call :meth:`MultiConfig.reset() <confattr.config.MultiConfig.reset>` before loading the config.



Settings without default value
==============================

Sometimes there is no sane default value, several values are equally likely and if a wrong value is set the application won't work at all.
In those cases you can use :class:`~confattr.config.ExplicitConfig` which throws an exception if the user does not explicitly set a value in the config file.

.. literalinclude:: examples/explicit_config/example.py
   :language: python
   :start-after: # ------- start -------


.. _exp-include:

Include
=======

Consider a backup application which synchronizes one or more directory pairs.
The following code might be a menu for it to choose which side should be changed:

.. literalinclude:: examples/include/example.py
   :language: python
   :start-after: # ------- start -------

Let's assume there are many more settings how to synchronize a pair of directories than just the direction.
You might want to use the same synchronization settings for several directory pairs.
You can write these settings to a separate config file and include it for the corresponding directory pairs:

.. literalinclude:: examples/include/config
   :caption: main config file: config
.. literalinclude:: examples/include/mirror
   :caption: included config file: mirror
.. literalinclude:: examples/include/two-way
   :caption: included config file: two-way

This produces the following display:

.. literalinclude:: examples/include/output.txt
   :emphasize-lines: 1

The config id of the included file starts with the value of the config id that the including file has at the moment of calling ``include``.
Otherwise the pattern shown above of reusing a config file for several config ids would not be possible.

If the included file changes the config id the config id is reset to the value it had at the beginning of the include when reaching the end of the included file.
Otherwise changing an included file might unexpectedly change the meaning of the main config file or another config file which is included later on.

It is possible to change this default behavior by using ``include --reset-config-id-before filename`` or ``include --no-reset-config-id-after filename``.


.. _exp-generating-help:

Generating help
===============

You can generate a help with :meth:`ConfigFile.write_help() <confattr.configfile.ConfigFile.write_help>` or :meth:`ConfigFile.get_help() <confattr.configfile.ConfigFile.get_help>`.

:meth:`ConfigFile.get_help() <confattr.configfile.ConfigFile.get_help>` is a wrapper around :meth:`ConfigFile.write_help() <confattr.configfile.ConfigFile.write_help>`.
If you want to print the help to stdout :python:`config_file.write_help(HelpWriter(None))` would be more efficient than :python:`print(config_file.get_help())`.
If you want to display the help in a graphical user interface you can implement a custom :class:`~confattr.configfile.FormattedWriter` which you can pass to :meth:`ConfigFile.write_help() <confattr.configfile.ConfigFile.write_help>` instead of parsing the output of :meth:`ConfigFile.get_help() <confattr.configfile.ConfigFile.get_help>`.

.. literalinclude:: examples/generating_help/example.py
   :language: python
   :start-after: # ------- start -------

Assuming the above file was contained in a package called ``exampleapp`` it would output the following:

.. literalinclude:: examples/generating_help/output.txt
   :language: text



The help is formatted on two levels:

1. :class:`argparse.HelpFormatter` does the merging of lines, wrapping of lines and indentation. It formats the usage and all the command line arguments and options.
   Unfortunately "All the methods provided by the class are considered an implementation detail" according to it's `doc string <https://github.com/python/cpython/blob/main/Lib/argparse.py#L157>`__.
   The only safe way to customize this level of formatting is by handing one of the predefined standard classes to the :paramref:`~confattr.configfile.ConfigFile.formatter_class` parameter of the :class:`~confattr.configfile.ConfigFile` constructor:

   - :class:`argparse.HelpFormatter`
   - :class:`argparse.RawDescriptionHelpFormatter`
   - :class:`argparse.RawTextHelpFormatter`
   - :class:`argparse.ArgumentDefaultsHelpFormatter`
   - :class:`argparse.MetavarTypeHelpFormatter`

   Additionally I provide another subclass :class:`confattr.utils.HelpFormatter` which has a few class attributes for customization which I am trying to keep backward compatible.
   So you can subclass this class and change these attributes.
   But I cannot guarantee to always support the newest python version.

   If you want any more customization take a look at the `source code <https://github.com/python/cpython/blob/main/Lib/argparse.py#L157>`__ but be prepared that you may need to change your code with any future python version.

2. :class:`~confattr.configfile.FormattedWriter` is intended to do stuff like underlining sections and inserting comment characters at the beginning of lines (when writing help to a config file).
   This package defines two subclasses:
   :class:`~confattr.configfile.ConfigFileWriter` which is used by default in :meth:`ConfigFile.save() <confattr.configfile.ConfigFile.save>` and
   :class:`~confattr.configfile.HelpWriter` which is used in :meth:`ConfigFile.get_help() <confattr.configfile.ConfigFile.get_help>`.

   If you want to customize this level of formatting implement your own :class:`~confattr.configfile.FormattedWriter`
   and override :meth:`ConfigFile.get_help() <confattr.configfile.ConfigFile.get_help>` or :meth:`ConfigFile.save_to_open_file() <confattr.configfile.ConfigFile.save_to_open_file>` to use your class.


.. _exp-regex:

Custom data type for regular expressions
========================================

The following example defines a custom data type for regular expressions.
Using this instead of a normal :class:`str` has the following advantages:

- It is called a "regular expression" instead of a "str" which tells the user that this is a regular expression.
- It provides help for the user.
- :meth:`ConfigFile.load() <confattr.configfile.ConfigFile.load>`/:meth:`ConfigFile.parse_line() <confattr.configfile.ConfigFile.parse_line>` will do the error handling for you. If the user enters a syntactically incorrect value then :func:`re.compile` throws an exception which will be caught and the error message is reported to the user by calling the callback which has been (or will be) passed to :meth:`ConfigFile.set_ui_callback() <confattr.configfile.ConfigFile.set_ui_callback>`.

.. literalinclude:: examples/type_regex/example_definition.py
   :language: python
   :start-after: # ------- start -------

This definition is actually included in :mod:`confattr.types` so you can easily use it like this:

.. literalinclude:: examples/type_regex/example_usage.py
   :language: python
   :start-after: # ------- start -------

Similarly there is also a :class:`confattr.types.CaseInsensitiveRegex` class which compiles the regular expression with the :const:`re.I` flag.

When you save the configuration like this

.. literalinclude:: examples/type_regex/example_save.py
   :language: python
   :start-after: # ------- start -------

the saved file looks like this:

.. literalinclude:: examples/type_regex/expected-config

Custom data types to be used as a :attr:`~confattr.config.Config.value` of a setting must fulfill the following conditions:

- Return a string representation suitable for the config file from :meth:`~confattr.types.AbstractType.__str__`.
- Accept the return value of :meth:`~confattr.types.AbstractType.__str__` as argument for the constructor to create an equal object.
- Have a :attr:`~confattr.types.AbstractType.help` attribute to give the user a description of the data type. Alternatively the help can be provided via :attr:`Primitive.help_dict <confattr.formatters.Primitive.help_dict>`.

It can have a :attr:`~confattr.types.AbstractType.type_name` attribute to specify how the type is called in the config file. If it is missing it is derived from the class name.

For more information on the supported data types see :class:`~confattr.config.Config`.


Custom data type for paths
==========================

Similar to the :ref:`regex example <exp-regex>` you can also define a custom data type to store paths.
Unlike :class:`~confattr.types.Regex` I have not included this in :mod:`confattr.types` because it differs too much from use case to use case:

- Does it point to files or directories?
- Does the target need to exist?
- Does an external drive need to be mounted? If so, at which point?
- Does a UUID need to be replaced by a mount point?

A very simple definition could look like this.
Note how :func:`os.path.expanduser` is used to convert this type to a str.
This is something that you will probably want in any case.

.. literalinclude:: examples/type_path/example.py
   :language: python
   :start-after: # ------- start -------



.. _exp-extend:

Adding new commands to the config file syntax
=============================================

You can extend this library by defining new commands which can be used in the config file.
All you need to do is subclass :class:`~confattr.configfile.ConfigFileCommand` and implement the :meth:`~confattr.configfile.ConfigFileCommand.run` method.
Additionally I recommend to provide a doc string explaining how to use the command in the config file. The doc string is used by :meth:`~confattr.configfile.ConfigFileCommand.get_help` which may be used by an in-app help.
Optionally you can set :attr:`~confattr.configfile.ConfigFileCommand.name` and :attr:`~confattr.configfile.ConfigFileCommand.aliases` and implement the :meth:`~confattr.configfile.ConfigFileCommand.save` method.

Alternatively :class:`~confattr.configfile.ConfigFileArgparseCommand` can be subclassed instead, it aims to make the parsing easier and avoid redundancy in the doc string by using the :mod:`argparse` module.
You must implement :meth:`~confattr.configfile.ConfigFileArgparseCommand.init_parser` and :meth:`~confattr.configfile.ConfigFileArgparseCommand.run_parsed`.
You should give a doc string describing what the command does.
In contrast to :class:`~confattr.configfile.ConfigFileCommand` :mod:`argparse` adds usage and the allowed arguments to the output of :meth:`~confattr.configfile.ConfigFileArgparseCommand.get_help` automatically.

For example you may want to add a new command to bind keys to whatever kind of command.
The following example assumes `urwid`_ as user interface framework.

.. literalinclude:: examples/map/example.py
   :language: python
   :start-after: # ------- start -------

Given the following config file it is possible to move the cursor upward and downward with ``j`` and ``k`` like in vim:

.. literalinclude:: examples/map/config


The help for the newly defined command looks like this:

.. literalinclude:: examples/map/example_print_help.py
   :language: python
   :start-after: # ------- start -------

.. literalinclude:: examples/map/output_help.txt



(All subclasses of :class:`~confattr.configfile.ConfigFileCommand` are saved in :meth:`ConfigFileCommand.__init_subclass__() <confattr.configfile.ConfigFileCommand.__init_subclass__>` and can be retrieved with :meth:`ConfigFileCommand.get_command_types() <confattr.configfile.ConfigFileCommand.get_command_types>`.
The :class:`~confattr.configfile.ConfigFile` constructor uses that if :paramref:`~confattr.configfile.ConfigFile.commands` is not given.)


Writing custom commands to the config file
==========================================

The previous example has shown how to define new commands so that they can be used in the config file.
Let's continue that example so that calls to the custom command ``map`` are written with :meth:`ConfigFile.save() <confattr.configfile.ConfigFile.save>`.

All you need to do for that is implementing the :meth:`ConfigFileCommand.save() <confattr.configfile.ConfigFileCommand.save>` method.

:attr:`~confattr.configfile.ConfigFileCommand.should_write_heading` is True if there are several commands which implement the :meth:`~confattr.configfile.ConfigFileCommand.save` method.

Experimental support for type checking ``**kw`` has been added in `mypy 0.981 <https://mypy-lang.blogspot.com/2022/09/mypy-0981-released.html>`__.
:class:`~confattr.configfile.SaveKwargs` depends on :class:`typing.TypedDict` and therefore is not available before Python 3.8.

.. literalinclude:: examples/map_save/example_1.py
   :language: python
   :start-after: # ------- start -------

However, :data:`urwid.command_map` contains more commands than the example app uses so writing all of them might be confusing.
Therefore let's add a keyword argument to write only the specified commands:

.. literalinclude:: examples/map_save/example_3.py
   :language: python
   :start-after: # ------- start -------

This produces the following config file:

.. literalinclude:: examples/map_save/config


If you don't care about Python < 3.8 you can import :class:`~confattr.configfile.SaveKwargs` normally and save a line when calling :meth:`ConfigFile.save() <confattr.configfile.ConfigFile.save>`:

.. code-block:: python

       kw: SaveKwargs = MapSaveKwargs(urwid_commands=...)
       config_file.save(**kw)


Customizing the config file syntax
==================================

If you want to make minor changes to the syntax of the config file you can subclass the corresponding command, i.e. :class:`~confattr.configfile.Set` or :class:`~confattr.configfile.Include`.

For example if you want to use a ``key: value`` syntax you could do the following.

I am setting :attr:`~confattr.configfile.ConfigFileCommand.name` to an empty string (i.e. :const:`~confattr.configfile.DEFAULT_COMMAND`) to make this the default command which is used if an unknown command is encountered.
This makes it possible to use this command without writing out it's name in the config file.

.. literalinclude:: examples/custom_set/example.py
   :language: python
   :start-after: # ------- start -------

Then a config file might look like this:

.. literalinclude:: examples/custom_set/config
   :end-before: # ------- end -------

Please note that it's still possible to use the ``include`` command.
If you want to avoid that use

.. literalinclude:: examples/custom_set/example_no_include.py
   :language: python
   :start-after: # ------- start -------
   :end-before: # ------- end -------

If you want to make bigger changes like using JSON you need to subclass :class:`~confattr.configfile.ConfigFile`.


.. _exp-auto-completion-with-prompt-toolkit:

Auto completion with prompt_toolkit
===================================

(This example uses `prompt_toolkit <https://pypi.org/project/prompt-toolkit/>`__ as user interface, the :ref:`next example<exp-auto-completion-with-urwid>` uses `urwid <http://urwid.org/>`__.)

:mod:`confattr` can also be used as backend for a command line interface.
In that case you call :meth:`ConfigFile.parse_line() <confattr.configfile.ConfigFile.parse_line>` directly with the input that you get from the user.

You can define custom commands as shown in :ref:`exp-extend` and if you use different :class:`~confattr.configfile.ConfigFile` objects for the config file and for the command line interface you can specify different commands to be available with the :paramref:`~confattr.configfile.ConfigFile.commands` parameter.

In order to make a command line usable, however, it also needs an auto completion.
The most interesting part of this example is therefore probably the ``ConfigFileCompleter`` class which acts an adapter between the suggestions generated by :meth:`ConfigFile.get_completions() <confattr.configfile.ConfigFile.get_completions>` and the way how prompt_toolkit wants to have them.

I am using different :class:`~confattr.configfile.ConfigFile` objects for the config file and for the command line in order to have different settings and default values for the :paramref:`~confattr.configfile.ConfigFile.notification_level`.
I am passing :paramref:`~confattr.configfile.ConfigFile.show_line_always` to the :class:`~confattr.configfile.ConfigFile` which is responsible for the command line so that the input line is not repeated in every response.
Note how I am patching the :attr:`~confattr.configfile.ConfigFileCommand.config_file` of the ``include`` command to always use the :class:`~confattr.configfile.ConfigFile` object for the config file, no matter whether it is called from the command line or from the config file.

.. literalinclude:: examples/auto_complete_prompt_toolkit/example.py
   :language: python
   :start-after: # ------- start -------


.. _exp-auto-completion-with-urwid:

Auto completion with urwid
==========================

This example is pretty similar to the :ref:`previous example<exp-auto-completion-with-prompt-toolkit>` but it uses `urwid <http://urwid.org/>`__ instead of `prompt_toolkit <https://pypi.org/project/prompt-toolkit/>`__.

Unfortunately urwid does not provide a widget with auto completion.
There is `urwid_readline <https://github.com/rr-/urwid_readline>`__ but it's auto completion feature is not powerful enough to work well with this library.
Instead this example implements a custom ``EditWithAutoComplete`` widget.

.. literalinclude:: examples/auto_complete_urwid/example.py
   :language: python
   :start-after: # ------- start -------

Opening the config file in a text editor
========================================

You can use :meth:`confattr.types.SubprocessCommandWithAlternatives.editor` to create a command for opening the config file.
It respects the ``EDITOR``/``VISUAL`` environment variables on non-Windows systems and includes some fall backs if the environment variables are not set.

:meth:`config_file.save() <confattr.configfile.ConfigFile.save>` returns the file name of the config file.

You can pass a context manager factory to :paramref:`~confattr.types.SubprocessCommand.run.context` in case you need to ``stop()`` an `urwid screen <https://urwid.org/reference/display_modules.html>`_ before opening the file and ``start()`` it again after closing the file.

.. literalinclude:: examples/editor/example.py
   :language: python
   :start-after: # ------- start -------


Config without classes
======================

If you want to use :class:`~confattr.config.Config` objects without custom classes you can access the value via the :attr:`Config.value <confattr.config.Config.value>` attribute:

.. literalinclude:: examples/config_without_classes/example.py
   :language: python
   :start-after: # ------- start -------

Given the following config file (the location of the config file is determined by :meth:`ConfigFile.iter_config_paths() <confattr.configfile.ConfigFile.iter_config_paths>`):

.. literalinclude:: examples/config_without_classes/config

The script will give the following output:

.. literalinclude:: examples/config_without_classes/output.txt
   :language: text



.. _exp-pytest:

Testing your application
========================

I recommend doing static type checking with `mypy <https://mypy-lang.org/>`__
in `strict mode <https://mypy.readthedocs.io/en/latest/getting_started.html#strict-mode-and-configuration>`__
and dynamic testing with `pytest`_.
`tox <https://tox.wiki/en/latest/>`__ can run both in a single command and automatically handles virtual environments for you.
While you can configure tox to run your tests on several specific python versions you can also simply use ``py3`` which will use whatever python 3 version you have installed.
For packaging and publishing your application I recommend `flit <https://flit.pypa.io/en/stable/>`__
over the older `setuptools <https://setuptools.pypa.io/en/latest/setuptools.html>`__
because flit is much more intuitive and less error prone.

For dynamic testing you need to consider two things:

1. Your application must not load a config file from the usual paths so that the tests always have the same outcome no matter which user is running them and on which computer.
   You can achieve that by setting one of the attributes :attr:`ConfigFile.config_directory <confattr.configfile.ConfigFile.config_directory>` or :attr:`ConfigFile.config_path <confattr.configfile.ConfigFile.config_path>` or one of the corresponding environment variables ``APPNAME_CONFIG_DIRECTORY`` or ``APPNAME_CONFIG_PATH`` in the setup of your tests.

   In `pytest`_ you can do this with an `auto use <https://docs.pytest.org/en/6.2.x/fixture.html#autouse-fixtures-fixtures-you-don-t-have-to-request>`__ `fixture <https://docs.pytest.org/en/6.2.x/fixture.html#what-fixtures-are>`__.
   `tmp_path <https://docs.pytest.org/en/6.2.x/reference.html#tmp-path>`__ creates an empty directory for you and `monkeypatch`_ cleans up for you after the test is done.
   If all of your tests are defined in a single file you can define this fixture in that file.
   Otherwise the definition goes into `conftest.py <https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files>`__.

   .. literalinclude:: examples/testing_tmp_path/example.py
      :language: python
      :start-after: # ------- start -------

2. Your tests need to change settings in order to test all possibilities but all settings which have been changed in a test must be reset after each test so that the tests always have the same outcome no matter whether they are executed all together or alone.

   Of course you could just save a config file in the setup and load it in the teardown (and don't forget to call :ref:`MultiConfig.reset <exp-multi-config-reset>`).
   But keep in mind that you may have many settings and many tests and that they may become more in the future.
   It is more efficient to let `monkeypatch`_ clean up only those settings that you have changed.

   Let's assume we want to test our car from the :ref:`first example <exp-config>`:

   .. literalinclude:: examples/testing_monkeypatch_config/example.py
      :language: python
      :start-after: # ------- start -------


   If we want to change the value of a :class:`~confattr.config.MultiConfig` setting like in :ref:`this example <exp-multi>` for a specific object
   we would use :meth:`monkeypatch.setitem() <pytest.MonkeyPatch.setitem>` to change :attr:`MultiConfig.values <confattr.config.MultiConfig.values>`:

   .. literalinclude:: examples/testing_monkeypatch_multiconfig/example.py
      :language: python
      :start-after: # ------- start -------



.. _pytest: https://docs.pytest.org/en/stable/
.. _monkeypatch: https://docs.pytest.org/en/6.2.x/reference.html#std-fixture-monkeypatch



.. _exp-env:

Environment variables
=====================

Settings can be changed via environment variables, too.
For example if you have an application called ``example-app`` with the following code

.. literalinclude:: examples/env/example.py
   :language: python
   :start-after: # ------- start -------

and you call it like this

.. literalinclude:: examples/env/example.sh
   :language: bash
   :start-after: # ------- start -------

it will print

.. literalinclude:: examples/env/expected_output.txt
   :language: bash

For the exact rules how the names of the environment variables are created are described in :meth:`ConfigFile.get_env_name() <confattr.configfile.ConfigFile.get_env_name>`.

Environment variables which start with the name of the application but do not match a setting (and are not one those listed below) or have an invalid value are reported as :const:`~confattr.configfile.NotificationLevel.ERROR` to the callback registered with :meth:`ConfigFile.set_ui_callback() <confattr.configfile.ConfigFile.set_ui_callback>`.


Furthermore this library is influenced by the following environment variables:

- ``XDG_CONFIG_HOME`` defines the base directory relative to which user-specific configuration files should be stored on Linux. [1]_ [2]_
- ``XDG_CONFIG_DIRS`` defines the preference-ordered set of base directories to search for configuration files in addition to the ``XDG_CONFIG_HOME`` base directory on Linux. The directories in ``XDG_CONFIG_DIRS`` should be separated with a colon. [1]_ [2]_
- ``APPNAME_CONFIG_PATH`` defines the value of :attr:`ConfigFile.config_path <confattr.configfile.ConfigFile.config_path>`. [2]_ [3]_
- ``APPNAME_CONFIG_DIRECTORY`` defines the value of :attr:`ConfigFile.config_directory <confattr.configfile.ConfigFile.config_directory>`. [2]_ [3]_
- ``APPNAME_CONFIG_NAME``  defines the value of :attr:`ConfigFile.config_name <confattr.configfile.ConfigFile.config_name>`. [2]_ [3]_


.. [1] is not queried directly but outsourced to `platformdirs <https://pypi.org/project/platformdirs/>`__, `xdgappdirs <https://pypi.org/project/xdgappdirs/>`__ or `appdirs <https://pypi.org/project/appdirs/>`__, see :meth:`ConfigFile.get_app_dirs() <confattr.configfile.ConfigFile.get_app_dirs>`.
   See also https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html#variables.
.. [2] influences :meth:`ConfigFile.iter_config_paths() <confattr.configfile.ConfigFile.iter_config_paths>`
.. [3] where ``APPNAME`` is the value of :paramref:`~confattr.configfile.ConfigFile.appname` which is passed to the constructor of :class:`~confattr.configfile.ConfigFile` but in all upper case letters and hyphens, dots and spaces replaced by underscores, see :meth:`ConfigFile.get_env_name() <confattr.configfile.ConfigFile.get_env_name>`.



.. _urwid: http://urwid.org/
