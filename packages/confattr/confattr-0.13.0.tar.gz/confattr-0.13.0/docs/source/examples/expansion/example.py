#!../../../../venv/bin/python3

# ------- start -------
from confattr import Config, ConfigFile

class App:
	s = Config('s', 'hello world')
	i = Config('i', 42, unit='')
	b = Config('b', True)
	l = Config('l', [1, 2, 3], unit='')
	d = Config('d', dict(a=1, b=2, c=3), unit='')
a = App()

config_file = ConfigFile(appname='exampleapp')
config_file.set_ui_callback(print)
# ------- 1 -------
config_file.parse_line('set s = "%i% = 0x%i:02X%"')
assert a.s == '42 = 0x2A'
# ------- 2 -------
config_file.parse_line('set s = "[%b!:<5%] ..."')
assert a.s == '[true ] ...'
# ------- 3 -------
config_file.parse_line('set i = %b:d%')
assert a.i == 1
# ------- 4 -------
config_file.parse_line('set s="i was %i%" i=2 s="%s%, i is %i%"')
assert a.s == 'i was 1, i is 2'
# ------- 5 -------
config_file.parse_line('set l="%l%,4"')
assert a.l == [1, 2, 3, 4]

config_file.parse_line('set d="%d%,d:4"')
assert a.d == dict(a=1, b=2, c=3, d=4)
# ------- 6 -------
# select all elements except for the second element
# i.e. all elements except for index 1
config_file.parse_line('set l="%l:[:1,2:]%"')
assert a.l == [1, 3, 4]

# select all elements except for key b
config_file.parse_line('set d="%d:{^b}%"')
assert a.d == dict(a=1, c=3, d=4)

# select the elements for keys c and d
# and assign the value of key a to z
config_file.parse_line('set d="%d:{c,d}%,z:%d:[a]%"')
assert a.d == dict(c=3, d=4, z=1)
# ------- 7 -------
config_file.parse_line('set s="%i%%%"')
assert a.s == '2%'
# ------- 8 -------
config_file.parse_line('set s="hello ${HELLO:-world}"')
assert a.s == 'hello world'
