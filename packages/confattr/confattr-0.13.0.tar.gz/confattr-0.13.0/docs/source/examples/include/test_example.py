#!../../../../venv/bin/pytest -s -vv

import os
import re
import pathlib
from collections.abc import Callable

import pytest
import urwid

from confattr import ConfigFile
from utils import run


@pytest.fixture(autouse=True)
def reset(monkeypatch: pytest.MonkeyPatch) -> None:
	# patching the command_map attribute of the urwid module does not work
	# because then the widget is using a different command_map
	monkeypatch.setattr(urwid.command_map, '_command', urwid.command_map._command.copy())



def test__output(monkeypatch: 'pytest.MonkeyPatch') -> None:
	monkeypatch.setattr(urwid, 'command_map', urwid.command_map.copy())

	from .example import App

	path = os.path.dirname(__file__)
	monkeypatch.setattr(ConfigFile, 'config_directory', path)
	fn = os.path.join(path, 'output.txt')
	app = App()
	with open(fn, 'rb') as f:
		expected = f.read().splitlines()
		assert app.frame.render((51,5)).text == expected



def test_run_example_with_invalid_config(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
	fn = str(tmp_path / 'config')
	monkeypatch.setenv('EXAMPLE_INCLUDE_CONFIG_PATH', fn)
	with open(fn, 'wt') as f:
		f.write('''\
		set undefined=123

		[documents]
		set path.src = ~/documents
		set path.dst = /media/usb1/documents
		set direction = src-to-dst

		[music]
		set path.src = ~/music
		set path.dst = /media/usb1/music
		set direction = src-to-dst

		[pictures]
		set path.src = ~/pictures
		set path.dst = /media/usb1/pictures
		set direction = two-way
		''')

	class Line:
		def __init__(self, pattern: bytes) -> None:
			self.reo = re.compile(pattern)
		def __eq__(self, other: object) -> bool:
			if isinstance(other, bytes):
				return bool(self.reo.match(other))
			return NotImplemented
		def __repr__(self) -> str:
			return '%s(%r)' % (type(self).__name__, self.reo.pattern)

	class MockLoop:

		size = (61, 5)

		expected_widget_invalid_config = [
			b"~/documents                   >  /media/usb1/documents       ",
			b"~/music                       >  /media/usb1/music           ",
			Line(b'While loading'),
			Line(b'.*'),
			b"invalid key 'undefined' in line 1 'set undefined=123'        ",
		]

		expected_widget_invalid_key_g = [
			b"~/documents                   >  /media/usb1/documents       ",
			b"~/music                       >  /media/usb1/music           ",
			b"~/pictures                   <-> /media/usb1/pictures        ",
			b"                                                             ",
			b"undefined key: g                                             ",
		]

		expected_widget_toggled_music = [
			b"~/documents                   >  /media/usb1/documents       ",
			b"~/music                       <  /media/usb1/music           ",
			b"~/pictures                   <-> /media/usb1/pictures        ",
			b"                                                             ",
			b"                                                             ",
		]

		expected_widget_ignored_pictures = [
			b"~/documents                   >  /media/usb1/documents       ",
			b"~/music                       <  /media/usb1/music           ",
			b"~/pictures                    |  /media/usb1/pictures        ",
			b"                                                             ",
			b"                                                             ",
		]

		expected_widget_pictures_src_to_dst = [
			b"~/documents                   >  /media/usb1/documents       ",
			b"~/music                       <  /media/usb1/music           ",
			b"~/pictures                    >  /media/usb1/pictures        ",
			b"                                                             ",
			b"                                                             ",
		]

		def __init__(self,
			widget: urwid.Widget, *,
			palette: object,
			input_filter: 'Callable[[list[str], list[int]], list[str]]',
			unhandled_input: 'Callable[[str], bool]',
			handle_mouse: bool,
		) -> None:
			self.widget = widget
			self.palette = palette
			self.input_filter = input_filter
			self.unhandled_input = unhandled_input

		def run(self) -> None:
			assert self.widget.render(self.size).text == self.expected_widget_invalid_config
			assert self.simulate_key_press('g')
			assert self.widget.render(self.size).text == self.expected_widget_invalid_key_g
			assert self.simulate_key_press('down')
			assert self.simulate_key_press(' ')
			assert self.widget.render(self.size).text == self.expected_widget_toggled_music
			assert self.simulate_key_press('down')
			assert self.simulate_key_press('i')
			assert self.widget.render(self.size).text == self.expected_widget_ignored_pictures
			assert self.simulate_key_press(' ')
			assert self.widget.render(self.size).text == self.expected_widget_pictures_src_to_dst
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

	monkeypatch.setattr(urwid, 'MainLoop', MockLoop)
	run('example.py', nextto=__file__)
