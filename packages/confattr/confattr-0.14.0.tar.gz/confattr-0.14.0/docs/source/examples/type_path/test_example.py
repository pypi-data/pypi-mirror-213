#!../../../../venv/bin/pytest

import os
import io

import pytest

def raise_error(msg: object) -> None:
	raise AssertionError(msg)


def test_definition() -> None:
	from .example import Path
	from confattr import Config, ConfigFile

	path = Config('path', Path(r'~/.config'))
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(raise_error)
	cf.save(comments=False)
	assert path.value.expand() == os.path.join(os.path.expanduser('~'), '.config')
	assert repr(path.value) == "Path('~/.config')"

	cf.parse_line('set path=/tmp/foo')
	assert path.value.expand() == '/tmp/foo'
	assert repr(path.value) == "Path('/tmp/foo')"

	cf.load()
	assert path.value.expand() == os.path.join(os.path.expanduser('~'), '.config')
	assert repr(path.value) == "Path('~/.config')"
