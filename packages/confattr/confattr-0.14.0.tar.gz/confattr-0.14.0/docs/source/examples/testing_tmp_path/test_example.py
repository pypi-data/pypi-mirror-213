#!../../../../venv/bin/pytest

from .example import reset_config
from confattr import ConfigFile

import pytest
import pathlib


def test_fixture() -> None:
	# I cannot call the fixture directly.
	# Instead, in order to check that the fixture is applied implicitly
	# I check for a str which is documented to be contained in the tmp_path.
	# https://docs.pytest.org/en/stable/how-to/tmp_path.html#base-temporary-directory
	# https://docs.pytest.org/en/stable/deprecations.html#calling-fixtures-directly
	assert ConfigFile.config_directory is not None
	assert 'pytest-' in ConfigFile.config_directory
