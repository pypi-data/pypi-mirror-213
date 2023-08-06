#!../../../../venv/bin/python3

# ------- start -------
from confattr import ExplicitConfig, ConfigFile

class Bus:

	bitrate = ExplicitConfig('bus.bitrate', int, unit='')

config_file = ConfigFile(appname='test')
config_file.set_ui_callback(print)
config_file.load()

bus = Bus()
print(f"bitrate: {bus.bitrate}")  # This throws a TypeError if bus.bitrate has not been set in the config file
