#!../../../../venv/bin/python3

if __name__ == '__main__':
	import os
	from confattr import ConfigFile
	ConfigFile.config_directory = os.path.dirname(__file__)

# ------- start -------
from confattr import Config, MultiConfig, ConfigId, ConfigFile, NotificationLevel, Message
import enum
import urwid

CMD_QUIT = 'quit'
CMD_TOGGLE = 'toggle'
CMD_IGNORE = 'ignore'

urwid.command_map['q'] = CMD_QUIT
urwid.command_map[' '] = CMD_TOGGLE
urwid.command_map['i'] = CMD_IGNORE


class Direction(enum.Enum):
	SRC_TO_DST = ' > '
	DST_TO_SRC = ' < '
	IGNORE = ' | '
	TWO_WAY = '<->'

class DirectoryPair:

	path_src = MultiConfig('path.src', '')
	path_dst = MultiConfig('path.dst', '')
	direction = MultiConfig('direction', Direction.SRC_TO_DST)

	def __init__(self, config_id: ConfigId) -> None:
		self.config_id = config_id

	def toggle_direction(self) -> None:
		if self.direction is Direction.SRC_TO_DST:
			self.direction = Direction.DST_TO_SRC
		else:
			self.direction = Direction.SRC_TO_DST

	def ignore(self) -> None:
		self.direction = Direction.IGNORE


class DirectoryPairWidget(urwid.WidgetWrap):  # type: ignore [misc]  # Class cannot subclass "WidgetWrap" (has type "Any") because urwid is not typed yet

	def __init__(self, dirs: DirectoryPair) -> None:
		self.model = dirs
		self.widget_src = urwid.Text(dirs.path_src)
		self.widget_dst = urwid.Text(dirs.path_dst)
		self.widget_direction = urwid.Text('')
		self.update_direction()
		widget = urwid.Columns([self.widget_src, (urwid.PACK, self.widget_direction), self.widget_dst])
		widget = urwid.AttrMap(widget, None, App.ATTR_FOCUS)
		super().__init__(widget)

	def selectable(self) -> bool:
		return True

	def keypress(self, size: 'tuple[int, ...]', key: str) -> 'str|None':
		if not super().keypress(size, key):
			return None  # pragma: no cover  # WidgetWrap does not consume any key presses

		cmd = self._command_map[key]
		if cmd == CMD_TOGGLE:
			self.model.toggle_direction()
			self.update_direction()
		elif cmd == CMD_IGNORE:
			self.model.ignore()
			self.update_direction()
		else:
			return key

		return None

	def update_direction(self) -> None:
		self.widget_direction.set_text(' %s ' % self.model.direction.value)


class App:

	ATTR_ERROR = NotificationLevel.ERROR.value
	ATTR_INFO = NotificationLevel.INFO.value
	ATTR_FOCUS = 'focus'

	PALETTE = (
		(ATTR_ERROR, 'dark red', 'default'),
		(ATTR_INFO, 'dark blue', 'default'),
		(ATTR_FOCUS, 'default', 'dark blue'),
	)

	notification_level = Config('notification-level', NotificationLevel.ERROR,
		help = {
			NotificationLevel.ERROR: 'show errors in the config file',
			NotificationLevel.INFO: 'additionally show all settings which are changed in the config file',
		}
	)

	def __init__(self) -> None:
		self.config_file = ConfigFile(appname='example-include', notification_level=type(self).notification_level)
		self.config_file.load()
		self.directory_pairs = [DirectoryPair(config_id) for config_id in MultiConfig.config_ids]

		self.body = urwid.ListBox([DirectoryPairWidget(dirs) for dirs in self.directory_pairs])
		self.status_bar = urwid.Pile([])
		self.frame = urwid.Frame(self.body, footer=self.status_bar)
		self.config_file.set_ui_callback(self.on_config_message)

	def run(self) -> None:
		urwid.MainLoop(self.frame, palette=self.PALETTE, input_filter=self.input_filter, unhandled_input=self.unhandled_input, handle_mouse=False).run()


	def on_config_message(self, msg: Message) -> None:
		markup = (msg.notification_level.value, str(msg))
		widget_options_tuple = (urwid.Text(markup), self.status_bar.options('pack'))
		self.status_bar.contents.append(widget_options_tuple)
		self.frame.footer = self.status_bar

	def input_filter(self, keys: 'list[str]', raws: 'list[int]') -> 'list[str]':
		self.status_bar.contents.clear()
		Message.reset()
		return keys

	def unhandled_input(self, key: str) -> bool:
		cmd = urwid.command_map[key]
		if cmd == CMD_QUIT:
			raise urwid.ExitMainLoop()
		self.on_config_message(Message(NotificationLevel.ERROR, 'undefined key: %s' % key))
		return True


if __name__ == '__main__':
	app = App()
	app.run()
