#!../../../../venv/bin/pytest

import os
import sys
import pathlib
import subprocess


def test_error_and_saved_config(tmp_path: pathlib.Path) -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example.py')
	fn_saved_config = str(tmp_path / 'config')
	fn_expected_config = os.path.join(path, 'expected-config')
	env = {'EXAMPLE_CONFIG_PATH' : fn_saved_config}
	p = subprocess.run([sys.executable, fn_script], env=env, stderr=subprocess.PIPE, check=False)

	with open(fn_expected_config, 'rt') as f_expected_config:
		with open(fn_saved_config, 'rt') as f_saved_config:
			assert f_saved_config.read() == f_expected_config.read()

	stderr = p.stderr.decode().splitlines()
	assert stderr[-1] == 'AssertionError'

	i = -2
	if '^^^^^^^^^^^^^^^^^^^^^^^^' in stderr[i]:  # since python 3.11 the error is underlined
		i += -1
	assert stderr[i].endswith('# This fails!')
