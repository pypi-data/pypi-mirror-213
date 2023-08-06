#!../../../../venv/bin/pytest

import os
import io

import pytest

from utils import run

def raise_error(msg: object) -> None:
	raise AssertionError(msg)


def test_app_polite(monkeypatch: 'pytest.MonkeyPatch', capsys: 'pytest.CaptureFixture[str]') -> None:
	monkeypatch.setattr('sys.stdin', io.StringIO('hello, computer'))
	run('example_usage.py', nextto=__file__)
	assert capsys.readouterr().out == '>>> nice to meet you\n'

def test_app_rude(monkeypatch: 'pytest.MonkeyPatch', capsys: 'pytest.CaptureFixture[str]') -> None:
	monkeypatch.setattr('sys.stdin', io.StringIO('you are slow'))
	run('example_usage.py', nextto=__file__)
	assert capsys.readouterr().out == '>>> you are rude\n'

def test_invalid_re(monkeypatch: 'pytest.MonkeyPatch', capsys: 'pytest.CaptureFixture[str]') -> None:
	monkeypatch.setenv('EXAMPLE_GREETING', '[')
	monkeypatch.setattr('sys.stdin', io.StringIO('\n'))
	run('example_usage.py', nextto=__file__)
	assert capsys.readouterr().out == '''\
While loading environment variables:
invalid value for greeting: '[' (unterminated character set at position 0) while trying to parse environment variable EXAMPLE_GREETING='['
>>> you are rude\n'''

def test_definition() -> None:
	from .example_definition import Regex
	from confattr import Config, ConfigFile

	greeting = Config('greeting', Regex(r'(?i)(hello|hi)\b'), help='determine whether the user is polite or not')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(raise_error)
	cf.save(comments=False)
	assert greeting.value.match('hello world')
	assert not greeting.value.match('こんにちは')

	cf.parse_line('set greeting=こんにちは')
	assert not greeting.value.match('hello world')
	assert greeting.value.match('こんにちは')
	assert repr(greeting.value) == "Regex('こんにちは')"

	cf.load()
	assert greeting.value.match('hello world')
	assert not greeting.value.match('こんにちは')

def test_save() -> None:
	from confattr import ConfigFile
	run('example_save.py', nextto=__file__)
	cf = ConfigFile(appname='type_regex')
	fn_obtained = cf.get_save_path()
	fn_expected = os.path.join(os.path.dirname(__file__), 'expected-config')
	with open(fn_obtained, 'rt') as f_obtained:
		with open(fn_expected, 'rt') as f_expected:
			assert f_obtained.read() == f_expected.read()
