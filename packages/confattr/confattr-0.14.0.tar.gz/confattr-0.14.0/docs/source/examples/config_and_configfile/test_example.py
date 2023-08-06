#!../../../../venv/bin/pytest

import os

import pytest

from utils import run_and_get_stdout

def test__accelerate() -> None:
	from .example import Car

	c1 = Car()
	assert c1.speed == 0
	assert c1.speed_limit == 50

	c1.accelerate(49)
	assert c1.speed == 49
	c1.accelerate(1)
	assert c1.speed == 50
	with pytest.raises(ValueError):
		c1.accelerate(1)
	assert c1.speed == 50


def test__print_config(capsys: 'pytest.CaptureFixture[str]') -> None:
	# is not executed again, so Conig.instances is empty so I cannot save or load but that does not matter for this test
	from .example import Car

	c1 = Car()
	c1.print_config()
	captured = capsys.readouterr()
	assert captured.out == "traffic-law.speed-limit: 50\n"


def test__output(monkeypatch: pytest.MonkeyPatch) -> None:
	# output.txt does not contain "configuration was written to ..." because print is redefined to do nothing
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example.py')
	fn_expected_output = os.path.join(path, 'output.txt')
	monkeypatch.setenv('EXAMPLE_CONFIG_DIRECTORY', path)
	stdout = run_and_get_stdout(fn_script)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert stdout == expected_output

	with open(os.path.join(path, 'expected-config'), 'rt') as f:
		expected_config = f.read()
	with open(os.path.join(path, 'exported-config'), 'rt') as f:
		exported_config = f.read()
	assert exported_config == expected_config
