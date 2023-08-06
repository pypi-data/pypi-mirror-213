#!../../../../venv/bin/pytest

import os
import shutil
import platform
import subprocess

import pytest
from confattr import ConfigFile

from utils import run


class RunMock:

	def __init__(self) -> None:
		self.calls: 'list[list[str]]' = []

	def __call__(self, cmd: 'list[str]', **kw: object) -> None:
		self.calls.append(cmd)


def test__output(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(platform, 'system', lambda: 'Linux')
	monkeypatch.setitem(os.environ, 'EDITOR', 'myeditor')
	monkeypatch.setattr(shutil, 'which', lambda cmd: True)

	run_mock = RunMock()
	monkeypatch.setattr(subprocess, 'run', run_mock)

	cf = ConfigFile(appname='example-app')
	cf.save()

	run('example.py', nextto=__file__)

	assert len(run_mock.calls) == 1
	assert run_mock.calls[0] == ['myeditor', cf.get_save_path()]
