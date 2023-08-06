#!./runmodule.sh

import os
import shutil
import shlex
import platform
import re
import abc
import typing
from collections.abc import Sequence, Callable, Mapping, MutableMapping

from .subprocess_pipe import run_and_pipe, CompletedProcess


#: The data type of a context manager factory which can be passed to :meth:`SubprocessCommand.run() <confattr.types.SubprocessCommand.run>` and :meth:`SubprocessCommandWithAlternatives.run() <confattr.types.SubprocessCommandWithAlternatives.run>`
TYPE_CONTEXT: 'typing.TypeAlias' = 'Callable[[SubprocessCommand], typing.ContextManager[SubprocessCommand]] | None'


class AbstractType(abc.ABC):

	'''
	This class is merely for documentation purposes.
	It shows which special methods and attributes are considered by this library
	for the data types which are used in a :class:`~confattr.config.Config`.
	'''

	#: If this attribute is present it is used instead of the class name in the config file.
	type_name: str

	#: A help for this data type must be provided, either in this attribute or by adding it to :attr:`Primitive.help_dict <confattr.formatters.Primitive.help_dict>`.
	help: str

	@abc.abstractmethod
	def __init__(self, value: str) -> None:
		'''
		The **constructor** must create an equal objet if it is passed the return value of :meth:`~confattr.types.AbstractType.__str__`.
		Optionally you may want to also accept another data type as argument for creating the default value.

		.. automethod:: __str__
		'''

	@abc.abstractmethod
	def __str__(self) -> str:
		'''
		This method must return a str representation of this object which is suitable to be written to a config file.
		'''



Regex: 'Callable[[str], re.Pattern[str]]'
# when https://github.com/python/typing/issues/213 is implemented I could add more methods
class Regex:  # type: ignore [no-redef]

	type_name = 'regular expression'
	help = '''
	A regular expression in python syntax.
	You can specify flags by starting the regular expression with `(?aiLmsux)`.
	https://docs.python.org/3/library/re.html#regular-expression-syntax
	'''

	def __init__(self, pattern: str) -> None:
		self._compiled_pattern: 're.Pattern[str]' = re.compile(pattern)

	def __getattr__(self, attr: str) -> object:
		return getattr(self._compiled_pattern, attr)

	def __str__(self) -> str:
		return self._compiled_pattern.pattern

	def __repr__(self) -> str:
		return f'{type(self).__name__}({self._compiled_pattern.pattern!r})'

class CaseInsensitiveRegex(Regex):  # type: ignore [valid-type,misc]  # mypy complains about inheriting from Regex because I have declared it as callable

	help = '''
	A case insensitive regular expression in python syntax.
	You can make it case sensitive by wrapping the pattern in `(?-i:...)`.
	https://docs.python.org/3/library/re.html#regular-expression-syntax
	'''

	def __init__(self, pattern: str) -> None:
		self._compiled_pattern = re.compile(pattern, flags=re.I)


class SubprocessCommand:

	type_name = 'command'
	help = '''\
	A command to be executed as a subprocess.
	The command is executed without a shell so redirection or wildcard expansion is not possible.
	Setting environment variables and piping like in a POSIX shell, however, are implemented in python and should work platform independently.
	If you need a shell write the command to a file, insert an appropriate shebang line, make the file executable and set this value to the file.
	'''

	python_callbacks: 'MutableMapping[str, Callable[[SubprocessCommand, TYPE_CONTEXT], None]]' = {}

	@classmethod
	def register_python_callback(cls, name: str, func: 'Callable[[SubprocessCommand, TYPE_CONTEXT], None]') -> None:
		cls.python_callbacks[name] = func

	@classmethod
	def unregister_python_callback(cls, name: str) -> None:
		del cls.python_callbacks[name]

	@classmethod
	def has_python_callback(cls, name: str) -> bool:
		return name in cls.python_callbacks


	def __init__(self, arg: 'SubprocessCommand|Sequence[str]|str', *, env: 'Mapping[str, str]|None' = None) -> None:
		self.cmd: 'Sequence[str]'
		self.env: 'Mapping[str, str]|None'
		if isinstance(arg, str):
			assert env is None
			self.parse_str(arg)
		elif isinstance(arg, SubprocessCommand):
			self.cmd = list(arg.cmd)
			self.env = dict(arg.env) if arg.env else None
			if env:
				if self.env:
					self.env.update(env)
				else:
					self.env = env
		else:
			self.cmd = list(arg)
			self.env = env

	def parse_str(self, arg: str) -> None:
		'''
		Parses a string as returned by :meth:`~confattr.types.SubprocessCommand.__str__` and initializes this objcet accordingly

		:param arg: The string to be parsed
		:raises ValueError: if arg is invalid

		Example:
			If the input is ``arg = 'ENVVAR1=val ENVVAR2= cmd --arg1 --arg2'``
			this function sets
			.. code-block::

				self.env = {'ENVVAR1' : 'val', 'ENVVAR2' : ''}
				self.cmd = ['cmd', '--arg1', '--arg2']
		'''
		if not arg:
			raise ValueError('cmd is empty')

		cmd = shlex.split(arg)

		self.env = {}
		for i in range(len(cmd)):
			if '=' in cmd[i]:
				var, val = cmd[i].split('=', 1)
				self.env[var] = val
			else:
				self.cmd = cmd[i:]
				if not self.env:
					self.env = None
				return

		raise ValueError('cmd consists of environment variables only, there is no command to be executed')

	# ------- compare -------

	def __eq__(self, other: typing.Any) -> bool:
		if isinstance(other, SubprocessCommand):
			return self.cmd == other.cmd and self.env == other.env
		return NotImplemented

	# ------- custom methods -------

	def replace(self, wildcard: str, replacement: str) -> 'SubprocessCommand':
		return SubprocessCommand([replacement if word == wildcard else word for word in self.cmd], env=self.env)

	def run(self, *, context: 'TYPE_CONTEXT|None') -> 'CompletedProcess[bytes]|None':
		'''
		Runs this command and returns when the command is finished.

		:param context: returns a context manager which can be used to stop and start an urwid screen.
		It takes the command to be executed so that it can log the command
		and it returns the command to be executed so that it can modify the command,
		e.g. processing and intercepting some environment variables.

		:return: The completed process
		:raises OSError: e.g. if the program was not found
		:raises CalledProcessError: if the called program failed
		'''
		if self.cmd[0] in self.python_callbacks:
			self.python_callbacks[self.cmd[0]](self, context)
			return None

		if context is None:
			return run_and_pipe(self.cmd, env=self._add_os_environ(self.env))

		with context(self) as command:
			return run_and_pipe(command.cmd, env=self._add_os_environ(command.env))

	@staticmethod
	def _add_os_environ(env: 'Mapping[str, str]|None') -> 'Mapping[str, str]|None':
		if env is None:
			return env
		return dict(os.environ, **env)

	def is_installed(self) -> bool:
		return self.cmd[0] in self.python_callbacks or bool(shutil.which(self.cmd[0]))

	# ------- to str -------

	def __str__(self) -> str:
		if self.env:
			env = ' '.join('%s=%s' % (var, shlex.quote(val)) for var, val in self.env.items())
			env += ' '
		else:
			env = ''
		return env + ' '.join(shlex.quote(word) for word in self.cmd)

	def __repr__(self) -> str:
		return '%s(%r, env=%r)' % (type(self).__name__, self.cmd, self.env)

class SubprocessCommandWithAlternatives:

	type_name = 'command with alternatives'
	help = '''
	One or more commands separated by ||.
	The first command where the program is installed is executed. The other commands are ignored.

	If the command name starts with a '$' it is interpreted as an environment variable containing the name of the program to be executed.
	This is useful to make use of environment variables like EDITOR.
	If the environment variable is not set the program is considered to not be installed and the next command is tried instead.

	The command is executed without a shell so redirection or wildcard expansion is not possible.
	Setting environment variables and piping like in a POSIX shell, however, are implemented in python and should work platform independently.
	If you need a shell write the command to a file, insert an appropriate shebang line, make the file executable and set this value to the file.
	'''

	SEP = '||'

	#: The wild card used by :meth:`~confattr.types.SubprocessCommandWithAlternatives.editor` for the file name
	WC_FILE_NAME = 'fn'

	@classmethod
	def editor(cls, *, visual: bool) -> 'SubprocessCommandWithAlternatives':
		'''
		Create a command to open a file in a text editor.
		The ``EDITOR``/``VISUAL`` environment variables are respected on non-Windows systems.
		'''
		apps: 'Sequence[str]'
		if platform.system() == 'Windows':
			apps = ('notepad',)
		elif visual:
			apps = ('$VISUAL', 'xdg-open',)
		else:
			apps = ('$EDITOR', 'rifle', 'vim', 'nano', 'vi')
		cmds = [[app, cls.WC_FILE_NAME] for app in apps]
		return cls(cmds)


	def get_preferred_command(self) -> SubprocessCommand:
		for cmd in self.commands:
			if cmd.cmd[0].startswith('$'):
				env = cmd.cmd[0][1:]
				exe = os.environ.get(env, None)
				if exe:
					return SubprocessCommand([exe] + list(cmd.cmd[1:]))
			elif cmd.is_installed():
				return cmd

		raise FileNotFoundError('none of the commands is installed: %s' % self)


	def __init__(self, commands: 'Sequence[SubprocessCommand|Sequence[str]|str]|str') -> None:
		if isinstance(commands, str):
			self.commands = [SubprocessCommand(cmd) for cmd in commands.split(self.SEP)]
		else:
			self.commands = [SubprocessCommand(cmd) for cmd in commands]


	def __str__(self) -> str:
		return self.SEP.join(str(cmd) for cmd in self.commands)

	def __repr__(self) -> str:
		return '%s(%s)' % (type(self).__name__, self.commands)


	def replace(self, wildcard: str, replacement: str) -> SubprocessCommand:
		return self.get_preferred_command().replace(wildcard, replacement)

	def run(self, context: 'TYPE_CONTEXT|None' = None) -> 'CompletedProcess[bytes]|None':
		return self.get_preferred_command().run(context=context)
