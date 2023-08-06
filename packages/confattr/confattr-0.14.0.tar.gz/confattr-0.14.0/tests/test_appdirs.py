#!../venv/bin/pytest -s

import os
import platform
import pathlib

import pytest

from confattr import ConfigFile, Config


class ParseError(ValueError):
	pass

def ui_callback(msg: object) -> None:
	raise ParseError(str(msg))


def test_using_correct_appdirs_library() -> None:
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)

	ENV = os.environ['TOX_ENV_NAME']
	if ENV == 'platformdirs':
		from platformdirs import PlatformDirs as AppDirs   # type: ignore [import]
		assert isinstance(cf.get_app_dirs(), AppDirs)
	elif ENV == 'xdgappdirs':
		from xdgappdirs import AppDirs   # type: ignore [import]
		assert isinstance(cf.get_app_dirs(), AppDirs)
	else:
		from appdirs import AppDirs
		assert isinstance(cf.get_app_dirs(), AppDirs)


@pytest.mark.skipif(platform.system() != 'Linux', reason='This directory structure applies to Linux only')
def test__config_location_linux(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(ConfigFile, 'config_directory', None)
	monkeypatch.delenv('XDG_CONFIG_HOME', raising=False)
	monkeypatch.delenv('TEST_CONFIG_PATH', raising=False)
	monkeypatch.delenv('TEST_CONFIG_DIRECTORY', raising=False)
	monkeypatch.delenv('TEST_CONFIG_NAME', raising=False)

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	assert list(cf.iter_config_paths())[0] == os.path.expanduser('~/.config/test/config')


@pytest.mark.skipif(platform.system() != 'Linux', reason='XDG_CONFIG_HOME environment variable applies on Linux only')
def test__save_and_load__xdg_config_home(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(ConfigFile, 'config_directory', None)
	monkeypatch.setenv('XDG_CONFIG_HOME', str(tmp_path))
	fn = tmp_path / 'test' / 'config'
	assert not os.path.exists(fn)

	c = Config('greeting', 'hello world')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	config_file.save()
	assert os.path.exists(fn)
	assert c.value == 'hello world'

	c.value = 'hi there'
	assert c.value == 'hi there'

	config_file.load()
	assert c.value == 'hello world'
