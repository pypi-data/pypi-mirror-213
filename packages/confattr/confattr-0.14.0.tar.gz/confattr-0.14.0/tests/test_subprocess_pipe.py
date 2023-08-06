#!../venv/bin/pytest -s

from confattr.subprocess_pipe import split_list, run_and_pipe

def test__split_list__str() -> None:
	assert split_list(['diff', '--color=always', '|', 'less', '-R'], '|') == [['diff', '--color=always'], ['less', '-R']]

def test__split_list__int() -> None:
	assert split_list([0, 1, 0, 2, 3, 0, 4], 0) == [[], [1], [2, 3], [4]]


def test__run_and_pipe__1() -> None:
	assert run_and_pipe(['echo', 'abc'], get_output=True).stdout.decode() == 'abc\n'

def test__run_and_pipe__2() -> None:
	assert run_and_pipe(['echo', 'ice', '|', 'sed', 's/i/a/'], get_output=True).stdout.decode() == 'ace\n'

def test__run_and_pipe__3() -> None:
	assert run_and_pipe(['echo', 'ice', '|', 'sed', 's/i/a/', '|', 'sed', 's/$/s/'], get_output=True).stdout.decode() == 'aces\n'

def test__run_and_pipe__4() -> None:
	assert run_and_pipe(['echo', 'ice', '|', 'sed', 's/i/a/', '|', 'sed', 's/$/s/', '|', 'sed', 's/^/tr/'], get_output=True).stdout.decode() == 'traces\n'




def test__run_and_pipe__no_output__success() -> None:
	assert run_and_pipe(['echo', 'apple\norange\nbanana', '|', 'grep', 'orange']).returncode == 0

def test__run_and_pipe__no_output__fail() -> None:
	assert run_and_pipe(['echo', 'apple\norange\nbanana', '|', 'grep', 'melon']).returncode != 0
