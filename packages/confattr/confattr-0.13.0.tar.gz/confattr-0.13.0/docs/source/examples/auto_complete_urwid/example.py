#!../../../../venv/bin/python3

# ------- start -------
from confattr import Config, ConfigFile, Message, NotificationLevel, ConfigFileArgparseCommand
import argparse
import urwid
urwid.command_map['esc'] = 'quit'
urwid.command_map['tab'] = 'complete cycle forward'
urwid.command_map['shift tab'] = 'complete cycle backward'
urwid.command_map['ctrl u'] = 'clear before'
urwid.command_map['ctrl k'] = 'clear after'

APPNAME = 'auto-completion-example'

class EditWithAutoComplete(urwid.Edit):  # type: ignore [misc]  # Class cannot subclass "Edit" (has type "Any")

	def __init__(self, caption: str, edit_text: str, *, config_file: ConfigFile) -> None:
		super().__init__(caption, edit_text)
		self.config_file = config_file
		self.completions: 'list[str]|None' = None
		self.completion_index = -1

	def keypress(self, size: 'tuple[int]', key: str) -> 'str|None':
		if not super().keypress(size, key):
			self.on_change()
			return None
		cmd = self._command_map[key]
		if cmd == 'complete cycle forward':
			self.complete_cycle(+1)
		elif cmd == 'complete cycle backward':
			self.complete_cycle(-1)
		elif cmd == 'clear before':
			self.set_edit_text(self.edit_text[self.edit_pos:])
			self.set_edit_pos(0)
		elif cmd == 'clear after':
			self.set_edit_text(self.edit_text[:self.edit_pos])
			self.set_edit_pos(len(self.edit_text))
		else:
			return key

		return None

	def on_change(self) -> None:
		self.completions = None
		self.completion_index = -1

	def complete_cycle(self, direction: int) -> None:
		if self.completions is None:
			self.default_line = self.edit_text
			self.default_pos = self.edit_pos
			self.start_of_line, self.completions, self.end_of_line = self.config_file.get_completions(self.edit_text, self.edit_pos)
		self.completion_index += direction
		if self.completion_index < -1:
			self.completion_index = len(self.completions) - 1
		elif self.completion_index >= len(self.completions):
			self.completion_index = -1
		if self.completion_index == -1:
			self.set_edit_text(self.default_line)
			self.set_edit_pos(self.default_pos)
		else:
			completed = self.start_of_line + self.completions[self.completion_index]
			self.set_edit_text(completed + self.end_of_line)
			self.set_edit_pos(len(completed))

class Quit(ConfigFileArgparseCommand):

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		pass

	def run_parsed(self, args: argparse.Namespace) -> None:
		raise urwid.ExitMainLoop()


def main() -> None:
	# creating 2 ConfigFile instances with different notification level filters
	config_file = ConfigFile(appname=APPNAME, notification_level=Config('notification-level.config-file', NotificationLevel.ERROR))
	cli = ConfigFile(appname=APPNAME, notification_level=Config('notification-level.cli', NotificationLevel.INFO), show_line_always=False)
	cli.command_dict['include'].config_file = config_file
	config_file.load()

	# show errors in config
	palette = [(NotificationLevel.ERROR.value, 'dark red', 'default')]
	status_bar = urwid.Pile([])
	def on_config_message(msg: Message) -> None:
		markup = (msg.notification_level.value, str(msg))
		widget_options_tuple = (urwid.Text(markup), status_bar.options('pack'))
		status_bar.contents.append(widget_options_tuple)
		frame_widget._invalidate()

	# main user interface
	def keypress(key: str) -> None:
		cmd = urwid.command_map[key]
		if cmd == 'activate':
			Message.reset()
			status_bar.contents.clear()
			if cli.parse_line(edit.edit_text):
				edit.set_edit_text('')
	edit = EditWithAutoComplete('>>> ', '', config_file=cli)
	main_widget = urwid.Filler(urwid.LineBox(edit))
	frame_widget = urwid.Frame(main_widget, footer=status_bar)

	config_file.set_ui_callback(on_config_message)
	cli.set_ui_callback(on_config_message)
	urwid.MainLoop(frame_widget, unhandled_input=keypress, palette=palette, handle_mouse=False).run()

if __name__ == '__main__':
	main()
