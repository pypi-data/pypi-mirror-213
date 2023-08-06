#!../../../../venv/bin/python3
# ------- start -------
from confattr import MultiConfig, ConfigId, ConfigFile

class Widget:

	greeting = MultiConfig('greeting', 'hello world')

	def __init__(self, name: str) -> None:
		self.config_id = ConfigId(name)

config_file = ConfigFile(appname='example')
config_file.set_ui_callback(lambda msg: print(msg))

w1 = Widget('w1')
assert w1.greeting == 'hello world'

config_file.save(comments=False)
w1.greeting = 'hey you'
assert w1.greeting == 'hey you'

#MultiConfig.reset()   # This is missing
config_file.load()
assert w1.greeting == 'hello world'   # This fails!
