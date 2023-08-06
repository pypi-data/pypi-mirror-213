# ------- start -------
from confattr import Config

class Car:

	speed_limit = Config('traffic-law.speed-limit', 50, unit='km/h')

	def __init__(self) -> None:
		self.speed = 0

	def accelerate(self, value: int) -> None:
		new_speed = self.speed + value
		if new_speed > self.speed_limit:
			raise ValueError('you are going too fast')

		self.speed = new_speed
# ------- 01 -------
	def print_config(self) -> None:
		print('{key}: {val}'.format(key=type(self).speed_limit.key, val=self.speed_limit))
# ------- 02 -------
if __name__ == '__main__':
	from confattr import ConfigFile, NotificationLevel
	config_file = ConfigFile(appname='example',
		notification_level=Config('notification-level', NotificationLevel.ERROR))
	config_file.load()

	# Print error messages which occurred while loading the config file.
	# In this easy example it would have been possible to register the callback
	# before calling load but in the real world the user interface
	# will depend on the values set in the config file.
	# Therefore the messages are stored until a callback is added.
	config_file.set_ui_callback(lambda msg: print(msg))

	c1 = Car()
	print('speed_limit: %s' % c1.speed_limit)
# ------- 02-end -------
	config_file.config_name = 'exported-config'
	def print(text: str) -> None: pass
# ------- 03-begin -------
	filename = config_file.save()
	print('configuration was written to %s' % filename)
