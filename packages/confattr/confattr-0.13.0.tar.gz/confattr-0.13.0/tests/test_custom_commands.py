#!../venv/bin/pytest -s

import os
from argparse import ArgumentParser, Namespace
from collections.abc import Sequence

import pytest

from confattr import ConfigFileCommand, ConfigFileArgparseCommand, ParseException, ConfigFile, Config, MultiConfig, Message, FormattedWriter, SectionLevel
from confattr.configfile import Set, Include

if False:
	from typing_extensions import Unpack  # type: ignore [unreachable]
	from confattr import SaveKwargs


class ConfigError(Exception):
	pass

def raise_error(msg: Message) -> None:
	raise ConfigError(msg.message)


# ------- replace = False -------

def test_custom_subclass() -> None:
	class SetAndLog(Set):
		pass

	assert Set in ConfigFileCommand.get_command_types()
	assert SetAndLog in ConfigFileCommand.get_command_types()
	assert SetAndLog.get_name() != Set.get_name()
	assert list(SetAndLog.get_names()) == [SetAndLog.get_name()]

def test_custom_classes() -> None:
	class Parent(ConfigFileCommand):
		name = 'foo'

	class Child(Parent):
		pass

	assert Parent in ConfigFileCommand.get_command_types()
	assert Child in ConfigFileCommand.get_command_types()
	assert Child.get_name() != Parent.get_name()
	assert list(Child.get_names()) == [Child.get_name()]

	assert Parent.get_name() == 'foo'
	assert Child.get_name() == 'child'

def test_custom_classes_with_aliases() -> None:
	class Parent(ConfigFileCommand):
		name = 'foo'
		aliases = ('bar', 'baz')

	class Child(Parent):
		pass

	assert Parent in ConfigFileCommand.get_command_types()
	assert Child in ConfigFileCommand.get_command_types()
	assert Child.get_name() != Parent.get_name()
	assert list(Child.get_names()) == [Child.get_name()]

	assert list(Parent.get_names()) == ['foo', 'bar', 'baz']
	assert list(Child.get_names()) == ['child']


def test_more_commands_that_implement_save() -> None:
	class Map(ConfigFileCommand):
		def run(self, cmd: 'Sequence[str]') -> None:
			pass
		def save(self, writer: 'FormattedWriter', **kw: 'Unpack[SaveKwargs]') -> None:
			if self.should_write_heading:
				writer.write_heading(SectionLevel.SECTION, 'Key mappings')
			writer.write_command('map <space> activate')

	c = Config('a', 'A')

	messages: 'list[Message]' = []
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(messages.append)
	fn = cf.save(comments=False)

	with open(fn, 'rt') as f:
		assert f.read() == '''\
# ========
# Settings
# ========
set a = A


# ============
# Key mappings
# ============
map <space> activate
'''

def test_more_commands_that_implement_save_with_multi_config() -> None:
	class Map(ConfigFileCommand):
		def run(self, cmd: 'Sequence[str]') -> None:
			pass
		def save(self, writer: 'FormattedWriter', **kw: 'Unpack[SaveKwargs]') -> None:
			if self.should_write_heading:
				writer.write_heading(SectionLevel.SECTION, 'Key mappings')
			writer.write_command('map <enter> activate')

	c = MultiConfig('m', 'A')

	messages: 'list[Message]' = []
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(messages.append)
	fn = cf.save(comments=False)

	with open(fn, 'rt') as f:
		assert f.read() == '''\
# ========
# Settings
# ========
set m = A


# ============
# Key mappings
# ============
map <enter> activate
'''

def test_help_attr() -> None:
	class Cmd1(ConfigFileCommand):

		'''
		Documentation for programmers
		'''

		help = '''
		Help for users
		'''

		name = 'foo'

		def run(self, cmd: 'Sequence[str]') -> None:
			pass

	cf = ConfigFile(appname='test', commands=[Cmd1])
	assert cf.command_dict['foo'].get_help() == 'Help for users'



def test_error_duplicate_name() -> None:
	class Cmd1(ConfigFileCommand):
		name = 'foo'

	with pytest.raises(ValueError, match="duplicate command name 'foo'"):
		class Cmd2(ConfigFileCommand):
			name = 'foo'


# ------- replace = True -------

def test_replace() -> None:
	class MySet(Set, replace=True):
		pass

	assert Set not in ConfigFileCommand.get_command_types()
	assert MySet in ConfigFileCommand.get_command_types()
	assert MySet.name == Set.get_name()
	assert list(MySet.get_names()) == list(Set.get_names())

def test_replace_with_explicit_name() -> None:
	class Parent(ConfigFileCommand):
		name = 'foo'

	class Replacement(Parent, replace=True):
		pass

	assert Parent not in ConfigFileCommand.get_command_types()
	assert Replacement in ConfigFileCommand.get_command_types()
	assert Replacement.name == Parent.name
	assert list(Replacement.get_names()) == list(Parent.get_names())

def test_replace_with_aliases() -> None:
	class Parent(ConfigFileCommand):
		aliases = ('foo', 'bar')

	class Replacement(Parent, replace=True):
		pass

	assert Parent not in ConfigFileCommand.get_command_types()
	assert Replacement in ConfigFileCommand.get_command_types()
	assert Replacement.get_name() == Parent.get_name()
	assert list(Replacement.get_names()) == list(Parent.get_names())
	assert list(Replacement.get_names()) == ['parent', 'foo', 'bar']

def test_replace_with_new_name() -> None:
	class Parent(ConfigFileCommand):
		pass

	class Replacement(Parent, replace=True):
		name = 'new'

	assert Parent not in ConfigFileCommand.get_command_types()
	assert Replacement in ConfigFileCommand.get_command_types()
	assert Replacement.name != Parent.get_name()
	assert Replacement.name == 'new'
	assert list(Replacement.get_names())[1:] == list(Parent.get_names())[1:]

def test_replace_with_new_aliases() -> None:
	class Parent(ConfigFileCommand):
		aliases = ['not-existing']

	class Replacement(Parent, replace=True):
		name = 'new'
		aliases = ['repl']

	assert Parent not in ConfigFileCommand.get_command_types()
	assert Replacement in ConfigFileCommand.get_command_types()
	assert Replacement.name != Parent.get_name()
	assert Replacement.name == 'new'
	assert list(Replacement.get_names()) == ['new', 'repl']



def test_double_replace() -> None:
	class Set1(Set, replace=True):
		name = 'set1'
	class Set2(Set, replace=True):
		name = 'set2'


def test_multiple_inheritance() -> None:
	class SetOrInclude(Set, Include, replace=True):

		def run(self, cmd: 'Sequence[str]') -> None:
			try:
				self.ui_notifier.show_error(f'trying include for {cmd}')
				Include.run(self, cmd)
			except ParseException:
				self.ui_notifier.show_error(f'falling back to set for {cmd}')
				Set.run(self, cmd)

	c = Config('a', '1')

	messages: 'list[Message]' = []
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(messages.append)

	fn = os.path.join(os.path.dirname(cf.get_save_path()), 'file')
	with open(fn, 'wt') as f:
		f.write('set a A')

	cf.parse_line('include file')
	assert c.value == 'A'

	assert [msg.message for msg in messages] == [
		"trying include for ['include', 'file']",
		"trying include for ['set', 'a', 'A']",
		"falling back to set for ['set', 'a', 'A']",
	]


def test_default_command() -> None:
	class SimpleSet(ConfigFileArgparseCommand, replace=True):
		name = 'set'
		aliases = ('',)

		@classmethod
		def init_parser(cls, parser: ArgumentParser) -> None:
			parser.add_argument('key')
			parser.add_argument('value')

		def run_parsed(self, args: Namespace) -> None:
			if args.key not in self.config_file.config_instances:
				raise ParseException('unknown setting %r' % args.key)

			config = self.config_file.config_instances[args.key]
			try:
				val = self.config_file.parse_value(config, args.value, raw=False)
				config.set_value(self.config_file.config_id, val)
				self.ui_notifier.show_info('set %s to %s' % (config.key, config.value))
			except ValueError as e:
				self.ui_notifier.show_error(str(e))

	c = Config('foo', 0, unit='apples')

	cf = ConfigFile(appname='test', commands=[SimpleSet])
	cf.set_ui_callback(raise_error)

	cf.parse_line('set foo 1')
	assert c.value == 1

	cf.parse_line('foo 2')
	assert c.value == 2

	with pytest.raises(ConfigError, match="unknown setting 'bar'"):
		cf.parse_line('bar 2')
