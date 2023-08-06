#!/usr/bin/env python3
# ------- start -------
from confattr import Config, ConfigFile

class App:

	color = Config('color', 'red', allowed_values=['red', 'green', 'blue'])


if __name__ == '__main__':
	config_file = ConfigFile(appname='example')
	config_file.load()

	a = App()
	print(a.color)
