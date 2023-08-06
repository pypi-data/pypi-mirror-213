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
sut_fn = os.path.join(os.path.dirname(__file__), '..', 'multiconfig', 'example.py')
import_file('sut', sut_fn)


# ------- start -------
from sut import Car, Color
from confattr import ConfigId
import pytest

def test_car_color(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(Car.color, 'value', Color.WHITE)
	monkeypatch.setitem(Car.color.values, ConfigId('alices-car'), Color.BLUE)
	monkeypatch.setitem(Car.color.values, ConfigId('bobs-car'), Color.GREEN)

	alices_car = Car(ConfigId('alices-car'))
	bobs_car = Car(ConfigId('bobs-car'))
	another_car = Car(ConfigId('another-car'))

	assert alices_car.color is Color.BLUE
	assert bobs_car.color is Color.GREEN
	assert another_car.color is Color.WHITE
