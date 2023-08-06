#!../../../../venv/bin/pytest

import os

import pytest

from utils import run, run_and_get_stdout

def test__output(monkeypatch: pytest.MonkeyPatch) -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example.py')
	fn_expected_output = os.path.join(path, 'output.txt')
	monkeypatch.setenv('EXAMPLE_CONFIG_DIRECTORY', path)
	stdout = run_and_get_stdout(fn_script)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert stdout == expected_output

def test__output_no_include(monkeypatch: pytest.MonkeyPatch) -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example_no_include.py')
	fn_expected_output = os.path.join(path, 'output_no_include.txt')
	monkeypatch.setenv('EXAMPLE_CONFIG_DIRECTORY', path)
	stdout = run_and_get_stdout(fn_script)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert stdout == expected_output


def test__save() -> None:
	from confattr import Config, ConfigFile
	run('example.py', main=False, nextto=__file__)

	cs = Config('some string', 'hello world')
	cb = Config('some bool', True)
	cl = Config('some list', [1,2,3], unit='')

	config_file = ConfigFile(appname='test')
	def fail(msg: str) -> None:
		raise AssertionError(msg)
	config_file.set_ui_callback(lambda msg: fail(str(msg)))

	config_file.save()

	cs.value = 'foo'
	cb.value = False
	cl.value = [42]
	assert cs.value == 'foo'
	assert cb.value == False
	assert cl.value == [42]

	config_file.load()
	assert cs.value == 'hello world'
	assert cb.value == True
	assert cl.value == [1,2,3]
