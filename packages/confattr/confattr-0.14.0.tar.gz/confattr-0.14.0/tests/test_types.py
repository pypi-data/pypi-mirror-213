#!../venv/bin/pytest -s

import os
import re
import shutil
import platform
from dataclasses import dataclass
from contextlib import contextmanager
from collections.abc import Sequence, Mapping, Iterator

import pytest

from confattr import Config, ConfigFile, Message, NotificationLevel
from confattr.types import Regex, CaseInsensitiveRegex, SubprocessCommandWithAlternatives, SubprocessCommand, TYPE_CONTEXT
from confattr import types


class ParseError(ValueError):
	pass

def ui_callback(msg: Message) -> None:
	if msg.notification_level is NotificationLevel.ERROR:
		raise ParseError(msg)


class MockRunAndPipe:

	@dataclass
	class Call:
		__slots__ = ('cmd', 'env', 'get_output')
		cmd: 'Sequence[str]'
		env: 'Mapping[str, str]'  # this can be None but I am ignoring that so that mypy does not always complain that None is not indexable
		get_output: bool

	def __init__(self) -> None:
		self.calls: 'list[MockRunAndPipe.Call]' = []

	def __call__(self, cmds: 'Sequence[str]', *, get_output: bool = False, env: 'Mapping[str, str]|None' = None) -> None:
		self.calls.append(self.Call(
			cmd = cmds,
			get_output = get_output,
			env = env,  # type: ignore [arg-type]
		))

	def __len__(self) -> int:
		return len(self.calls)

	def __getitem__(self, i: int) -> 'Call':
		return self.calls[i]


@pytest.fixture(autouse=True)
def reset_python_callbacks() -> None:
	SubprocessCommand.python_callbacks.clear()


# ========== Regex ==========

def test__regex_alone() -> None:
	r = Regex('(?i)foo')
	assert r.match('FOO')
	assert not r.match('FFOO')

def test__regex() -> None:
	class Test:
		foo = Config('foo', Regex('(?i)foo'))

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)

	t = Test()
	assert t.foo.match('foo')
	assert t.foo.match('Foo')
	assert not t.foo.match('FFoo')

def test__regex_repr() -> None:
	r = Regex('foo|bar')
	assert repr(r) == "Regex('foo|bar')"

def test_save_and_load_regex() -> None:
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	
	class Test:
		c = Config('c', CaseInsensitiveRegex('foo'))
	t = Test()

	assert t.c.match('FOO')
	assert not t.c.match('BAR')
	cf.save()

	cf.parse_line('set c=bar')
	assert not t.c.match('FOO')
	assert t.c.match('BAR')


# ========== SubprocessCommand ==========

def test_save_and_load_command() -> None:
	WC_PATH = '{path}'
	class MyTestClass:
		cmd = Config('cmd.file-browser', SubprocessCommand(['ranger', WC_PATH]))

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t = MyTestClass()
	config_file.save()
	assert t.cmd == SubprocessCommand(['ranger', WC_PATH])

	t.cmd = SubprocessCommand(['xdg-open', WC_PATH])
	assert t.cmd == SubprocessCommand(['xdg-open', WC_PATH])

	config_file.load()
	assert t.cmd == SubprocessCommand(['ranger', WC_PATH])

def test_command_dunder_methods() -> None:
	cmd = SubprocessCommand(['ranger', 'a dir'])
	assert str(cmd) == "ranger 'a dir'"
	assert repr(cmd) == "SubprocessCommand(['ranger', 'a dir'], env=None)"

def test_command_with_env() -> None:
	cmd = SubprocessCommand(['git', '--paginate', 'diff', '--no-index', '--', '{path_from}', '{path_to}'], env=dict(GIT_PAGER='less -+F'))
	cmd_copy = SubprocessCommand(cmd)
	assert cmd == cmd_copy
	assert str(cmd) == str(cmd_copy)
	assert repr(cmd) == repr(cmd_copy)

	# mypy does not allow to modify env because it is declared as Mapping:
	#cmd_copy.env['GIT_WORK_TREE'] = '~'
	#cmd_copy.env['GIT_DIR'] = '~/.dotfiles'
	# instead I am assigning a new dict:
	assert cmd_copy.env is not None
	cmd_copy.env = dict(cmd_copy.env, GIT_WORK_TREE='~', GIT_DIR='~/.dotfiles')
	assert cmd != cmd_copy
	assert str(cmd) != str(cmd_copy)
	assert repr(cmd) != repr(cmd_copy)

def test_command_change_env() -> None:
	cmd = SubprocessCommand(['git', '--paginate', 'diff', '--no-index', '--', '{path_from}', '{path_to}'], env=dict(GIT_PAGER='less -+F'))
	cmd2 = SubprocessCommand(cmd, env=dict(GIT_WORK_TREE='~', GIT_DIR='~/.dotfiles'))
	assert cmd.cmd == cmd2.cmd
	assert cmd.env != cmd2.env
	assert cmd2.env == dict(GIT_PAGER='less -+F', GIT_WORK_TREE='~', GIT_DIR='~/.dotfiles')

def test_command_add_env() -> None:
	cmd = SubprocessCommand(['git', '--paginate', 'diff', '--no-index', '--', '{path_from}', '{path_to}'])
	cmd2 = SubprocessCommand(cmd, env=dict(GIT_WORK_TREE='~', GIT_DIR='~/.dotfiles'))
	assert cmd.cmd == cmd2.cmd
	assert cmd.env != cmd2.env
	assert cmd2.env == dict(GIT_WORK_TREE='~', GIT_DIR='~/.dotfiles')

def test_command_replace() -> None:
	cmd = SubprocessCommand(['git', '--paginate', 'diff', '--no-index', '--', '{path_from}', '{path_to}'], env=dict(GIT_PAGER='less -+F'))
	cmd_ready = cmd.replace('{path_from}', '/tmp/a').replace('{path_to}', '/tmp/b')
	assert cmd_ready.cmd == ['git', '--paginate', 'diff', '--no-index', '--', '/tmp/a', '/tmp/b']
	assert cmd_ready.env == dict(GIT_PAGER='less -+F')


def test__error__empty_command() -> None:
	c = Config('cmd.git-diff', SubprocessCommand(['gitd']))

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with pytest.raises(ParseError, match=re.escape("invalid value for cmd.git-diff: '' (cmd is empty)")):
		config_file.parse_line('set cmd.git-diff=')

def test__error__env_vars_without_command() -> None:
	c = Config('cmd.git-diff', SubprocessCommand(['gitd']))

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with pytest.raises(ParseError, match=re.escape("invalid value for cmd.git-diff: \"GIT_PAGER='less -+F'\" (cmd consists of environment variables only, there is no command to be executed)")):
		config_file.parse_line("set \"cmd.git-diff=GIT_PAGER='less -+F'\"")


# ========== SubprocessCommandWithAlternatives ==========

def test_save_and_load_command_with_alternatives() -> None:
	WC_PATH = '{path}'
	class MyTestClass:
		cmd = Config('cmd.file-browser', SubprocessCommandWithAlternatives([['ranger', WC_PATH], ['xdg-open', WC_PATH]]))

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t = MyTestClass()
	config_file.save()
	assert repr(t.cmd) == repr(SubprocessCommandWithAlternatives([['ranger', WC_PATH], ['xdg-open', WC_PATH]]))

	t.cmd = SubprocessCommandWithAlternatives([['vim', WC_PATH]])
	assert repr(t.cmd) == repr(SubprocessCommandWithAlternatives([['vim', WC_PATH]]))

	config_file.load()
	assert repr(t.cmd) == repr(SubprocessCommandWithAlternatives([['ranger', WC_PATH], ['xdg-open', WC_PATH]]))

def test_save_and_load_command_with_alternatives_with_env() -> None:
	PATH_SRC = '{path.src}'
	PATH_DST = '{path.dst}'
	PATH_FROM = '{path.change-from}'
	PATH_TO = '{path.change-to}'
	class MyTestClass:
		cmd = Config('cmd.diff', SubprocessCommandWithAlternatives([
			['vimdiff', PATH_SRC, PATH_DST],
			SubprocessCommand(['git', '--paginate', 'diff', '--no-index', '--', PATH_TO, PATH_FROM], env=dict(GIT_PAGER='less -+F')),
		]))

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t = MyTestClass()
	config_file.save()
	assert repr(t.cmd) == repr(SubprocessCommandWithAlternatives([
		['vimdiff', PATH_SRC, PATH_DST],
		SubprocessCommand(['git', '--paginate', 'diff', '--no-index', '--', PATH_TO, PATH_FROM], env=dict(GIT_PAGER='less -+F')),
	]))
	assert repr(t.cmd) != repr(SubprocessCommandWithAlternatives([
		['vimdiff', PATH_SRC, PATH_DST],
		SubprocessCommand(['git', '--paginate', 'diff', '--no-index', '--', PATH_TO, PATH_FROM]),  # same command except that env is missing
	]))

	t.cmd = SubprocessCommandWithAlternatives([['gitd', '--open-always', '--no-index', '--', PATH_TO, PATH_FROM]])
	assert repr(t.cmd) == repr(SubprocessCommandWithAlternatives([['gitd', '--open-always', '--no-index', '--', PATH_TO, PATH_FROM]]))

	config_file.load()
	assert repr(t.cmd) == repr(SubprocessCommandWithAlternatives([
		['vimdiff', PATH_SRC, PATH_DST],
		SubprocessCommand(['git', '--paginate', 'diff', '--no-index', '--', PATH_TO, PATH_FROM], env=dict(GIT_PAGER='less -+F')),
	]))

def test_command_with_alternative_dunder_methods(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(shutil, 'which', lambda cmd: cmd == 'xdg-open')
	cmd = SubprocessCommandWithAlternatives([SubprocessCommand(['ranger', 'a dir']), SubprocessCommand(['xdg-open', 'a dir']), SubprocessCommand(['vim', 'a dir'])])
	assert str(cmd) == "ranger 'a dir'||xdg-open 'a dir'||vim 'a dir'"
	assert repr(cmd) == "SubprocessCommandWithAlternatives([SubprocessCommand(['ranger', 'a dir'], env=None), SubprocessCommand(['xdg-open', 'a dir'], env=None), SubprocessCommand(['vim', 'a dir'], env=None)])"

def test_command_with_alternative__register_python_callback(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(shutil, 'which', lambda cmd: cmd == 'xdg-open')
	cmd = SubprocessCommandWithAlternatives([SubprocessCommand(['rifle']), SubprocessCommand(['xdg-open', 'a dir']), SubprocessCommand(['vim', 'a dir'])])
	assert cmd.get_preferred_command().cmd == ['xdg-open', 'a dir']
	assert not SubprocessCommand.has_python_callback('rifle')

	SubprocessCommand.register_python_callback('rifle', lambda cmd, context: None)
	assert SubprocessCommand.has_python_callback('rifle')
	assert cmd.get_preferred_command().cmd == ['rifle']

	SubprocessCommand.unregister_python_callback('rifle')
	assert not SubprocessCommand.has_python_callback('rifle')
	assert cmd.get_preferred_command().cmd == ['xdg-open', 'a dir']

def test_command_with_alternative__env(monkeypatch: pytest.MonkeyPatch) -> None:
	PATH_FROM = '{path.change-from}'
	PATH_TO = '{path.change-to}'
	cmd = SubprocessCommandWithAlternatives([
		['gitd', '--open-always', '--no-index', '--', PATH_TO, PATH_FROM],
		SubprocessCommand(['git', '--paginate', 'diff', '--no-index', '--', PATH_TO, PATH_FROM], env=dict(GIT_PAGER='less -+F')),
	])

	monkeypatch.setattr(shutil, 'which', lambda cmd: cmd == 'git')
	assert cmd.get_preferred_command().cmd == ['git', '--paginate', 'diff', '--no-index', '--', PATH_TO, PATH_FROM]
	assert cmd.get_preferred_command().env == {'GIT_PAGER' : 'less -+F'}

	monkeypatch.setattr(shutil, 'which', lambda cmd: cmd == 'git' or cmd=='gitd')
	assert cmd.get_preferred_command().cmd == ['gitd', '--open-always', '--no-index', '--', PATH_TO, PATH_FROM]
	assert cmd.get_preferred_command().env is None

def test_command_with_alternative_replace(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(shutil, 'which', lambda cmd: cmd == 'diff')
	cmd = SubprocessCommandWithAlternatives([
		SubprocessCommand(['git', '--paginate', 'diff', '--no-index', '--', '{path_from}', '{path_to}'], env=dict(GIT_PAGER='less -+F')),
		['diff', '{path_from}', '{path_to}'],
	])
	cmd_ready = cmd.replace('{path_from}', '/tmp/a').replace('{path_to}', '/tmp/b')
	assert cmd_ready.cmd == ['diff', '/tmp/a', '/tmp/b']
	assert not cmd_ready.env



def test_command_with_alternative_replace_and_run(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(shutil, 'which', lambda cmd: cmd == 'git' or cmd == 'diff')
	cmd = SubprocessCommandWithAlternatives([
		['gitd', '--no-index', '--', '{path_from}', '{path_to}'],
		SubprocessCommand(['git', '--paginate', 'diff', '--no-index', '--', '{path_from}', '{path_to}'], env=dict(GIT_PAGER='less -+F')),
		['diff', '{path_from}', '{path_to}'],
	])

	mock = MockRunAndPipe()
	monkeypatch.setattr(types, 'run_and_pipe', mock)
	cmd.replace('{path_from}', '/tmp/a').replace('{path_to}', '/tmp/b').run(context=None)
	assert len(mock) == 1
	assert mock[0].cmd == ['git', '--paginate', 'diff', '--no-index', '--', '/tmp/a', '/tmp/b']
	assert mock[0].env['GIT_PAGER'] == 'less -+F'

def test_command_with_alternative_run(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(shutil, 'which', lambda cmd: cmd == 'git' or cmd == 'gitd')
	cmd = SubprocessCommandWithAlternatives([
		['gitd'],
		SubprocessCommand(['git', '--paginate', 'diff'], env=dict(GIT_PAGER='less -+F')),
	])

	mock = MockRunAndPipe()
	monkeypatch.setattr(types, 'run_and_pipe', mock)
	cmd.run(context=None)
	assert len(mock) == 1
	assert mock[0].cmd == ['gitd']
	assert not mock[0].env

def test_command_with_alternative_run_with_context(monkeypatch: pytest.MonkeyPatch) -> None:
	@contextmanager
	def envcontext(cmd: 'SubprocessCommand') -> 'Iterator[SubprocessCommand]':
		yield SubprocessCommand(cmd, env={'CONTEXT': 'true'})

	monkeypatch.setattr(shutil, 'which', lambda cmd: cmd == 'git' or cmd == 'gitd')
	cmd = SubprocessCommandWithAlternatives([
		['gitd'],
		SubprocessCommand(['git', '--paginate', 'diff'], env=dict(GIT_PAGER='less -+F')),
	])

	mock = MockRunAndPipe()
	monkeypatch.setattr(types, 'run_and_pipe', mock)
	cmd.run(context=envcontext)
	assert len(mock) == 1
	assert mock[0].cmd == ['gitd']
	assert mock[0].env['CONTEXT'] == 'true'
	assert not cmd.get_preferred_command().env

def test_command_with_alternative_run_python_callback(monkeypatch: pytest.MonkeyPatch) -> None:
	@contextmanager
	def envcontext(cmd: 'SubprocessCommand') -> 'Iterator[SubprocessCommand]':
		yield SubprocessCommand(cmd, env={'CONTEXT': 'true'})

	mock = MockRunAndPipe()
	def callback(cmd: SubprocessCommand, context: TYPE_CONTEXT) -> None:
		assert context is envcontext
		mock(cmd.cmd, env=cmd.env)
	SubprocessCommand.register_python_callback('gitd', callback)

	monkeypatch.setattr(shutil, 'which', lambda cmd: cmd == 'git' or cmd == 'gitd')
	cmd = SubprocessCommandWithAlternatives([
		['gitd'],
		SubprocessCommand(['git', '--paginate', 'diff'], env=dict(GIT_PAGER='less -+F')),
	])

	mock_run_and_pipe = MockRunAndPipe()
	monkeypatch.setattr(types, 'run_and_pipe', mock_run_and_pipe)
	cmd.run(context=envcontext)
	assert len(mock_run_and_pipe) == 0
	assert len(mock) == 1
	assert mock[0].cmd == ['gitd']
	assert not mock[0].env   # context is passed but not executed in callback
	assert not cmd.get_preferred_command().env

def test_command_with_alternative_run_none_installed(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(shutil, 'which', lambda cmd: False)
	cmd = SubprocessCommandWithAlternatives([
		['gitd'],
		SubprocessCommand(['git', '--paginate', 'diff'], env=dict(GIT_PAGER='less -+F')),
	])

	mock = MockRunAndPipe()
	monkeypatch.setattr(types, 'run_and_pipe', mock)
	with pytest.raises(FileNotFoundError, match="none of the commands is installed"):
		cmd.replace('{path_from}', '/tmp/a').replace('{path_to}', '/tmp/b').run(context=None)
	assert len(mock) == 0


# ========== editor ==========

WC_FILE_NAME = SubprocessCommandWithAlternatives.WC_FILE_NAME

def test_editor__linux_cli__editor_set(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(platform, 'system', lambda: 'Linux')
	monkeypatch.setitem(os.environ, 'EDITOR', 'my-cli-editor')
	monkeypatch.setitem(os.environ, 'VISUAL', 'my-gui-editor')
	monkeypatch.setattr(shutil, 'which', lambda cmd: True)
	cmd = SubprocessCommandWithAlternatives.editor(visual=False)

	cmd.get_preferred_command().cmd == ['my-cli-editor', WC_FILE_NAME]

def test_editor_linux_cli__editor_unset(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(platform, 'system', lambda: 'Linux')
	monkeypatch.delitem(os.environ, 'EDITOR', raising=False)
	monkeypatch.setattr(shutil, 'which', lambda cmd: True)
	cmd = SubprocessCommandWithAlternatives.editor(visual=False)

	cmd.get_preferred_command().cmd == ['rifle', WC_FILE_NAME]


def test_editor_linux_gui__visual_set(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(platform, 'system', lambda: 'Linux')
	monkeypatch.setitem(os.environ, 'EDITOR', 'my-cli-editor')
	monkeypatch.setitem(os.environ, 'VISUAL', 'my-gui-editor')
	monkeypatch.setattr(shutil, 'which', lambda cmd: True)
	cmd = SubprocessCommandWithAlternatives.editor(visual=True)

	cmd.get_preferred_command().cmd == ['my-gui-editor', WC_FILE_NAME]

def test_editor_linux_gui__editor_unset(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(platform, 'system', lambda: 'Linux')
	monkeypatch.delitem(os.environ, 'VISUAL', raising=False)
	monkeypatch.setattr(shutil, 'which', lambda cmd: True)
	cmd = SubprocessCommandWithAlternatives.editor(visual=True)

	cmd.get_preferred_command().cmd == ['xdg-open', WC_FILE_NAME]


def test_editor_windows_gui__editor_unset(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(platform, 'system', lambda: 'Windows')
	monkeypatch.setattr(shutil, 'which', lambda cmd: True)
	cmd = SubprocessCommandWithAlternatives.editor(visual=True)

	cmd.get_preferred_command().cmd == ['notepad', WC_FILE_NAME]
