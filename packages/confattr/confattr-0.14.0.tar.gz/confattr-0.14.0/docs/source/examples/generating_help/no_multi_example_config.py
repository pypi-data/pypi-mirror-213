#!../../../../venv/bin/python3

from confattr import ConfigFile, ConfigFileWriter

from utils import run
run('no_multi_example.py', main=False, nextto=__file__)

config_file = ConfigFile(appname='exampleapp')
config_file.save_to_writer(ConfigFileWriter(f=None, prefix='# '))
