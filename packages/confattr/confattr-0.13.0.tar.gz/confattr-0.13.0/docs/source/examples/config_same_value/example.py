# ------- start -------
from confattr import Config

class Car:
	speed_limit = Config('traffic-law.speed-limit', 50, unit='km/h')

c1 = Car()
c2 = Car()

print(c1.speed_limit, c2.speed_limit)
c2.speed_limit = 30  # don't do this, this is misleading!
print(c1.speed_limit, c2.speed_limit)
