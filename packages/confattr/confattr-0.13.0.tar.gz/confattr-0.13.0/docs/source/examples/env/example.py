#!../../../../venv/bin/python3

# ------- start -------
from confattr import Config, ConfigFile
greeting = Config('ui.greeting', 'hello world')
ConfigFile(appname='example-app').load()
print(greeting.value)
