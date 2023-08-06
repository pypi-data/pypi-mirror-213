#!../venv/bin/pytest -vv

from confattr import ConfigFile, Message, ConfigFileCommand
from confattr.configfile import Help

from collections.abc import Sequence


def test_help_general() -> None:
	messages: 'list[Message]' = []

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(messages.append)

	cf.parse_line("help")
	msg, = messages
	assert str(msg) == """\
The following commands are defined:
- set      Change the value of a setting.
- include  Load another config file.
- echo     Display a message.
- help     Display help.

Use `help <cmd>` to get more information about a command."""

def test_help_no_short_descr() -> None:
	class Test(ConfigFileCommand):

		'''
		usage: test foo [bar]
		'''

		def run(self, cmd: 'Sequence[str]') -> None:
			pass


	messages: 'list[Message]' = []

	cf = ConfigFile(appname='test', commands=(Help, Test))
	cf.set_ui_callback(messages.append)

	cf.parse_line("help")
	msg, = messages
	assert str(msg) == """\
The following commands are defined:
- help  Display help.
- test

Use `help <cmd>` to get more information about a command."""

def test_help_for_help_command() -> None:
	messages: 'list[Message]' = []

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(messages.append)

	cf.parse_line("help help")
	msg, = messages
	assert str(msg) == """\
usage: help [cmd]

Display help.

positional arguments:
  cmd  The command for which you want help"""

def test_help_for_undefined_command() -> None:
	messages: 'list[Message]' = []

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(messages.append)

	cf.parse_line("help undefined")
	msg, = messages
	assert str(msg) == "unknown command 'undefined' in line 'help undefined'"


def test__format_table__long_name() -> None:
	table = [
		('command-with-long-long-name', 'A description for the command with the long name'),
		('normal-command', 'A description for the command with the shorter name'),
	]
	cf = ConfigFile(appname='test')
	h = cf.command_dict['help']
	assert isinstance(h, Help)
	assert h.format_table(table) == '''\
command-with-long-long-name
                    A description for the command with the long name
normal-command      A description for the command with the shorter name'''

def test__format_table__long_descr() -> None:
	table = [
		('command-with-long-long-name', 'A description for the command with the long name'),
		('normal-command', 'A description for the command with the shorter name'),
	]
	cf = ConfigFile(appname='test')
	h = cf.command_dict['help']
	assert isinstance(h, Help)
	h.max_width = 40
	assert h.format_table(table) == '''\
command-with-long-long-name
                    A description for
                    the command with the
                    long name
normal-command      A description for
                    the command with the
                    shorter name'''
