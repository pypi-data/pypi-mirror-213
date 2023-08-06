#!../../../../venv/bin/pytest

import os

import pytest

from utils import run_and_get_stdout

def test__output(monkeypatch: pytest.MonkeyPatch) -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example.py')
	fn_expected_output = os.path.join(path, 'output.txt')
	monkeypatch.setenv('EXAMPLE_CONFIG_DIRECTORY', path)
	stdout = run_and_get_stdout(fn_script)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert stdout == expected_output
