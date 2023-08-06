#!../../../../venv/bin/pytest

import os
import sys
import subprocess

def test__output() -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example.sh')
	fn_expected_output = os.path.join(path, 'expected_output.txt')
	env = {'EXAMPLE_APP_CONFIG_DIRECTORY' : path}
	p = subprocess.run(['bash', fn_script, sys.executable], env=env, stdout=subprocess.PIPE, check=True)

	with open(fn_expected_output, 'rt') as f:
		expected_output = f.read()

	assert p.stdout.decode() == expected_output
