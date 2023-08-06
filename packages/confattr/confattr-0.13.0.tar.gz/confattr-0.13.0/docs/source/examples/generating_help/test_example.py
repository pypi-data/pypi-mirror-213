#!../../../../venv/bin/pytest

import os
import sys

import pytest
from utils import run_and_get_stdout

from confattr import ConfigFile


def test__output(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(ConfigFile, 'config_directory', None)
	monkeypatch.setenv('HOME', '/home/username')
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example.py')
	fn_expected_output = os.path.join(path, 'output.txt')
	stdout = run_and_get_stdout(fn_script)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	if sys.version_info < (3, 10):
		expected_output = expected_output.replace('options:', 'optional arguments:')

	assert stdout == expected_output

def test_normal_config(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(ConfigFile, 'config_directory', None)
	monkeypatch.setenv('HOME', '/home/username')
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example_config.py')
	fn_expected_output = os.path.join(path, 'expected-config')
	stdout = run_and_get_stdout(fn_script)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert stdout == expected_output


def test_raw_help(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(ConfigFile, 'config_directory', None)
	monkeypatch.setenv('HOME', '/home/username')
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example_raw_help.py')
	fn_expected_output = os.path.join(path, 'expected-raw-help.txt')
	stdout = run_and_get_stdout(fn_script)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	if sys.version_info < (3, 10):
		expected_output = expected_output.replace('options:', 'optional arguments:')

	assert stdout == expected_output

def test_raw_config(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(ConfigFile, 'config_directory', None)
	monkeypatch.setenv('HOME', '/home/username')
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example_raw_config.py')
	fn_expected_output = os.path.join(path, 'expected-raw-config')
	stdout = run_and_get_stdout(fn_script)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert stdout == expected_output


def test_no_multi_help(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(ConfigFile, 'config_directory', None)
	monkeypatch.setenv('HOME', '/home/username')
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'no_multi_example.py')
	fn_expected_output = os.path.join(path, 'expected-no-multi-help.txt')
	stdout = run_and_get_stdout(fn_script)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	if sys.version_info < (3, 10):
		expected_output = expected_output.replace('options:', 'optional arguments:')

	assert stdout == expected_output

def test_no_multi_config(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(ConfigFile, 'config_directory', None)
	monkeypatch.setenv('HOME', '/home/username')
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'no_multi_example_config.py')
	fn_expected_output = os.path.join(path, 'expected-no-multi-config')
	stdout = run_and_get_stdout(fn_script)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert stdout == expected_output
