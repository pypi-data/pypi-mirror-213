#!../../../../venv/bin/python3

# ------- start -------
from confattr import ConfigFile, Config, DictConfig, MultiConfig
from enum import Enum, auto

class Color(Enum):
	RED = auto()
	GREEN = auto()
	BLUE = auto()

Config('answer', 42, unit='', help={
	42: 'The answer to everything',
	23: '''
		The natural number following 22
		and preceding 24
	''',
})
DictConfig('color', dict(foreground=Color.RED, background=Color.GREEN))


if __name__ == '__main__':
	config_file = ConfigFile(appname='exampleapp')
	print(config_file.get_help())
