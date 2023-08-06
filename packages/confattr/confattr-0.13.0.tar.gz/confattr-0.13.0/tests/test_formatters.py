#!../venv/bin/pytest -vv

import enum
import inspect
import typing
from collections.abc import Iterator, Container

from confattr import Config, ConfigFile
from confattr.formatters import List, Dict, Primitive, Hex

import pytest

def test_hex() -> None:
	c = Config('c', 0xFF, type=Hex(), help="This is just a test.")
	cf = ConfigFile(appname='test')

	fn = cf.save(comments=True)
	with open(fn, 'rt') as f:
		assert f.read() == '''\
# c
# -
# a hexadecimal number
# This is just a test.
set c = FF
'''

	cf.parse_line('set c = 23')
	assert c.value == 0x23

def test_empty_list_of_hex() -> None:
	c = Config('c', [], type=List(item_type=Hex()))
	cf = ConfigFile(appname='test')

	fn = cf.save(comments=True)
	with open(fn, 'rt') as f:
		assert f.read() == '''\
# c
# -
# a comma separated list of hexadecimal numbers
set c = ''
'''

	cf.parse_line('set c = 23')
	assert c.value == [0x23]


def iter_intersting_attributes(o: 'Primitive[typing.Any]', *, ignore: 'Container[str]' = []) -> 'Iterator[str]':
	for name, val in inspect.getmembers(o):
		if name.startswith('__'):
			continue
		if inspect.ismethod(val):
			continue
		if name == 'config_key':
			continue
		if name in ignore:
			continue

		yield name


def test_copy_primitive() -> None:
	p = Primitive(str, allowed_values=('red', 'green', 'blue'), type_name='color', unit='')

	for name in iter_intersting_attributes(p):
		assert getattr(p, name) is not None, f"{name} has not been set so I cannot test whether it will be copied"

	p2 = p.copy()
	for name in iter_intersting_attributes(p):
		assert getattr(p, name) == getattr(p2, name), f"{name} has not been copied"

def test_copy_hex() -> None:
	p = Hex(allowed_values=(0xFF, 0xFE))

	for name in iter_intersting_attributes(p, ignore=('type_name')):
		assert getattr(p, name) is not None, f"{name} has not been set so I cannot test whether it will be copied"

	p2 = p.copy()
	for name in iter_intersting_attributes(p):
		assert getattr(p, name) == getattr(p2, name), f"{name} has not been copied"

def test_copy_primitive_ignore_config_key() -> None:
	p = Primitive(str, allowed_values=('red', 'green', 'blue'), type_name='color', unit='')
	p.set_config_key('foo')

	for name in iter_intersting_attributes(p):
		assert getattr(p, name) is not None, f"{name} has not been set so I cannot test whether it will be copied"

	p2 = p.copy()
	for name in iter_intersting_attributes(p):
		assert getattr(p, name) == getattr(p2, name), f"{name} has not been copied"
	p2.set_config_key('bar')

	assert p.config_key == 'foo'
	assert p2.config_key == 'bar'


def test_set_comparable() -> None:
	c = Config('myset', {3,2,1}, unit='')
	cf = ConfigFile(appname='test')

	fn = cf.save(comments=True)
	with open(fn, 'rt') as f:
		assert f.read() == '''\
# Data types
# ----------
# int:
#   An integer number in python 3 syntax, as decimal (e.g. 42),
#   hexadecimal (e.g. 0x2a), octal (e.g. 0o52) or binary (e.g.
#   0b101010). Leading zeroes are not permitted to avoid confusion
#   with python 2's syntax for octal numbers. It is permissible to
#   group digits with underscores for better readability, e.g.
#   1_000_000.

# myset
# -----
# a comma separated set of int
set myset = 1,2,3
'''
	assert c.value == {1,2,3}

	cf.parse_line('set myset = 1,1')
	assert c.value == {1}

def test_set_not_comparable() -> None:
	class Color(enum.Enum):
		RED = enum.auto()
		GREEN = enum.auto()
		BLUE = enum.auto()

	c = Config('myset', {Color.RED, Color.BLUE})
	cf = ConfigFile(appname='test')

	fn = cf.save(comments=True)
	with open(fn, 'rt') as f:
		assert f.read() == '''\
# myset
# -----
# a comma separated set of red, green, blue
set myset = blue,red
'''

	cf.parse_line('set myset = green,blue')
	assert c.value == {Color.GREEN, Color.BLUE}


def test_dict() -> None:
	c = Config('mydict', {"a":1, "b":2, "c":3}, unit='')
	cf = ConfigFile(appname='test')

	fn = cf.save(comments=True)
	with open(fn, 'rt') as f:
		assert f.read() == '''\
# Data types
# ----------
# int:
#   An integer number in python 3 syntax, as decimal (e.g. 42),
#   hexadecimal (e.g. 0x2a), octal (e.g. 0o52) or binary (e.g.
#   0b101010). Leading zeroes are not permitted to avoid confusion
#   with python 2's syntax for octal numbers. It is permissible to
#   group digits with underscores for better readability, e.g.
#   1_000_000.

# str:
#   A text. If it contains spaces it must be wrapped in single or
#   double quotes.

# mydict
# ------
# a dict of str:int
set mydict = a:1,b:2,c:3
'''

	cf.parse_line('set mydict = a:0,b:1')
	assert c.value == {"a":0, "b":1}

def test_dict_hex() -> None:
	c = Config('mydict', {"a":0xa, "b":0xb, "c":0xc}, type=Dict(Primitive(str), Hex()))
	cf = ConfigFile(appname='test')

	fn = cf.save(comments=True)
	with open(fn, 'rt') as f:
		assert f.read() == '''\
# Data types
# ----------
# str:
#   A text. If it contains spaces it must be wrapped in single or
#   double quotes.

# mydict
# ------
# a dict of str:hexadecimal number
set mydict = a:A,b:B,c:C
'''

	cf.parse_line('set mydict = a:1,b:2')
	assert c.value == {"a":1, "b":2}


# ========== errors ==========

def test_error_empty_set() -> None:
	with pytest.raises(TypeError, match="I cannot infer the item type from an empty set. Please pass an argument to the type parameter."):
		c: 'Config[set[str]]' = Config('c', set())

def test_error_empty_dict() -> None:
	with pytest.raises(TypeError, match="I cannot infer the key and value types from an empty dict. Please pass an argument to the type parameter."):
		c: 'Config[dict[str,int]]' = Config('c', {})

def test_error_when_passing_unit_and_type() -> None:
	with pytest.raises(TypeError, match="The keyword argument 'unit' is not supported if 'type' is given."):
		c = Config('c', 0xFF, type=Hex(), unit='apples')

def test_error_when_passing_allowed_values_and_type() -> None:
	with pytest.raises(TypeError, match="The keyword argument 'allowed_values' is not supported if 'type' is given."):
		c = Config('c', 0x1234, type=Hex(), allowed_values=(0x1234, 0x4321))

def test_error_when_trying_to_reuse_type() -> None:
	t = Primitive(int, unit='', allowed_values=(1,2,3))
	c1 = Config('c1', 1, type=t)
	with pytest.raises(TypeError, match="config_key has already been set to 'c1', not setting to 'c2'"):
		c2 = Config('c2', 2, type=t)

def test_error_when_help_has_wrong_type() -> None:
	class TestType(int):

		help = b"This won't work"

	c = Config('c', TestType(2))
	cf = ConfigFile(appname='test')
	with pytest.raises(TypeError, match="help attribute of 'TestType' has invalid type 'bytes'"):
		cf.save()
