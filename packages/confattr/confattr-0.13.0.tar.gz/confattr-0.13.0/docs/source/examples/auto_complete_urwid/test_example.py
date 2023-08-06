#!../../../../venv/bin/pytest -vv

import re
from collections.abc import Callable

import pytest
import urwid

from confattr import ConfigFile
from utils import run


class AbstractMockLoop:

	size: 'tuple[int, int]'

	def __init__(self,
		widget: urwid.Widget, *,
		palette: object,
		input_filter: 'Callable[[list[str], list[int]], list[str]]|None' = None,
		unhandled_input: 'Callable[[str], bool]',
		handle_mouse: bool,
	) -> None:
		if input_filter is None:
			input_filter = lambda keys, raws: keys
		self.widget = widget
		self.palette = palette
		self.input_filter = input_filter
		self.unhandled_input = unhandled_input

	def run(self) -> None:
		raise NotImplementedError()

	def simulate_key_press(self, key: str) -> bool:
		'''
		The urwid documentation says "The unhandled_input function should return True if it handled the input." [description of MainLoop.unhandled_input]
		But the return value is not checked and none of the official examples returns something from unhandled_input.
		Therefore I am not returning anything from the unhandled_input function either, making the return value of this method mean:
		True if it has been handled by widget, None if it has been passed to unhandled_input.
		'''
		keys = self.input_filter([key], [-1])
		assert len(keys) == 1
		key = keys[0]
		k = self.widget.keypress(self.size, key)
		if k:
			return self.unhandled_input(key)
		return True

class Line:
	def __init__(self, pattern: bytes) -> None:
		self.reo = re.compile(pattern)
	def __eq__(self, other: object) -> bool:
		if isinstance(other, bytes):
			return bool(self.reo.match(other))
		return NotImplemented
	def __repr__(self) -> str:
		return '%s(%r)' % (type(self).__name__, self.reo.pattern)


def test_complete_cycle(monkeypatch: pytest.MonkeyPatch) -> None:
	cf = ConfigFile(appname='test')
	command_names = list(cf.command_dict.keys())
	command_names.append('quit')
	class MockLoop(AbstractMockLoop):

		size = (61, 5)

		expected_widget_empty = [
			"                                                             ".encode(),
			"┌───────────────────────────────────────────────────────────┐".encode(),
			"│>>>                                                        │".encode(),
			"└───────────────────────────────────────────────────────────┘".encode(),
			"                                                             ".encode(),
		]

		expected_widget_complete_1 = [
			"                                                             ".encode(),
			"┌───────────────────────────────────────────────────────────┐".encode(),
			"│>>> set                                                    │".encode(),
			"└───────────────────────────────────────────────────────────┘".encode(),
			"                                                             ".encode(),
		]

		expected_widget_complete_2 = [
			"                                                             ".encode(),
			"┌───────────────────────────────────────────────────────────┐".encode(),
			"│>>> include                                                │".encode(),
			"└───────────────────────────────────────────────────────────┘".encode(),
			"                                                             ".encode(),
		]

		expected_widget = '\n'.join([
			"                                                             ",
			"┌───────────────────────────────────────────────────────────┐",
			"│>>> {:<54} │",
			"└───────────────────────────────────────────────────────────┘",
			"                                                             ",
		])

		def run(self) -> None:
			assert self.widget.render(self.size).text == self.expected_widget_empty

			for cmd in command_names:
				assert self.simulate_key_press('tab')
				assert b'\n'.join(self.widget.render(self.size).text).decode() == self.expected_widget.format(cmd)
			assert self.simulate_key_press('tab')
			assert self.widget.render(self.size).text == self.expected_widget_empty

			for cmd in command_names[:2]:
				assert self.simulate_key_press('tab')
				assert b'\n'.join(self.widget.render(self.size).text).decode() == self.expected_widget.format(cmd)
			assert self.simulate_key_press('shift tab')
			assert b'\n'.join(self.widget.render(self.size).text).decode() == self.expected_widget.format(command_names[0])
			assert self.simulate_key_press('shift tab')
			assert self.widget.render(self.size).text == self.expected_widget_empty

			assert self.simulate_key_press('shift tab')
			assert b'\n'.join(self.widget.render(self.size).text).decode() == self.expected_widget.format(command_names[-1])

	monkeypatch.setattr(urwid, 'MainLoop', MockLoop)
	run('example.py', nextto=__file__)


def test_quit(monkeypatch: pytest.MonkeyPatch) -> None:
	class MockLoop(AbstractMockLoop):

		size = (61, 5)

		def run(self) -> None:
			for c in 'quit':
				self.simulate_key_press(c)

			with pytest.raises(urwid.ExitMainLoop):
				self.simulate_key_press('enter')

	monkeypatch.setattr(urwid, 'MainLoop', MockLoop)
	run('example.py', nextto=__file__)


def test_ctrl_k_and_ctrl_u(monkeypatch: pytest.MonkeyPatch) -> None:
	class MockLoop(AbstractMockLoop):

		size = (61, 5)

		expected_widget_empty = [
			"                                                             ".encode(),
			"┌───────────────────────────────────────────────────────────┐".encode(),
			"│>>>                                                        │".encode(),
			"└───────────────────────────────────────────────────────────┘".encode(),
			"                                                             ".encode(),
		]

		expected_widget_after_input = [
			"                                                             ".encode(),
			"┌───────────────────────────────────────────────────────────┐".encode(),
			"│>>> abcdef                                                 │".encode(),
			"└───────────────────────────────────────────────────────────┘".encode(),
			"                                                             ".encode(),
		]

		expected_widget_after_ctrl_k = [
			"                                                             ".encode(),
			"┌───────────────────────────────────────────────────────────┐".encode(),
			"│>>> abc                                                    │".encode(),
			"└───────────────────────────────────────────────────────────┘".encode(),
			"                                                             ".encode(),
		]

		expected_widget_after_ctrl_u = [
			"                                                             ".encode(),
			"┌───────────────────────────────────────────────────────────┐".encode(),
			"│>>> c                                                      │".encode(),
			"└───────────────────────────────────────────────────────────┘".encode(),
			"                                                             ".encode(),
		]

		def run(self) -> None:
			assert self.widget.render(self.size).text == self.expected_widget_empty
			for c in 'abcdef':
				assert self.simulate_key_press(c)
			for i in range(3):
				assert self.simulate_key_press('left')
			assert self.widget.render(self.size).text == self.expected_widget_after_input
			assert self.simulate_key_press('ctrl k')
			assert self.widget.render(self.size).text == self.expected_widget_after_ctrl_k
			assert self.simulate_key_press('left')
			assert self.simulate_key_press('ctrl u')
			assert self.widget.render(self.size).text == self.expected_widget_after_ctrl_u

	monkeypatch.setattr(urwid, 'MainLoop', MockLoop)
	run('example.py', nextto=__file__)


def test_invalid_input(monkeypatch: pytest.MonkeyPatch) -> None:
	class MockLoop(AbstractMockLoop):

		size = (61, 5)

		expected_widget_empty = [
			"                                                             ".encode(),
			"┌───────────────────────────────────────────────────────────┐".encode(),
			"│>>>                                                        │".encode(),
			"└───────────────────────────────────────────────────────────┘".encode(),
			"                                                             ".encode(),
		]

		expected_widget_after_input = [
			"                                                             ".encode(),
			"┌───────────────────────────────────────────────────────────┐".encode(),
			"│>>> abc                                                    │".encode(),
			"└───────────────────────────────────────────────────────────┘".encode(),
			"                                                             ".encode(),
		]

		expected_widget_after_enter = [
			"┌───────────────────────────────────────────────────────────┐".encode(),
			"│>>> abc                                                    │".encode(),
			"└───────────────────────────────────────────────────────────┘".encode(),
			"                                                             ".encode(),
			"unknown command 'abc'                                        ".encode(),
		]

		def run(self) -> None:
			assert self.widget.render(self.size).text == self.expected_widget_empty
			for c in 'abc':
				assert self.simulate_key_press(c)
			assert self.widget.render(self.size).text == self.expected_widget_after_input
			self.simulate_key_press('enter')
			assert self.widget.render(self.size).text == self.expected_widget_after_enter

	monkeypatch.setattr(urwid, 'MainLoop', MockLoop)
	run('example.py', nextto=__file__)


def test_valid_input(monkeypatch: pytest.MonkeyPatch) -> None:
	class MockLoop(AbstractMockLoop):

		size = (61, 5)

		expected_widget_empty = [
			"                                                             ".encode(),
			"┌───────────────────────────────────────────────────────────┐".encode(),
			"│>>>                                                        │".encode(),
			"└───────────────────────────────────────────────────────────┘".encode(),
			"                                                             ".encode(),
		]

		expected_widget_completed_command = [
			"                                                             ".encode(),
			"┌───────────────────────────────────────────────────────────┐".encode(),
			"│>>> set                                                    │".encode(),
			"└───────────────────────────────────────────────────────────┘".encode(),
			"                                                             ".encode(),
		]

		expected_widget_completed_key = [
			"                                                             ".encode(),
			"┌───────────────────────────────────────────────────────────┐".encode(),
			"│>>> set notification-level.cli                             │".encode(),
			"└───────────────────────────────────────────────────────────┘".encode(),
			"                                                             ".encode(),
		]

		expected_widget_completed_value = [
			"                                                             ".encode(),
			"┌───────────────────────────────────────────────────────────┐".encode(),
			"│>>> set notification-level.cli=error                       │".encode(),
			"└───────────────────────────────────────────────────────────┘".encode(),
			"                                                             ".encode(),
		]

		def run(self) -> None:
			assert self.widget.render(self.size).text == self.expected_widget_empty
			self.simulate_key_press('s')
			self.simulate_key_press('tab')
			self.simulate_key_press(' ')
			assert self.widget.render(self.size).text == self.expected_widget_completed_command
			self.simulate_key_press('n')
			self.simulate_key_press('tab')
			self.simulate_key_press('tab')
			assert self.widget.render(self.size).text == self.expected_widget_completed_key
			self.simulate_key_press('=')
			self.simulate_key_press('e')
			self.simulate_key_press('tab')
			assert self.widget.render(self.size).text == self.expected_widget_completed_value
			self.simulate_key_press('enter')
			assert self.widget.render(self.size).text == self.expected_widget_empty

	monkeypatch.setattr(urwid, 'MainLoop', MockLoop)
	run('example.py', nextto=__file__)
