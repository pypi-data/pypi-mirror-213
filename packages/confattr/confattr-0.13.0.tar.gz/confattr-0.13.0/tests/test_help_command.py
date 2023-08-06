#!../venv/bin/pytest -vv

from confattr import ConfigFile, Message

def test_help_general() -> None:
	messages: 'list[Message]' = []

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(messages.append)

	cf.parse_line("help")
	msg, = messages
	assert str(msg) == """\
The following commands are defined:
- set
- include
- echo
- help

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
