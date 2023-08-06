#!../../../../venv/bin/pytest

import os
from collections.abc import Callable

import pytest
import urwid

from utils import run_and_get_stdout


@pytest.fixture(autouse=True)
def reset(monkeypatch: pytest.MonkeyPatch) -> None:
	# patching the command_map attribute of the urwid module does not work
	# because then the widget is using a different command_map
	monkeypatch.setattr(urwid.command_map, '_command', urwid.command_map._command.copy())


def test__output(monkeypatch: pytest.MonkeyPatch) -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example_print_help.py')
	fn_expected_output = os.path.join(path, 'output_help.txt')
	monkeypatch.setenv('MAP_EXP_CONFIG_DIRECTORY', path)
	stdout = run_and_get_stdout(fn_script)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert stdout == expected_output


def test_run_example(monkeypatch: pytest.MonkeyPatch) -> None:
	class MockLoop:

		size = (30, 5)

		expected_widget_default = [
			b"                              ",
			b"[ ] vanilla                   ",
			b"[ ] strawberry                ",
			b"                              ",
			b"                              ",
		]

		expected_widget_invalid_key_g = [
			b"                              ",
			b"[ ] vanilla                   ",
			b"[ ] strawberry                ",
			b"                              ",
			b"key 'g' is not mapped         ",
		]

		def __init__(self,
			widget: urwid.Widget, *,
			palette: object,
			input_filter: 'Callable[[list[str], list[int]], list[str]]',
			unhandled_input: 'Callable[[str], bool]',
		) -> None:
			self.widget = widget
			self.palette = palette
			self.input_filter = input_filter
			self.unhandled_input = unhandled_input

		def run(self) -> None:
			assert self.widget.render(self.size).text == self.expected_widget_default
			assert self.simulate_key_press('g')
			assert self.widget.render(self.size).text == self.expected_widget_invalid_key_g
			assert self.simulate_key_press('j')
			assert self.simulate_key_press(' ')
			with pytest.raises(urwid.ExitMainLoop):
				self.simulate_key_press('q')

		def simulate_key_press(self, key: str) -> bool:
			keys = self.input_filter([key], [-1])
			assert len(keys) == 1
			key = keys[0]
			k = self.widget.keypress(self.size, key)
			if k:
				return self.unhandled_input(key)
			return True

	#monkeypatch.setenv('MAP_EXP_CONFIG_DIRECTORY', os.path.dirname(__file__))
	monkeypatch.setattr(urwid, 'MainLoop', MockLoop)
	stdout = run_and_get_stdout('example.py', nextto=__file__)
	assert stdout == '''\
vanilla: False
strawberry: True
'''
