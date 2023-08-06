#!../../../../venv/bin/python3
import os
from confattr import ConfigFile
ConfigFile.config_directory = os.path.dirname(__file__)

# ------- start -------
import argparse
import typing
if typing.TYPE_CHECKING:
	from typing_extensions import Unpack  # This will hopefully be replaced by the ** syntax proposed in https://peps.python.org/pep-0692/
	from confattr import SaveKwargs

import urwid
from confattr import ConfigFileArgparseCommand, FormattedWriter, ConfigFile, SectionLevel


class Map(ConfigFileArgparseCommand):

	'''
	bind a command to a key
	'''

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument('key', help='http://urwid.org/manual/userinput.html#keyboard-input')
		parser.add_argument('cmd', help='any urwid command')

	def run_parsed(self, args: argparse.Namespace) -> None:
		urwid.command_map[args.key] = args.cmd

	def save(self, writer: FormattedWriter, **kw: 'Unpack[SaveKwargs]') -> None:
		if self.should_write_heading:
			writer.write_heading(SectionLevel.SECTION, 'Key bindings')

		for key, cmd in sorted(urwid.command_map._command.items(), key=lambda key_cmd: str(key_cmd[1])):
			quoted_key = self.config_file.quote(key)
			quoted_cmd = self.config_file.quote(cmd)
			writer.write_command(f'map {quoted_key} {quoted_cmd}')


if __name__ == '__main__':
	ConfigFile(appname='example').save()
