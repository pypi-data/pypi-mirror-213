#!../../../../venv/bin/pytest

import os

import pytest
import urwid

from confattr import ConfigFile

from utils import run, raise_error


@pytest.fixture(autouse=True)
def reset(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(urwid, 'command_map', urwid.command_map.copy())


def test__example_1() -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example_1.py')
	run(fn_script)

	# I am not checking the output to avoid a fail if urwid.command_map changes
	# but I at least want to make sure that it runs without raising an exception

def test__example_1_run() -> None:
	run('example_1.py', nextto=__file__, main=False)

	urwid.command_map[' '] = 'foo'
	cf = ConfigFile(appname='test-map')
	cf.set_ui_callback(raise_error)
	cf.parse_line("map ' ' bar")
	assert urwid.command_map[' '] == 'bar'


def test__output__example_3() -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example_3.py')
	fn_expected_output = os.path.join(path, 'config_expected')
	fn_generated_output = os.path.join(path, 'config')
	run(fn_script)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	with open(fn_generated_output, 'rt') as f:
		generated_output = f.read()

	assert generated_output == expected_output

def test__example_3_run() -> None:
	run('example_3.py', nextto=__file__, main=False)

	urwid.command_map[' '] = 'foo'
	cf = ConfigFile(appname='test-map')
	cf.set_ui_callback(raise_error)
	cf.parse_line("map ' ' bar")
	assert urwid.command_map[' '] == 'bar'
