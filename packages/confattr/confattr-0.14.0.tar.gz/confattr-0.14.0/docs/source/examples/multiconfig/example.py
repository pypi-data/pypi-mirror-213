# ------- start -------
import enum
from confattr import Config, MultiConfig, ConfigId, ConfigFile, NotificationLevel

class Color(enum.Enum):
	RED = 'red'
	YELLOW = 'yellow'
	GREEN = 'green'
	BLUE = 'blue'
	WHITE = 'white'
	BLACK = 'black'


class Car:

	speed_limit = Config('traffic-law.speed-limit', 50, unit='km/h')
	color = MultiConfig('car.color', Color.BLACK)

	def __init__(self, config_id: ConfigId) -> None:
		self.config_id = config_id


if __name__ == '__main__':
	config_file = ConfigFile(appname='example',
		notification_level=Config('notification-level', NotificationLevel.ERROR))
	config_file.load()

	config_file.set_ui_callback(lambda msg: print(msg))

	cars = []
	for config_id in MultiConfig.config_ids:
		cars.append(Car(config_id))
	cars.append(Car(ConfigId('another-car')))

	for car in cars:
		print('color of %s: %s' % (car.config_id, car.color))
