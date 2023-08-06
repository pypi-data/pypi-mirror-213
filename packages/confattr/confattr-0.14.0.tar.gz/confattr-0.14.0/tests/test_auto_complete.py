#!../venv/bin/pytest -vv

import os
import platform
import enum
import argparse
from collections.abc import Sequence

import pytest

from confattr import ConfigFile, ConfigFileCommand, ConfigFileArgparseCommand, Config, MultiConfig, Message


def raise_error(msg: object) -> None:
	raise AssertionError(msg)

@pytest.fixture
def cf_diff() -> ConfigFile:
	class Diff(ConfigFileArgparseCommand):

		name = 'diff'

		def init_parser(self, parser: argparse.ArgumentParser) -> None:
			parser.add_argument('-y', '--side-by-side', action='store_true')
			parser.add_argument('-C', '--context', type=int, default=0)
			parser.add_argument('file1', choices=['old', 'first file'])
			parser.add_argument('file2', choices=['new', 'second file'])

		def run_parsed(self, args: argparse.Namespace) -> None:
			pass

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(raise_error)
	return cf

@pytest.fixture
def cf_git_log() -> ConfigFile:
	class GitLog(ConfigFileArgparseCommand):

		name = 'git'

		def init_parser(self, parser: argparse.ArgumentParser) -> None:
			parser.add_argument('cmd', choices=('log', 'diff', 'show'))
			parser.add_argument('--format', choices=('oneline', 'short', 'medium', 'full', 'fuller', 'reference', 'email', 'raw'))

		def run_parsed(self, args: argparse.Namespace) -> None:
			pass

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(raise_error)
	return cf

@pytest.fixture
def cf_tox() -> ConfigFile:
	class Tox(ConfigFileArgparseCommand):

		name = 'tox'

		def init_parser(self, parser: argparse.ArgumentParser) -> None:
			parser.add_argument('-e', choices=('py3', 'py36', 'mypy'))
			parser.add_argument('-v', '--verbose', action='store_true')
			parser.add_argument('pytestpath', choices=('src/', 'tests/'))

		def run_parsed(self, args: argparse.Namespace) -> None:
			pass

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(raise_error)
	return cf


# ---------- split line ----------

def test__split_line_ignore_errors__behaves_like__split_line() -> None:
	cf = ConfigFile(appname='test')
	for s in (
		'',
		'test',
		'include config',
		'set a=b',
		"set b='42'",
		"set b=' 42 '",
		'set a "foo  bar"',
		'set progress=25%',
		'set foo bar  #test comment',
	):
		assert cf.split_line_ignore_errors(s) == cf.split_line(s)

def test__split_line_ignore_errors__error_handling_in_second_iteration() -> None:
	cf = ConfigFile(appname='test')
	assert cf.split_line_ignore_errors("set foo='a  n  b") == ['set', "foo=a  n  b"]

def test__split_line_ignore_errors__error_handling_in_first_iteration() -> None:
	cf = ConfigFile(appname='test')
	assert cf.split_line_ignore_errors("'set foo=a  #test") == ['set foo=a  #test']


def test__split_line_ignore_errors__empty_arg() -> None:
	cf = ConfigFile(appname='test')
	assert cf.split_line_ignore_errors("set tab='    ") == ['set', 'tab=    ']


def test_complete_inclomplete_space_arg() -> None:
	cf = ConfigFile(appname='test')
	before_cursor = "set tab='    "
	after_cursor = ""
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == []
	assert start_of_line == 'set tab='

def test_complete_complete_space_arg() -> None:
	cf = ConfigFile(appname='test')
	before_cursor = "set tab='  "
	after_cursor = "  '"
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == []
	assert start_of_line == 'set tab='

def test_complete_backslash_space() -> None:
	cf = ConfigFile(appname='test')
	before_cursor = r"set tab=\ \ "
	after_cursor = "  a=1"
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == '  a=1'
	assert completions == []
	assert start_of_line == 'set tab='


# ---------- nothing in same argument after cursor ----------

def test_complete_dont_crash_on_comment() -> None:
	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'set #'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == []
	assert start_of_line == 'set #'

def test_complete_dont_crash_on_comment_char_in_arg() -> None:
	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'set f#'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	# in bash f# would be one argument but shlex treats the # as comment character and therefore ends the argument before the #
	assert end_of_line == '#'
	assert completions == []
	assert start_of_line == 'set '

def test_complete_comment_after_cursor() -> None:
	Config('foo', '42')

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'set '
	after_cursor = ' # ignore this'
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == after_cursor
	assert completions == ['foo']
	assert start_of_line == before_cursor


def test_complete_command_name() -> None:
	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = ''
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['set', 'include', 'echo', 'help']
	assert start_of_line == ''

def test_complete_command_name_no_one_letter_abbreviations() -> None:
	class Se(ConfigFileCommand):
		def run(self, cmd: 'Sequence[str]') -> None:
			pass
	class Send(ConfigFileCommand):
		aliases = ('s',)
		def run(self, cmd: 'Sequence[str]') -> None:
			pass
	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 's'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['set', 'se', 'send']
	assert start_of_line == ''

def test_complete_argparse_option() -> None:
	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'include -'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['--reset-config-id-before', '--no-reset-config-id-after']
	assert start_of_line == 'include '

def test_complete_argparse_option_value() -> None:
	class TestCommand(ConfigFileArgparseCommand):
		name = 'test'
		def init_parser(self, parser: argparse.ArgumentParser) -> None:
			parser.add_argument('-f', '--foo', choices=['foo', 'bar', 'baz'])
			parser.add_argument('-p', '--prime', type=int, choices=[2,3,5,7])

		def run_parsed(self, args: argparse.Namespace) -> None:
			raise NotImplementedError()

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'test -f='
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['foo', 'bar', 'baz']
	assert start_of_line == 'test -f='

def test_complete_argparse_unknown_option_value() -> None:
	class TestCommand(ConfigFileArgparseCommand):
		name = 'test'
		def init_parser(self, parser: argparse.ArgumentParser) -> None:
			parser.add_argument('-f', '--foo', choices=['foo', 'bar', 'baz'])
			parser.add_argument('-p', '--prime', type=int, choices=[2,3,5,7])

		def run_parsed(self, args: argparse.Namespace) -> None:
			raise NotImplementedError()

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'test -g='
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == []
	assert start_of_line == 'test -g='

def test_complete_argparse_option_value_int() -> None:
	class TestCommand(ConfigFileArgparseCommand):
		name = 'test'
		def init_parser(self, parser: argparse.ArgumentParser) -> None:
			parser.add_argument('-f', '--foo', choices=['foo', 'bar', 'baz'])
			parser.add_argument('-p', '--prime', type=int, choices=[2,3,5,7])

		def run_parsed(self, args: argparse.Namespace) -> None:
			raise NotImplementedError()

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'test --prime='
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['2', '3', '5', '7']
	assert start_of_line == 'test --prime='


def test_complete__set__no_start() -> None:
	Config('color.error', 'red')
	Config('color.warning', 'yellow')
	Config('text.greeting', 'hello world')

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'set '
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['color.error', 'color.warning', 'text.greeting']
	assert start_of_line == 'set '

def test_complete__set__setting() -> None:
	Config('color.error', 'red')
	Config('color.warning', 'yellow')
	Config('text.greeting', 'hello world')

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'set col'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['color.error', 'color.warning']
	assert start_of_line == 'set '

def test_complete__set_vim_style__setting_2() -> None:
	Config('color.error', 'red')
	Config('color.warning', 'yellow')
	Config('text.greeting', 'hello world')

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'set color.warning=orange t'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['text.greeting']
	assert start_of_line == 'set color.warning=orange '

def test_complete__set_vim_style__value() -> None:
	class Color(enum.Enum):
		BLACK = enum.auto()
		WHITE = enum.auto()
	Config('color.fg', Color.WHITE)
	Config('color.bg', Color.BLACK)

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'set color.fg='
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['black', 'white']
	assert start_of_line == 'set color.fg='


def test_complete__set_vim_style__list_value() -> None:
	class Flavor(enum.Enum):
		VANILLA = enum.auto()
		STRAWBERRY = enum.auto()
	MultiConfig('flavors', [Flavor.VANILLA])

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'set undefed=foo flavors=vanilla,straw'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['strawberry']
	assert start_of_line == 'set undefed=foo flavors=vanilla,'

def test_complete__set_vim_style__list_first_value() -> None:
	class Flavor(enum.Enum):
		VANILLA = enum.auto()
		STRAWBERRY = enum.auto()
	MultiConfig('flavors', [Flavor.VANILLA])

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'set undefed=foo flavors=van'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['vanilla']
	assert start_of_line == 'set undefed=foo flavors='

def test_complete__set_vim_style__list_third_value() -> None:
	class Flavor(enum.Enum):
		VANILLA = enum.auto()
		STRAWBERRY = enum.auto()
	MultiConfig('flavors', [Flavor.VANILLA])

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'set undefed=foo flavors=vanilla,vanilla,s'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['strawberry']
	assert start_of_line == 'set undefed=foo flavors=vanilla,vanilla,'


def test_complete__set_vim_style__first_dict_key() -> None:
	class Sweets(enum.Enum):
		ICE_CREAM = enum.auto()
		SIRUP = enum.auto()
	class Flavor(enum.Enum):
		VANILLA = enum.auto()
		STRAWBERRY = enum.auto()
	Config('dessert', {Sweets.ICE_CREAM : Flavor.VANILLA})

	cf = ConfigFile(appname='test')
	before_cursor = 'set undefed=foo dessert=ice'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['ice-cream']
	assert start_of_line == 'set undefed=foo dessert='

def test_complete__set_vim_style__first_dict_value() -> None:
	class Sweets(enum.Enum):
		ICE_CREAM = enum.auto()
		SIRUP = enum.auto()
	class Flavor(enum.Enum):
		VANILLA = enum.auto()
		STRAWBERRY = enum.auto()
	Config('dessert', {Sweets.ICE_CREAM : Flavor.VANILLA})

	cf = ConfigFile(appname='test')
	before_cursor = 'set undefed=foo dessert=ice-cream:va'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['vanilla']
	assert start_of_line == 'set undefed=foo dessert=ice-cream:'

def test_complete__set_vim_style__second_dict_key() -> None:
	class Sweets(enum.Enum):
		ICE_CREAM = enum.auto()
		SIRUP = enum.auto()
	class Flavor(enum.Enum):
		VANILLA = enum.auto()
		STRAWBERRY = enum.auto()
	Config('dessert', {Sweets.ICE_CREAM : Flavor.VANILLA})

	cf = ConfigFile(appname='test')
	before_cursor = 'set undefed=foo dessert=ice-cream:vanilla,s'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['sirup']
	assert start_of_line == 'set undefed=foo dessert=ice-cream:vanilla,'

def test_complete__set_vim_style__second_dict_value() -> None:
	class Sweets(enum.Enum):
		ICE_CREAM = enum.auto()
		SIRUP = enum.auto()
	class Flavor(enum.Enum):
		VANILLA = enum.auto()
		STRAWBERRY = enum.auto()
	Config('dessert', {Sweets.ICE_CREAM : Flavor.VANILLA})

	cf = ConfigFile(appname='test')
	before_cursor = 'set undefed=foo dessert=ice-cream:vanilla,sirup:str'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['strawberry']
	assert start_of_line == 'set undefed=foo dessert=ice-cream:vanilla,sirup:'

def test_complete__set_vim_style__third_dict_key() -> None:
	class Sweets(enum.Enum):
		ICE_CREAM = enum.auto()
		SIRUP = enum.auto()
	class Flavor(enum.Enum):
		VANILLA = enum.auto()
		STRAWBERRY = enum.auto()
	Config('dessert', {Sweets.ICE_CREAM : Flavor.VANILLA})

	cf = ConfigFile(appname='test')
	before_cursor = 'set undefed=foo dessert=,ice-cream:vanilla,s'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['sirup']
	assert start_of_line == 'set undefed=foo dessert=,ice-cream:vanilla,'

def test_complete__set_vim_style__third_dict_value() -> None:
	class Sweets(enum.Enum):
		ICE_CREAM = enum.auto()
		SIRUP = enum.auto()
	class Flavor(enum.Enum):
		VANILLA = enum.auto()
		STRAWBERRY = enum.auto()
	Config('dessert', {Sweets.ICE_CREAM : Flavor.VANILLA})

	cf = ConfigFile(appname='test')
	before_cursor = 'set undefed=foo dessert=,ice-cream:vanilla,sirup:str'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['strawberry']
	assert start_of_line == 'set undefed=foo dessert=,ice-cream:vanilla,sirup:'


def test_complete__set_ranger_style__value() -> None:
	class Color(enum.Enum):
		BLACK = enum.auto()
		WHITE = enum.auto()
	Config('color.fg', Color.WHITE)
	Config('color.bg', Color.BLACK)

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'set color.fg '
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	# this cannot be a 2nd setting because the 1st setting does not have a value
	assert completions == ['black', 'white']
	assert start_of_line == 'set color.fg '

def test_complete__set_ranger_style__value_after_equals() -> None:
	class Color(enum.Enum):
		BLACK = enum.auto()
		WHITE = enum.auto()
	Config('color.fg', Color.WHITE)
	Config('color.bg', Color.BLACK)

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'set color.fg  = '
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['black', 'white']
	assert start_of_line == 'set color.fg  = '

def test_complete__set_ranger_style__no_completion_after_end() -> None:
	class Color(enum.Enum):
		BLACK = enum.auto()
		WHITE = enum.auto()
	Config('color.fg', Color.WHITE)
	Config('color.bg', Color.BLACK)

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'set color.fg  = white '
	after_cursor = ' # comment'
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ' # comment'
	assert completions == []
	assert start_of_line == 'set color.fg  = white '

def test_complete__set_ranger_style__expand_config() -> None:
	class Color(enum.Enum):
		BLACK = enum.auto()
		WHITE = enum.auto()
	Config('color.fg', Color.WHITE)
	Config('color.bg', Color.BLACK)

	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'set color.fg  = %'
	after_cursor = ' # comment'
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ' # comment'
	assert completions == ['color.bg', 'color.fg']
	assert start_of_line == 'set color.fg  = %'


def test_complete_between_args(monkeypatch: pytest.MonkeyPatch) -> None:
	cf = ConfigFile(appname='test', enable_config_ids=True)
	monkeypatch.setattr(os, 'listdir', lambda path: ['config', 'another'] if path == os.path.dirname(cf.get_save_path()) else [])
	monkeypatch.setattr(os.path, 'isdir', lambda path: False)
	before_cursor = 'include '
	after_cursor = ' file'
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))
	
	# in this very specific case a user would probably want to insert an option
	# but understanding that would be too complex
	# if a user wants to insert an option they need to say so by inserting a hyphen
	# without the hyphen it's treated as positional argument
	# that there is already a positional argument after it and this command accepts only a single positional argument is out of scope of auto completion
	assert end_of_line == after_cursor
	assert completions == ['config', 'another']
	assert start_of_line == before_cursor

def test_complete_after_last_arg(monkeypatch: pytest.MonkeyPatch) -> None:
	cf = ConfigFile(appname='test', enable_config_ids=True)
	monkeypatch.setattr(os, 'listdir', lambda path: ['config', 'another'] if path == os.path.dirname(cf.get_save_path()) else [])
	monkeypatch.setattr(os.path, 'isdir', lambda path: False)
	before_cursor = 'include '
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == after_cursor
	assert completions == ['config', 'another']
	assert start_of_line == before_cursor

def test_complete_indentation() -> None:
	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = '    include  -'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['--reset-config-id-before', '--no-reset-config-id-after']
	assert start_of_line == '    include  '


def test_complete_command() -> None:
	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'incl'
	after_cursor = ' # foo'
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ' # foo'
	assert completions == ['include']
	assert start_of_line == ''


def test_complete_config_id() -> None:
	cf = ConfigFile(appname='test', enable_config_ids=True)
	cf.set_ui_callback(raise_error)
	cf.parse_line('[foo-bar]')
	cf.parse_line('[foo-baz]')

	before_cursor = '[foo'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['[foo-bar]', '[foo-baz]']
	assert start_of_line == ''

def test_complete_after_invalid_config_id() -> None:
	cf = ConfigFile(appname='test', enable_config_ids=True)
	cf.set_ui_callback(raise_error)
	cf.parse_line('[foo-bar]')
	cf.parse_line('[foo-baz]')

	before_cursor = '[foo]'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == []
	assert start_of_line == ''

def test_complete_argparse_before_double_hyphen() -> None:
	class Tox(ConfigFileArgparseCommand):

		name = 'tox'

		def init_parser(self, parser: argparse.ArgumentParser) -> None:
			parser.add_argument('-r', '--recreate', action='store_true')
			parser.add_argument('pytestoptions', choices=('-k', '-s'))

		def run_parsed(self, args: argparse.Namespace) -> None:
			pass

	cf = ConfigFile(appname='test')

	before_cursor = 'tox -'
	after_cursor = ' -- -s'
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ' -- -s'
	# -k and -s are not suggested because they are choices of a positional argument
	# in this very rare case that a positional argument has choices starting with a hyphen
	# the user needs to insert a double hyphen before if they want to get auto completion
	assert completions == ['--recreate']
	assert start_of_line == 'tox '

def test_complete_argparse_after_double_hyphen() -> None:
	class Tox(ConfigFileArgparseCommand):

		name = 'tox'

		def init_parser(self, parser: argparse.ArgumentParser) -> None:
			parser.add_argument('-r', '--recreate', action='store_true')
			parser.add_argument('-e')
			parser.add_argument('pytestoptions', choices=('-k', '-s'))

		def run_parsed(self, args: argparse.Namespace) -> None:
			pass

	cf = ConfigFile(appname='test')

	before_cursor = 'tox -r -- -'
	after_cursor = ' -s'
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ' -s'
	assert completions == ['-k', '-s']
	assert start_of_line == 'tox -r -- '

def test_complete_argparse_last_arg_after_double_hyphen() -> None:
	class Tox(ConfigFileArgparseCommand):

		name = 'tox'

		def init_parser(self, parser: argparse.ArgumentParser) -> None:
			parser.add_argument('-r', '--recreate', action='store_true')
			parser.add_argument('-e')
			parser.add_argument('pytestoptions', choices=('-k', '-s'))

		def run_parsed(self, args: argparse.Namespace) -> None:
			pass

	cf = ConfigFile(appname='test')

	before_cursor = 'tox -r -- -s -'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == []
	assert start_of_line == 'tox -r -- -s '

def test_complete_argparse_positional_arg() -> None:
	class Diff(ConfigFileArgparseCommand):

		name = 'diff'

		def init_parser(self, parser: argparse.ArgumentParser) -> None:
			parser.add_argument('-y', '--side-by-side', action='store_true')
			parser.add_argument('-C', type=int)
			parser.add_argument('file1', choices=['old', 'first file'])
			parser.add_argument('file2', choices=['new', 'second file'])

		def run_parsed(self, args: argparse.Namespace) -> None:
			pass

	cf = ConfigFile(appname='test')

	before_cursor = 'diff -y old n'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['new']
	assert start_of_line == 'diff -y old '

def test_complete_argparse_filter_option_name(cf_diff: ConfigFile) -> None:
	before_cursor = 'diff --side'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf_diff.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['--side-by-side']
	assert start_of_line == 'diff '

def test_complete_argparse_action_without_choices(cf_diff: ConfigFile) -> None:
	before_cursor = 'diff --context='
	after_cursor = ''
	start_of_line, completions, end_of_line = cf_diff.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == []
	assert start_of_line == before_cursor

def test_complete_include_fallback_to_super() -> None:
	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'include --reset-config-id-before='
	after_cursor = ' file'
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ' file'
	assert completions == []
	assert start_of_line == before_cursor

def test__get_completions_if_positional_argument__first_arg(cf_diff: ConfigFile) -> None:
	ln = 'diff '
	start_of_line, completions, end_of_line = cf_diff.get_completions(ln, len(ln))
	assert completions == ['old', "'first file'"]
	assert start_of_line == ln
	assert end_of_line == ''
	
def test__get_completions_if_positional_argument__after_argless_option(cf_diff: ConfigFile) -> None:
	ln = 'diff -y '
	start_of_line, completions, end_of_line = cf_diff.get_completions(ln, len(ln))
	assert completions == ['old', "'first file'"]
	assert start_of_line == ln
	assert end_of_line == ''

def test__get_completions_if_positional_argument__after_option_with_given_eq_arg(cf_diff: ConfigFile) -> None:
	ln = 'diff -C=3 '
	start_of_line, completions, end_of_line = cf_diff.get_completions(ln, len(ln))
	assert completions == ['old', "'first file'"]
	assert start_of_line == ln
	assert end_of_line == ''

def test__get_completions_if_positional_argument__after_option_with_given_separate_arg(cf_diff: ConfigFile) -> None:
	ln = 'diff -C 3 '
	start_of_line, completions, end_of_line = cf_diff.get_completions(ln, len(ln))
	assert completions == ['old', "'first file'"]
	assert start_of_line == ln
	assert end_of_line == ''

def test__get_completions_if_positional_argument__after_option_with_combined_arg(cf_diff: ConfigFile) -> None:
	ln = 'diff -C3 '
	start_of_line, completions, end_of_line = cf_diff.get_completions(ln, len(ln))
	assert completions == ['old', "'first file'"]
	assert start_of_line == ln
	assert end_of_line == ''

def test__get_completions_if_positional_argument__after_combined_options_with_combined_arg(cf_diff: ConfigFile) -> None:
	ln = 'diff -yC3 '
	start_of_line, completions, end_of_line = cf_diff.get_completions(ln, len(ln))
	assert completions == ['old', "'first file'"]
	assert start_of_line == ln
	assert end_of_line == ''

def test__get_completions_if_positional_argument__after_combined_options_with_separate_arg(cf_diff: ConfigFile) -> None:
	ln = 'diff -yC 3 '
	start_of_line, completions, end_of_line = cf_diff.get_completions(ln, len(ln))
	assert completions == ['old', "'first file'"]
	assert start_of_line == ln
	assert end_of_line == ''

def test__get_completions_if_positional_argument__after_long_option_with_separate_arg(cf_diff: ConfigFile) -> None:
	ln = 'diff -y --context 3 '
	start_of_line, completions, end_of_line = cf_diff.get_completions(ln, len(ln))
	assert completions == ['old', "'first file'"]
	assert start_of_line == ln
	assert end_of_line == ''

def test__get_completions_if_positional_argument__after_long_option_with_eq_arg(cf_diff: ConfigFile) -> None:
	ln = 'diff -y --context=3 '
	start_of_line, completions, end_of_line = cf_diff.get_completions(ln, len(ln))
	assert completions == ['old', "'first file'"]
	assert start_of_line == ln
	assert end_of_line == ''

def test__get_completions_if_positional_argument__after_invalid_long_option(cf_diff: ConfigFile) -> None:
	ln = 'diff --invalid '
	start_of_line, completions, end_of_line = cf_diff.get_completions(ln, len(ln))
	assert completions == ['old', "'first file'"]
	assert start_of_line == ln
	assert end_of_line == ''

def test__get_completions_if_positional_argument__after_argless_option_and_pos_arg(cf_diff: ConfigFile) -> None:
	ln = 'diff --side-by-side 3 '
	start_of_line, completions, end_of_line = cf_diff.get_completions(ln, len(ln))
	assert completions == ['new', "'second file'"]
	assert start_of_line == ln
	assert end_of_line == ''


def test__get_completions_if_option_argument__separate(cf_git_log: ConfigFile) -> None:
	ln = 'git log --format fu'
	start_of_line, completions, end_of_line = cf_git_log.get_completions(ln, len(ln))
	assert completions == ['full', 'fuller']
	assert start_of_line == 'git log --format '
	assert end_of_line == ''

def test__get_completions_if_option_argument__eq(cf_git_log: ConfigFile) -> None:
	ln = 'git log --format=fu'
	start_of_line, completions, end_of_line = cf_git_log.get_completions(ln, len(ln))
	assert completions == ['full', 'fuller']
	assert start_of_line == 'git log --format='
	assert end_of_line == ''

def test__get_completions_if_option_argument__invalid_leading_flag(cf_tox: ConfigFile) -> None:
	ln = 'tox -xe '
	start_of_line, completions, end_of_line = cf_tox.get_completions(ln, len(ln))
	assert completions == ['py3', 'py36', 'mypy']
	assert start_of_line == ln
	assert end_of_line == ''

def test__get_completions_if_option_argument__invalid_trailing_flag(cf_tox: ConfigFile) -> None:
	ln = 'tox -vx '
	start_of_line, completions, end_of_line = cf_tox.get_completions(ln, len(ln))
	assert completions == ['src/', 'tests/']
	assert start_of_line == ln
	assert end_of_line == ''


def test__quote_path__tilde() -> None:
	cf = ConfigFile(appname='test')

	assert cf.quote_path('~') == '~'

def test__quote_path__tilde_slash() -> None:
	cf = ConfigFile(appname='test')

	assert cf.quote_path('~/') == '~/'

def test__quote_path__no_quote() -> None:
	cf = ConfigFile(appname='test')

	assert cf.quote_path('a/b/c') == 'a/b/c'

def test__quote_path__quote() -> None:
	cf = ConfigFile(appname='test')

	assert cf.quote_path('a/b c') == "a/'b c'"


def test__get_completions__include_rel_path(monkeypatch: pytest.MonkeyPatch) -> None:
	cf = ConfigFile(appname='test')
	def listdir(path: str) -> 'list[str]':
		if path == os.path.dirname(cf.get_save_path()):
			return ['config', 'other']
		return []
	monkeypatch.setattr(os.path, 'isdir', lambda path: False)
	monkeypatch.setattr(os, 'listdir', listdir)

	ln = 'include '
	start_of_line, completions, end_of_line = cf.get_completions(ln, len(ln))
	assert completions == ['config', 'other']
	assert start_of_line == ln
	assert end_of_line == ''

def test__get_completions__include_rel_path_with_pathsep(monkeypatch: pytest.MonkeyPatch) -> None:
	COLORS = ['white', 'yellow', 'black', 'blue']
	cf = ConfigFile(appname='test')
	def listdir(path: str) -> 'list[str]':
		if path == os.path.join(os.path.dirname(cf.get_save_path()), 'color'):
			return COLORS
		return []
	monkeypatch.setattr(os.path, 'isdir', lambda path: os.path.split(path)[1] not in COLORS)
	monkeypatch.setattr(os, 'listdir', listdir)

	ln = 'include color/b'.replace('/', os.path.sep)
	start_of_line, completions, end_of_line = cf.get_completions(ln, len(ln))
	assert completions == ['black', 'blue']
	assert start_of_line == ln.split(os.path.sep)[0] + os.path.sep
	assert end_of_line == ''

pytest.mark.skipif(platform.system() == 'Windows', reason='This test uses hard coded Unix-style paths.')
def test__get_completions__include_abs_path(monkeypatch: pytest.MonkeyPatch) -> None:
	cf = ConfigFile(appname='test')
	def listdir(path: str) -> 'list[str]':
		if path == '/':
			return ['bin', 'home', 'usr']
		elif path == '/home':
			return ['user1', 'user2']
		elif path == '/home/user1':
			return ['.config', 'file1', 'file2']
		return []
	def isdir(path: str) -> bool:
		return 'file' not in path
	monkeypatch.setattr(os, 'listdir', listdir)
	monkeypatch.setattr(os.path, 'isdir', isdir)

	ln = 'include /'
	start_of_line, completions, end_of_line = cf.get_completions(ln, len(ln))
	assert completions == ['bin/', 'home/', 'usr/']
	assert start_of_line == ln
	assert end_of_line == ''

	ln = 'include /home/'
	start_of_line, completions, end_of_line = cf.get_completions(ln, len(ln))
	assert completions == ['user1/', 'user2/']
	assert start_of_line == ln
	assert end_of_line == ''

	ln = 'include /home/user1/'
	start_of_line, completions, end_of_line = cf.get_completions(ln, len(ln))
	assert completions == ['file1', 'file2']
	assert start_of_line == ln
	assert end_of_line == ''

	ln = 'include /home/user1/.'
	start_of_line, completions, end_of_line = cf.get_completions(ln, len(ln))
	assert completions == ['.config/']
	assert start_of_line == 'include /home/user1/'
	assert end_of_line == ''

def test__get_completions__include_invalid_path() -> None:
	cf = ConfigFile(appname='test')
	ln = 'include /some/invalid/path/that/does/not/exist'
	start_of_line, completions, end_of_line = cf.get_completions(ln, len(ln))
	assert completions == []
	assert start_of_line == 'include /some/invalid/path/that/does/not/'
	assert end_of_line == ''

def test__get_completions_for_file_name__exclude(monkeypatch: pytest.MonkeyPatch) -> None:
	def listdir(path: str) -> 'list[str]':
		if path == '.':
			return ['abc', 'abc~']
		return []
	def isdir(path: str) -> bool:
		return False
	monkeypatch.setattr(os, 'listdir', listdir)
	monkeypatch.setattr(os.path, 'isdir', isdir)

	cf = ConfigFile(appname='test')
	start_of_line, completions, end_of_line = cf.get_completions_for_file_name('a', relative_to='.', start_of_line='', end_of_line='', exclude=r'.*~$')
	assert start_of_line == ''
	assert end_of_line == ''
	assert completions == ['abc']

def test__get_completions_for_file_name__include(monkeypatch: pytest.MonkeyPatch) -> None:
	def listdir(path: str) -> 'list[str]':
		if path == '.':
			return ['bat.dbc', 'bat.sym', 'bat.pdf']
		return []
	def isdir(path: str) -> bool:
		return False
	monkeypatch.setattr(os, 'listdir', listdir)
	monkeypatch.setattr(os.path, 'isdir', isdir)

	extensions = ('.dbc', '.sym')
	cf = ConfigFile(appname='test')
	start_of_line, completions, end_of_line = cf.get_completions_for_file_name('b', relative_to='.', start_of_line='', end_of_line='', include=lambda path, fn: any(fn.endswith(ext) for ext in extensions))
	assert start_of_line == ''
	assert end_of_line == ''
	assert completions == ['bat.dbc', 'bat.sym']

def test__get_completions_for_file_name__match(monkeypatch: pytest.MonkeyPatch) -> None:
	def listdir(path: str) -> 'list[str]':
		if path == '.':
			return ['bat_x.dbc', 'bat_y.dbc', 'bat_z.sym']
		return []
	def isdir(path: str) -> bool:
		return False
	monkeypatch.setattr(os, 'listdir', listdir)
	monkeypatch.setattr(os.path, 'isdir', isdir)

	cf = ConfigFile(appname='test')
	start_of_line, completions, end_of_line = cf.get_completions_for_file_name('x', relative_to='.', start_of_line='', end_of_line='', match=lambda path, name, start: start in name)
	assert start_of_line == ''
	assert end_of_line == ''
	assert completions == ['bat_x.dbc']


def test_complete_default_implementation() -> None:
	class Foo(ConfigFileCommand):

		name = 'foo'

		def run(self, cmd: 'Sequence[str]') -> None:
			pass

	cf = ConfigFile(appname='test', enable_config_ids=True)

	before_cursor = 'foo '
	after_cursor = ' # comment'
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == after_cursor
	assert completions == []
	assert start_of_line == before_cursor



def test_complete_echo_config() -> None:
	Config('foo', 'foo')
	Config('bar', 'bar')

	cf = ConfigFile(appname='test')
	before_cursor = 'echo foo=%'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['bar', 'foo']
	assert start_of_line == 'echo foo=%'

def test_complete_echo_config_not_applicable() -> None:
	Config('c1', 'foo')
	Config('c2', 'bar')

	cf = ConfigFile(appname='test')
	before_cursor = 'echo 100%%'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == []
	assert start_of_line == 'echo '

def test_complete_echo_env(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(os, 'environ', {'USER': 'me', 'HOME': '~'})

	cf = ConfigFile(appname='test')
	before_cursor = 'echo I am ${'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['HOME', 'USER']
	assert start_of_line == 'echo I am ${'

def test_complete_echo_env_not_applicable() -> None:
	cf = ConfigFile(appname='test')
	before_cursor = 'echo I am ${USER}'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == []
	assert start_of_line == 'echo I am '

def test_complete_echo_empty() -> None:
	cf = ConfigFile(appname='test')
	before_cursor = 'echo '
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == []
	assert start_of_line == 'echo '


def test_complete_help() -> None:
	cf = ConfigFile(appname='test')
	before_cursor = 'help s'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['set']
	assert start_of_line == 'help '

def test_complete_help_fallback() -> None:
	cf = ConfigFile(appname='test')
	before_cursor = 'help set '
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == []
	assert start_of_line == 'help set '


# ---------- 1 symbol commands ----------

@pytest.fixture
def cmd_next() -> None:
	MESSAGES = ('Status', 'Warning', 'Error')

	class Next(ConfigFileArgparseCommand):

		aliases = ('/',)

		def init_parser(self, parser: argparse.ArgumentParser) -> None:
			parser.add_argument('msg')

		def run_parsed(self, args: argparse.Namespace) -> None:
			self.ui_notifier.show_info(args.msg, ignore_filter=True)

		def get_completions_for_action(self, action: 'argparse.Action|None', start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
			if action and action.dest == 'msg':
				completions = [key for key in MESSAGES if key.startswith(start)]
				return start_of_line, completions, end_of_line

			return start_of_line, [], end_of_line

def test__1_symbol_command__empty_arg(cmd_next: None) -> None:
	cf = ConfigFile(appname='test')
	before_cursor = '/'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['Status', 'Warning', 'Error']
	assert start_of_line == '/'

def test__1_symbol_command__1_letter(cmd_next: None) -> None:
	cf = ConfigFile(appname='test')
	before_cursor = '/S'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == ['Status']
	assert start_of_line == '/'

def test__1_symbol_command__with_trailing_arg(cmd_next: None) -> None:
	cf = ConfigFile(appname='test')
	before_cursor = '/'
	after_cursor = ' 2'
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ' 2'
	assert completions == ['Status', 'Warning', 'Error']
	assert start_of_line == '/'

def test__1_symbol_command__comment(cmd_next: None) -> None:
	cf = ConfigFile(appname='test')
	before_cursor = '/'
	after_cursor = '  # comment'
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == '  # comment'
	assert completions == ['Status', 'Warning', 'Error']
	assert start_of_line == '/'

def test__1_symbol_command__dont_crash_on_comment(cmd_next: None) -> None:
	cf = ConfigFile(appname='test')
	before_cursor = '/Status #'
	after_cursor = ''
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ''
	assert completions == []
	assert start_of_line == '/Status #'

def test__parse_line__1_symbol_command(cmd_next: None) -> None:
	cf = ConfigFile(appname='test')
	cf.parse_line('/Status')
	
	messages: 'list[Message]' = []
	cf.set_ui_callback(messages.append)
	assert len(messages) == 1
	assert messages[0].message == 'Status'


# ---------- replace argument ----------

def test_complete_replace_arg() -> None:
	cf = ConfigFile(appname='test', enable_config_ids=True)
	before_cursor = 'include --'
	after_cursor = 'reset file'
	start_of_line, completions, end_of_line = cf.get_completions(before_cursor + after_cursor, len(before_cursor))

	assert end_of_line == ' file'
	assert completions == ['--reset-config-id-before', '--no-reset-config-id-after']
	assert start_of_line == 'include '


# ---------- quote ----------

# quoting of positional arguments of ConfigFileArgparseCommand is tested above with cf_diff

def test__get_completions_for_file_name__quote_completions(monkeypatch: pytest.MonkeyPatch) -> None:
	def listdir(path: str) -> 'list[str]':
		return ['abc1', 'abc  def']
	def isdir(path: str) -> bool:
		return False
	monkeypatch.setattr(os, 'listdir', listdir)
	monkeypatch.setattr(os.path, 'isdir', isdir)

	cf = ConfigFile(appname='test')
	ln = 'include '
	start_of_line, completions, end_of_line = cf.get_completions(ln, len(ln))
	assert start_of_line == ln
	assert end_of_line == ''
	assert completions == ['abc1', "'abc  def'"]

pytest.mark.skipif(platform.system() == 'Windows', reason='This test uses hard coded Unix-style paths.')
def test__get_completions_for_file_name__quote_entire_path(monkeypatch: pytest.MonkeyPatch) -> None:
	def listdir(path: str) -> 'list[str]':
		return ['abc1', 'abc  def']
	def isdir(path: str) -> bool:
		return False
	monkeypatch.setattr(os, 'listdir', listdir)
	monkeypatch.setattr(os.path, 'isdir', isdir)

	cf = ConfigFile(appname='test')
	ln = 'include "a dir/sub dir/'
	start_of_line, completions, end_of_line = cf.get_completions(ln, len(ln))
	assert start_of_line == "include 'a dir'/'sub dir'/"
	assert end_of_line == ""
	assert completions == ['abc1', "'abc  def'"]

def test_set_quote_arg_ranger_style() -> None:
	values = ['hello world', 'hey you', 'x']
	Config('greeting', values[0], allowed_values=values)

	cf = ConfigFile(appname='test')
	ln = 'set greeting '
	start_of_line, completions, end_of_line = cf.get_completions(ln, len(ln))
	assert start_of_line == ln
	assert end_of_line == ''
	assert completions == ["'hello world'", "'hey you'", 'x']

def test_set_quote_arg_vim_style() -> None:
	values = ['hello world', 'hey you', 'x']
	Config('greeting', values[0], allowed_values=values)

	cf = ConfigFile(appname='test')
	ln = 'set greeting='
	start_of_line, completions, end_of_line = cf.get_completions(ln, len(ln))
	assert start_of_line == ln
	assert end_of_line == ''
	assert completions == ["'hello world'", "'hey you'", 'x']
