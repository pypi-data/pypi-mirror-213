#!./runmodule.sh

import subprocess
import typing
from collections.abc import Sequence, Mapping

PIPE = '|'

T = typing.TypeVar('T')
CompletedProcess = subprocess.CompletedProcess

def run_and_pipe(cmds: 'Sequence[str]', *, get_output: bool = False, env: 'Mapping[str, str]|None' = None) -> 'subprocess.CompletedProcess[bytes]':
	'''
	Run an external program and return when the program is finished.

	:param cmds: One or several commands to be executed. If several commands are passed they are seperated by a '|' and stdout of the former command is piped to stdin of the following command.
	:param env: The environment variables to be passed to the subprocess. If env is None :py:data:`os.environ` is used.
	:param get_output: Make stdout and stderr available in the returned completed process object.
	:return: The completed process
	:raises OSError: e.g. if the program was not found
	:raises CalledProcessError: if the called program failed

	https://docs.python.org/3/library/subprocess.html#exceptions
	'''
	# I am not using shell=True because that is platform dependend
	# and shlex is for UNIX like shells only, so it may not work on Windows
	if get_output:
		def run(cmd: 'Sequence[str]', input: 'bytes|None' = None) -> 'subprocess.CompletedProcess[bytes]':
			return subprocess.run(cmd, env=env, input=input, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	else:
		def run(cmd: 'Sequence[str]', input: 'bytes|None' = None) -> 'subprocess.CompletedProcess[bytes]':
			return subprocess.run(cmd, env=env, input=input)

	cmd_list = split_list(cmds, PIPE)
	n = len(cmd_list)
	if n == 1:
		return run(cmd_list[0])

	p = subprocess.run(cmd_list[0], env=env, stdout=subprocess.PIPE)
	for cmd in cmd_list[1:-1]:
		p = subprocess.run(cmd, env=env, input=p.stdout, stdout=subprocess.PIPE)
	return run(cmd_list[-1], input=p.stdout)

def split_list(l: 'Sequence[T]', sep: T) -> 'Sequence[Sequence[T]]':
	'''
	Like str.split but for lists/tuples.
	Splits a sequence into several sequences.
	'''
	out: 'list[Sequence[T]]' = []
	i0 = 0
	while True:
		try:
			i1 = l.index(sep, i0)
		except ValueError:
			break
		out.append(l[i0:i1])
		i0 = i1 + 1
	out.append(l[i0:])
	return out
