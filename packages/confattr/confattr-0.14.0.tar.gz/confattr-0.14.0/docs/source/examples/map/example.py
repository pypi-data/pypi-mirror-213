#!../../../../venv/bin/python3

import os
from confattr import ConfigFile
ConfigFile.config_directory = os.path.dirname(__file__)

# ------- start -------
import argparse
from collections.abc import Sequence
import urwid
from confattr import ConfigFileArgparseCommand, ConfigFile, Config, NotificationLevel, Message


class Map(ConfigFileArgparseCommand):

	'''
	bind a command to a key
	'''

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument('key', help='http://urwid.org/manual/userinput.html#keyboard-input')
		parser.add_argument('cmd', help='any urwid command')

	def run_parsed(self, args: argparse.Namespace) -> None:
		urwid.command_map[args.key] = args.cmd
		self.ui_notifier.show_info(f'map {args.key} {args.cmd!r}')


if __name__ == '__main__':
	# config
	choices = Config('choices', ['vanilla', 'strawberry'])
	urwid.command_map['enter'] = 'confirm'
	config_file = ConfigFile(appname='map-exp', notification_level=Config('notification-level', NotificationLevel.ERROR))
	config_file.load()

	# show errors in config
	palette = [(NotificationLevel.ERROR.value, 'dark red', 'default')]
	status_bar = urwid.Pile([])
	def on_config_message(msg: Message) -> None:
		markup = (msg.notification_level.value, str(msg))
		widget_options_tuple = (urwid.Text(markup), status_bar.options('pack'))
		status_bar.contents.append(widget_options_tuple)
		if 'frame' in globals():
			frame._invalidate()
	config_file.set_ui_callback(on_config_message)

	def input_filter(keys: 'list[str]', raw: 'list[int]') -> 'list[str]':
		status_bar.contents.clear()
		Message.reset()
		return keys

	# a simple example app showing check boxes and printing the user's choice to stdout
	def key_handler(key: str) -> bool:
		cmd = urwid.command_map[key]
		if cmd == 'confirm':
			raise urwid.ExitMainLoop()
		on_config_message(Message(NotificationLevel.ERROR, f'key {key!r} is not mapped'))
		return True
	checkboxes = [urwid.CheckBox(choice) for choice in choices.value]
	frame = urwid.Frame(urwid.Filler(urwid.Pile(checkboxes)), footer=status_bar)
	urwid.MainLoop(frame, palette=palette, input_filter=input_filter, unhandled_input=key_handler).run()

	for ckb in checkboxes:
		print(f'{ckb.label}: {ckb.state}')
