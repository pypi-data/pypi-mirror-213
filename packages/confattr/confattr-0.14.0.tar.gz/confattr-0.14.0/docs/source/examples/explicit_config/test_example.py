#!../../../../venv/bin/pytest

import pytest

from confattr import ConfigFile
from utils import run_and_get_stdout

def test_load_without_config() -> None:
	with pytest.raises(TypeError, match="value for 'bus.bitrate' has not been set"):
		run_and_get_stdout('example.py', nextto=__file__)

def test_load_with_config() -> None:
	cf = ConfigFile(appname='test')
	fn = cf.get_save_path()
	with open(fn, 'wt') as f:
		f.write("set bus.bitrate = 9600")
	stdout = run_and_get_stdout('example.py', nextto=__file__)
	assert stdout.rstrip() == "bitrate: 9600"
