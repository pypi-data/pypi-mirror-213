#!../../../../venv/bin/pytest

import os
import sys
import subprocess

def test__output() -> None:
	path = os.path.dirname(__file__)
	fn_script = os.path.join(path, 'example.py')
	p = subprocess.run([sys.executable, '-m', 'pytest', fn_script], check=True)
