#!../../../../venv/bin/python3
__package__ = 'map'
from confattr import ConfigFile
from .example import Map

# ------- start -------
print(ConfigFile(appname='example').command_dict['map'].get_help())
