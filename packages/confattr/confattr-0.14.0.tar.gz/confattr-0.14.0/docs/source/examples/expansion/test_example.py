#!../../../../venv/bin/pytest

from utils import run_and_get_stdout

def test_example() -> None:
	stdout = run_and_get_stdout('example.py', nextto=__file__)
	assert stdout == ''
