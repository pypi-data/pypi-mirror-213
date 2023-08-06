#!venv/bin/pytest

from confattr import ConfigFile, Config, MultiConfig, ConfigFileCommand, Message

import pytest
import pathlib

@pytest.fixture(autouse=True)
def reset_config_path(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
	assert ConfigFile.config_path is None
	assert ConfigFile.config_directory is None
	monkeypatch.setattr(ConfigFile, 'config_directory', str(tmp_path))
	monkeypatch.setattr(ConfigFileCommand, '_subclasses', ConfigFileCommand._subclasses.copy())
	monkeypatch.setattr(ConfigFileCommand, '_used_names', ConfigFileCommand._used_names.copy())
	Config.instances.clear()
	MultiConfig.reset()
	Message.reset()
