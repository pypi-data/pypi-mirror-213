#!../../../../venv/bin/pytest

import sys
import io
import re
import pathlib

import pytest

from utils import run_and_get_stdout

@pytest.mark.skipif(sys.version_info < (3,7), reason='prompt_toolkit requires python 3.7 or higher')
def test__echo(monkeypatch: pytest.MonkeyPatch) -> None:
	from prompt_toolkit.application import create_app_session
	from prompt_toolkit.input import create_pipe_input
	from prompt_toolkit.output import DummyOutput
	from prompt_toolkit.formatted_text import FormattedText
	calls: 'list[str|FormattedText]' = []
	monkeypatch.setattr('prompt_toolkit.print_formatted_text', calls.append)
	with create_pipe_input() as inp:
		with create_app_session(input=inp, output=DummyOutput()):
			inp.send_text('echo hello world\n')
			inp.close()
			run_and_get_stdout('example.py', nextto=__file__)

	assert calls == ['hello world']

@pytest.mark.skipif(sys.version_info < (3,7), reason='prompt_toolkit requires python 3.7 or higher')
def test__include_and_quit(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
	from prompt_toolkit.application import create_app_session
	from prompt_toolkit.input import create_pipe_input
	from prompt_toolkit.output import DummyOutput
	from prompt_toolkit.formatted_text import FormattedText
	calls: 'list[str|FormattedText]' = []
	monkeypatch.setattr('prompt_toolkit.print_formatted_text', calls.append)
	monkeypatch.setenv('AUTO_COMPLETION_EXAMPLE_CONFIG_DIRECTORY', str(tmp_path))
	with open(str(tmp_path / 'test'), 'wt') as f:
		f.write('set unknown=42')
	with create_pipe_input() as inp:
		with create_app_session(input=inp, output=DummyOutput()):
			inp.send_text('include test\n')
			inp.send_text('quit\n')
			run_and_get_stdout('example.py', nextto=__file__)

	assert len(calls) == 1
	formatted_text = calls[0]
	assert isinstance(formatted_text, FormattedText)
	assert len(formatted_text) == 1
	assert formatted_text[0][0] == 'ansired'
	assert re.match("While loading [^\n]+\ninvalid key 'unknown' in line 1 'set unknown=42'", formatted_text[0][1])
