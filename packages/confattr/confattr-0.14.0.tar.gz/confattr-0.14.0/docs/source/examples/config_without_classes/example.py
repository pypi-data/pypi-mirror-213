# ------- start -------
from confattr import Config, ConfigFile

backend = Config('urwid.backend', 'auto', allowed_values=('auto', 'raw', 'curses'))

config_file = ConfigFile(appname='example')
config_file.load()
config_file.set_ui_callback(lambda msg: print(msg))

print(backend.value)
