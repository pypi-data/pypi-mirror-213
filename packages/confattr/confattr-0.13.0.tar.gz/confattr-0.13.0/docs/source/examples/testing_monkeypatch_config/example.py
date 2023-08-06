#!../../../../venv/bin/pytest

# I want to import ../config_and_configfile/example.py with `from sut import Car`.
def import_file(module_name: str, file_path: str) -> None:
	# https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
	import sys, importlib
	spec = importlib.util.spec_from_file_location(module_name, file_path)
	assert spec is not None
	assert spec.loader is not None
	module = importlib.util.module_from_spec(spec)
	sys.modules[module_name] = module
	spec.loader.exec_module(module)
import os
sut_fn = os.path.join(os.path.dirname(__file__), '..', 'config_and_configfile', 'example.py')
import_file('sut', sut_fn)


# ------- start -------
from sut import Car
import pytest

def test_car_accelerate(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(Car.speed_limit, 'value', 10)

	c1 = Car()
	c1.accelerate(5)
	c1.accelerate(5)
	with pytest.raises(ValueError):
		c1.accelerate(5)

	assert c1.speed == 10
