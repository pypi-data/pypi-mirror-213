#!../../../../venv/bin/python3

from confattr import ConfigFile
from argparse import RawTextHelpFormatter

from utils import run
run('example.py', main=False, nextto=__file__)

config_file = ConfigFile(appname='exampleapp', formatter_class=RawTextHelpFormatter)
print(config_file.get_help())
