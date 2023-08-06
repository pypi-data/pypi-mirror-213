#!../venv/bin/pytest -s

import os
import re
import enum
import typing
import pytest
import pathlib


from confattr import Config, DictConfig, ConfigFile, NotificationLevel, Message, MultiConfig, MultiDictConfig, ConfigId
from confattr.configfile import Set
from confattr.formatters import Primitive

T_co = typing.TypeVar('T_co')


@pytest.fixture()
def fn_config(tmp_path: pathlib.Path) -> str:
	return str(tmp_path / 'config')


class ParseError(ValueError):
	pass

def ui_callback(msg: Message) -> None:
	if msg.notification_level is NotificationLevel.ERROR:
		raise ParseError(msg)


class COLOR(enum.Enum):
	RED = 'red'
	GREEN = 'green'
	BLUE = 'blue'


def test_get_and_set() -> None:
	class MyTestClass:
		myint = Config('a', 42, unit='', help='test attribute')

	t = MyTestClass()

	assert t.myint == 42
	assert isinstance(type(t).myint, Config)
	assert type(t).myint.key == 'a'
	assert type(t).myint.value == 42
	assert type(t).myint.help == 'test attribute'

	t.myint = 0

	assert t.myint == 0
	assert isinstance(type(t).myint, Config)
	assert type(t).myint.key == 'a'

def test_settings_are_consistent_across_different_objects() -> None:
	class MyTestClass:
		myint = Config('a', 42, unit='apples')

	t1 = MyTestClass()
	t2 = MyTestClass()

	t1.myint += 1

	assert t1.myint == 43
	assert t2.myint == 43

	t3 = MyTestClass()

	assert t1.myint == 43
	assert t2.myint == 43
	assert t3.myint == 43

def test_unique_keys() -> None:
	class A:
		a = Config('foo', 1, unit='')

	class B:
		with pytest.raises(ValueError):
			b = Config('foo', 2, unit='')

def test_unique_keys_rename() -> None:
	class A:
		a = Config('foo', 1, unit='')

	class B:
		b = Config('bar', 2, unit='')

	with pytest.raises(ValueError, match="duplicate config key 'foo'"):
		B.b.key = 'foo'

def test_change_key() -> None:
	c1 = Config('c', 'hello world')
	c1.key = 'greeting'

	c2 = Config('c', 'foo')

	assert c1.key == 'greeting'
	assert c1.value == 'hello world'

	assert c2.key == 'c'
	assert c2.value == 'foo'


def test__format_allowed_values_or_type_primitives() -> None:
	class SomeType:
		type_name = 'something'
		def __init__(self, val: str) -> None:
			self.val = val

	class MyTestClass:
		a = Config('a', 'hello world')
		b = Config('b', True)
		c = Config('c', COLOR.RED)
		f = Config('f', 3.14159, unit='')
		i = Config('i', 42, unit='')
		s = Config('s', SomeType('foo'))

	cf = ConfigFile(appname='test')
	assert MyTestClass.a.type.get_description(cf) == 'a str'
	assert MyTestClass.b.type.get_description(cf) == 'one of true, false'
	assert MyTestClass.c.type.get_description(cf) == 'one of red, green, blue'
	assert MyTestClass.f.type.get_description(cf) == 'a float'
	assert MyTestClass.i.type.get_description(cf) == 'an int'
	assert MyTestClass.s.type.get_description(cf) == 'a something'

def test__format_allowed_values_or_type__allowed_values_dict() -> None:
	PUD_OFF  = 0
	PUD_DOWN = 1
	PUD_UP   = 2
	pud = Config('pull-up-or-down', PUD_OFF, allowed_values=dict(off=PUD_OFF, down=PUD_DOWN, up=PUD_UP))
	cf = ConfigFile(appname='test')
	assert pud.type.get_description(cf) == 'one of off, down, up'

def test__format_allowed_values_or_type__list__type_without_unit() -> None:
	l = Config('l', [1, 2, 3], unit='')
	cf = ConfigFile(appname='test')
	assert l.type.get_description(cf) == 'a comma separated list of int'

def test__format_allowed_values_or_type__list__type_with_unit() -> None:
	l = Config('l', [1, 2, 3], unit='apples')
	cf = ConfigFile(appname='test')
	assert l.type.get_description(cf) == 'a comma separated list of int in apples'

def test__format_allowed_values_or_type__list__values_with_unit() -> None:
	l = Config('l', [1, 2, 3], allowed_values=(1,2,3), unit='oranges')
	cf = ConfigFile(appname='test')
	assert l.type.get_description(cf) == 'a comma separated list of 1, 2, 3 (unit: oranges)'

def test__format_allowed_values_or_type__list__values() -> None:
	l = Config('l', [COLOR.RED, COLOR.GREEN])
	cf = ConfigFile(appname='test')
	assert l.type.get_description(cf) == 'a comma separated list of red, green, blue'

def test__format_allowed_values_or_type__no_article() -> None:
	class Color:
		type_name = 'foreground[,emphases][/background]'
		type_article = None
	col = Config('col', Color())
	cf = ConfigFile(appname='test')
	assert col.type.get_description(cf) == 'foreground[,emphases][/background]'

def test__format_allowed_values_or_type__explicit_article() -> None:
	class Hour:
		type_name = 'hour'
		type_article = 'an'
		def __init__(self, val: int) -> None:
			self.val = val
	l = Config('h', Hour(12))
	cf = ConfigFile(appname='test')
	assert l.type.get_description(cf) == 'an hour'

def test__format_allowed_values_or_type__type_with_unit() -> None:
	l = Config('wait-time', .5, unit='seconds', help='time to wait')
	cf = ConfigFile(appname='test')
	assert l.type.get_description(cf) == 'a float in seconds'

def test__format_allowed_values_or_type__values_with_unit() -> None:
	l = Config('n', 1, allowed_values=(1,2,3,4,5), unit='oranges')
	cf = ConfigFile(appname='test')
	assert l.type.get_description(cf) == 'one of 1, 2, 3, 4, 5 (unit: oranges)'


# ------- DictConfig -------

def test__dict_config__format_bool_key() -> None:
	d = DictConfig('d', {True: '1', False: '0'})
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	fn = cf.save(comments=False)

	with open(fn, 'rt') as f:
		assert f.read() == '''\
set d.false = 0
set d.true = 1
'''

def test__dict_config__contains_and_iter() -> None:
	d = DictConfig('color', {
		COLOR.RED : 1,
		COLOR.GREEN : 1,
	}, ignore_keys = {COLOR.GREEN, COLOR.BLUE}, unit='')
	assert COLOR.RED in d
	assert COLOR.GREEN in d
	assert COLOR.BLUE not in d

	assert list(d) == [COLOR.RED, COLOR.GREEN]

def test__dict_config__get() -> None:
	d = DictConfig('color', {
		COLOR.RED : 1,
		COLOR.GREEN : 0.5,
	}, ignore_keys = {COLOR.GREEN, COLOR.BLUE}, unit='')

	assert d.get(COLOR.RED) == 1
	assert d.get(COLOR.BLUE) is None


# ------- MultiDictConfig -------

def test__multi_dict_config__add_new_items() -> None:
	class Widget:

		symbols = MultiDictConfig('symbols', {'new' : '+'})
		symbols['delete'] = '-'

		def __init__(self, name: str) -> None:
			self.config_id = ConfigId(name)

	w1 = Widget('foo')
	w2 = Widget('bar')
	assert w1.symbols['new'] == '+'
	assert w1.symbols['delete'] == '-'

	w1.symbols['same'] = '='
	assert w1.symbols['same'] == '='
	assert w2.symbols['same'] == '='

	w2.symbols['same'] = '/'
	assert w2.symbols['same'] == '/'
	assert w1.symbols['same'] == '='

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.save()

	w2.symbols['new'] = 'n'
	assert w2.symbols['new'] == 'n'
	assert w1.symbols['new'] == '+'

	cf.load()
	assert w1.symbols['new'] == '+'
	assert w1.symbols['delete'] == '-'
	assert w1.symbols['same'] == '='
	assert w2.symbols['new'] == '+'
	assert w2.symbols['delete'] == '-'
	assert w2.symbols['same'] == '/'



# ------- numbers require a unit -------

def test__float_requires_unit() -> None:
	with pytest.raises(TypeError) as e:
		i = Config('a', 1.414)
		assert str(e).startswith("missing argument unit")

def test__list_of_int_requires_unit() -> None:
	with pytest.raises(TypeError) as e:
		i = Config('a', [1,2,3])
		assert str(e).startswith("missing argument unit")


# ------- save only some -------

def test_save_some_in_given_order(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', 1, unit='')
		b = Config('b', 2, unit='')
		c = Config('c', 3, unit='')
		d = DictConfig('d', {COLOR.RED:1, COLOR.GREEN:2, COLOR.BLUE:3}, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	config_file.save_file(fn_config, config_instances=[MyTestClass.b, MyTestClass.d], comments=False)

	with open(fn_config, 'rt') as f:
		assert f.read() == '''\
set b = 2
set d.blue = 3
set d.green = 2
set d.red = 1
'''

	config_file.save_file(fn_config, config_instances=[MyTestClass.d, MyTestClass.b], comments=False)

	with open(fn_config, 'rt') as f:
		assert f.read() == '''\
set d.blue = 3
set d.green = 2
set d.red = 1
set b = 2
'''

def test_save_some_sorted() -> None:
	class MyTestClass:
		a = Config('a', 1, unit='')
		b = Config('b', 2, unit='')
		c = Config('c', 3, unit='')
		d = DictConfig('d', {COLOR.RED:1, COLOR.GREEN:2, COLOR.BLUE:3}, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	fn_config = config_file.save(config_instances={MyTestClass.d, MyTestClass.b}, comments=False)

	with open(fn_config, 'rt') as f:
		assert f.read() == '''\
set b = 2
set d.blue = 3
set d.green = 2
set d.red = 1
'''


def test_save_ignore(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', 1, unit='')
		b = Config('b', 2, unit='')
		c = Config('c', 3, unit='')
		d = DictConfig('d', {COLOR.RED:1, COLOR.GREEN:2, COLOR.BLUE:3}, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	config_file.save_file(fn_config, ignore={MyTestClass.d, MyTestClass.b}, comments=False)

	with open(fn_config, 'rt') as f:
		assert f.read() == '''\
set a = 1
set c = 3
'''

def test_save_ignore_multi_config(fn_config: str) -> None:
	class MyTestClass:
		def __init__(self, config_id: ConfigId) -> None:
			self.config_id = config_id
		a = Config('a', 1, unit='')
		b = Config('b', 2, unit='')
		c = Config('c', 3, unit='')
		m = MultiConfig('m', 42, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t1 = MyTestClass(ConfigId('1'))
	assert t1.m == 42
	t1.m = 1
	assert t1.m == 1

	t2 = MyTestClass(ConfigId('2'))
	assert t2.m == 42
	t2.m = 2
	assert t2.m == 2

	config_file.save_file(fn_config, ignore={MyTestClass.b, MyTestClass.m}, comments=False)

	with open(fn_config, 'rt') as f:
		assert f.read() == '''\
set a = 1
set c = 3
'''

def test_save_each_command_only_once_even_if_they_have_aliases() -> None:
	# abstract = True because I don't want this to replace the normal set in other test cases
	class SetWithAlias(Set, abstract=True):
		name = 'set'
		aliases = ['let']

	assert list(SetWithAlias.get_names()) == ['set', 'let']

	cf = ConfigFile(appname='test', commands=[SetWithAlias])
	cf.set_ui_callback(ui_callback)

	Config('foo', 42, unit='')
	fn = cf.save(comments=False)

	with open(fn, 'rt') as f:
		assert f.read() == '''\
set foo = 42
'''


def test_save_respects_wants_to_be_exported() -> None:
	class HiddenConfig(Config[T_co]):
		def wants_to_be_exported(self) -> bool:
			return False

	normal = Config('normal', 'hello world')
	hidden = HiddenConfig('hidden', 'I am too shy')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	fn = cf.save()

	with open(fn) as f:
		assert f.read() == '''\
# Data types
# ----------
# str:
#   A text. If it contains spaces it must be wrapped in single or
#   double quotes.

# normal
# ------
# a str
set normal = 'hello world'
'''

def test_save_multi_config_without_help_for_data_types() -> None:
	MultiConfig('flag', True)

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	fn = cf.save()

	with open(fn) as f:
		assert f.read() == '''\
# flag
# ----
# one of true, false
set flag = true
'''


# ------- write help -------

def test_help_no_multi() -> None:
	Config('answer', 42, unit='')
	expected = '''\
usage: set [--raw] key1=val1 [key2=val2 ...]
       set [--raw] key [=] val

Change the value of a setting.

In the first form set takes an arbitrary number of arguments, each
argument sets one setting. This has the advantage that several
settings can be changed at once. That is useful if you want to bind a
set command to a key and process that command with
ConfigFile.parse_line() if the key is pressed.

In the second form set takes two arguments, the key and the value.
Optionally a single equals character may be added in between as third
argument. This has the advantage that key and value are separated by
one or more spaces which can improve the readability of a config file.

You can use the value of another setting with %other.key% or an
environment variable with ${ENV_VAR}. If you want to insert a literal
percent character use two of them: %%. You can disable expansion of
settings and environment variables with the --raw flag.

data types:

  int:
    An integer number in python 3 syntax, as decimal (e.g. 42),
    hexadecimal (e.g. 0x2a), octal (e.g. 0o52) or binary (e.g.
    0b101010). Leading zeroes are not permitted to avoid confusion
    with python 2's syntax for octal numbers. It is permissible to
    group digits with underscores for better readability, e.g.
    1_000_000.

settings:

  answer:
    an int'''

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	assert Set(config_file).get_help() == expected

def test_help_no_normal() -> None:
	# get_help_config_id() is not wrapped to a width of 70 but 68
	# because argparse.HelpFormatter subtracts the indentation from the width
	# so that the text is not only indented from the left but from the right, too.
	# linewidth = textwidth - 2*indentation

	MultiConfig('greeting', 'hello world')
	expected = '''\
usage: set [--raw] key1=val1 [key2=val2 ...]
       set [--raw] key [=] val

Change the value of a setting.

In the first form set takes an arbitrary number of arguments, each
argument sets one setting. This has the advantage that several
settings can be changed at once. That is useful if you want to bind a
set command to a key and process that command with
ConfigFile.parse_line() if the key is pressed.

In the second form set takes two arguments, the key and the value.
Optionally a single equals character may be added in between as third
argument. This has the advantage that key and value are separated by
one or more spaces which can improve the readability of a config file.

You can use the value of another setting with %other.key% or an
environment variable with ${ENV_VAR}. If you want to insert a literal
percent character use two of them: %%. You can disable expansion of
settings and environment variables with the --raw flag.

data types:

  str:
    A text. If it contains spaces it must be wrapped in single or
    double quotes.

settings which can have different values for different objects:
  You can specify the object that a value shall refer to by
  inserting the line `[config-id]` above. `config-id` must be
  replaced by the corresponding identifier for the object.

  greeting:
    a str'''

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	assert Set(config_file).get_help() == expected


# ------- syntax -------

def test__parse_line() -> None:
	class MyTestClass:
		myint = Config('a', 42, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t = MyTestClass()
	assert t.myint == 42

	config_file.parse_line('set a=1')
	assert t.myint == 1

def test_load_with_spaces(fn_config: str) -> None:
	class MyTestClass:
		myint = Config('a', 42, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('set a = 1')

	t = MyTestClass()
	assert t.myint == 42

	config_file.load_file(fn_config)
	assert t.myint == 1

def test_load_without_spaces(fn_config: str) -> None:
	class MyTestClass:
		myint = Config('a', 42, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('set a=1')

	t = MyTestClass()
	assert t.myint == 42

	config_file.load_file(fn_config)
	assert t.myint == 1

def test_load_without_equals(fn_config: str) -> None:
	class MyTestClass:
		myint = Config('a', 42, unit='')
		mystr = Config('b', 'foo')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('''
			set a 1
			set b "foo bar"
		''')

	t = MyTestClass()
	assert t.myint == 42
	assert t.mystr == 'foo'

	config_file.load_file(fn_config)
	assert t.myint == 1
	assert t.mystr == 'foo bar'

def test_load_multiple(fn_config: str) -> None:
	class MyTestClass:
		myint = Config('a', 42, unit='')
		mystr = Config('b', 'foo')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('set a=1 b="foo bar"')

	t = MyTestClass()
	assert t.myint == 42
	assert t.mystr == 'foo'

	config_file.load_file(fn_config)
	assert t.myint == 1
	assert t.mystr == 'foo bar'


def test_load_multi_config(fn_config: str) -> None:
	class MyTestClass:
		a = MultiConfig('a', 0, unit='')
		def __init__(self, config_id: ConfigId) -> None:
			self.config_id = config_id

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('''
			[foo]
			set a = 11

			[bar]
			set a = 22
		''')

	t1 = MyTestClass(ConfigId('none'))
	t2 = MyTestClass(ConfigId('foo'))
	t3 = MyTestClass(ConfigId('bar'))
	assert t1.a == 0
	assert t2.a == 0
	assert t3.a == 0
	assert not MultiConfig.config_ids

	config_file.load_file(fn_config)
	assert t1.a == 0
	assert t2.a == 11
	assert t3.a == 22
	assert MultiConfig.config_ids == [ConfigId('foo'), ConfigId('bar')]


def test_load__include__no_implicit_reset_before(fn_config: str) -> None:
	class MyTestClass:
		path_src = MultiConfig('path.src', '')
		path_dst = MultiConfig('path.dst', '')
		direction = MultiConfig('direction', '')

		def __init__(self, config_id: ConfigId) -> None:
			self.config_id = config_id

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('''
			[doc]
			set path.src = src/documents
			set path.dst = dst/documents
			include mirror

			[music]
			set path.src = src/music
			set path.dst = dst/music
			include mirror

			[pic]
			set path.src = src/pictures
			set path.dst = dst/pictures
			include two-way
		''')

	path_root = os.path.dirname(fn_config)
	with open(os.path.join(path_root, 'mirror'), 'wt') as f:
		f.write('''
			set direction = '>'
		''')

	with open(os.path.join(path_root, 'two-way'), 'wt') as f:
		f.write('''
			set direction = '<>'
		''')

	config_file.load_file(fn_config)

	doc = MyTestClass(ConfigId('doc'))
	pic = MyTestClass(ConfigId('pic'))
	music = MyTestClass(ConfigId('music'))
	videos = MyTestClass(ConfigId('videos'))

	assert doc.path_src == 'src/documents'
	assert doc.path_dst == 'dst/documents'
	assert doc.direction == '>'

	assert music.path_src == 'src/music'
	assert music.path_dst == 'dst/music'
	assert music.direction == '>'

	assert pic.path_src == 'src/pictures'
	assert pic.path_dst == 'dst/pictures'
	assert pic.direction == '<>'

	assert videos.direction == ''

def test_load__include__implicit_reset_after(fn_config: str) -> None:
	class Bike:
		color = MultiConfig('color', '')
		gears = MultiConfig('gears', 8, unit='')

		def __init__(self, config_id: ConfigId) -> None:
			self.config_id = config_id

	with open(fn_config, 'wt') as f:
		f.write('''
			[my-bike]
			set color blue
			set gears 11

			[moms-bike]

			include other-config

			set color black
		''')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	path_root = os.path.dirname(fn_config)
	with open(os.path.join(path_root, 'other-config'), 'wt') as f:
		f.write('''
			set gears 7

			[kids-bike]
			set gears = 3
		''')

	config_file.load_file(fn_config)

	my_bike = Bike(ConfigId('my-bike'))
	moms_bike = Bike(ConfigId('moms-bike'))
	kids_bike = Bike(ConfigId('kids-bike'))
	default_bike = Bike(ConfigId('default-bike'))

	assert my_bike.color == 'blue'
	assert my_bike.gears == 11

	assert moms_bike.color == 'black'
	assert moms_bike.gears == 7

	assert kids_bike.color == ''
	assert kids_bike.gears == 3

	assert default_bike.color == ''
	assert default_bike.gears == 8

def test_load__include__explicit_reset_before(fn_config: str) -> None:
	class Bike:
		color = MultiConfig('color', '')
		gears = MultiConfig('gears', 7, unit='')

		def __init__(self, config_id: ConfigId) -> None:
			self.config_id = config_id

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('''
			[my-bike]
			set color blue
			set gears 8

			[moms-bike]

			include --reset-config-id other-config

			set color black
		''')

	path_root = os.path.dirname(fn_config)
	with open(os.path.join(path_root, 'other-config'), 'wt') as f:
		f.write('''
			set color undefined

			[kids-bike]
			set gears = 3
		''')

	config_file.load_file(fn_config)

	my_bike = Bike(ConfigId('my-bike'))
	moms_bike = Bike(ConfigId('moms-bike'))
	kids_bike = Bike(ConfigId('kids-bike'))
	default_bike = Bike(ConfigId('default-bike'))

	assert my_bike.color == 'blue'
	assert my_bike.gears == 8

	assert moms_bike.color == 'black'
	assert moms_bike.gears == 7

	assert kids_bike.color == 'undefined'
	assert kids_bike.gears == 3

	assert default_bike.color == 'undefined'
	assert default_bike.gears == 7

def test_load__include__explicit_no_reset_after(fn_config: str) -> None:
	class Bike:
		color = MultiConfig('color', '')
		gears = MultiConfig('gears', 7, unit='')

		def __init__(self, config_id: ConfigId) -> None:
			self.config_id = config_id

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('''
			include --no-reset-config-id color
			include --no-reset-config-id gears
		''')

	path_root = os.path.dirname(fn_config)
	with open(os.path.join(path_root, 'color'), 'wt') as f:
		f.write('''
			[my-bike]
			set color yellow
		''')
	with open(os.path.join(path_root, 'gears'), 'wt') as f:
		f.write('''
			set gears 14
		''')

	config_file.load_file(fn_config)

	my_bike = Bike(ConfigId('my-bike'))
	default_bike = Bike(ConfigId('default-bike'))

	assert my_bike.color == 'yellow'
	assert my_bike.gears == 14

	assert default_bike.color == ''
	assert default_bike.gears == 7

def test_load_include_from_command_line(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setattr(ConfigFile, 'config_directory', str(tmp_path))
	fn_config = str(tmp_path / 'config')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)

	config = Config('color', 'red')
	cf.save()

	config.value = 'green'
	cf.parse_line('include config')
	assert config.value == 'red'

def test__include__slash() -> None:
	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	config_path = os.path.dirname(config_file.get_save_path())
	config_path = os.path.join(config_path, 'foo', 'bar')

	os.mkdir(os.path.dirname(config_path))
	with open(config_path, 'wt') as f:
		f.write('set color = yellow')

	config = Config('color', 'red')
	assert config.value == 'red'

	config_file.parse_line('include foo/bar')
	assert config.value == 'yellow'


# ------- data types -------

def test_save_and_load_int(fn_config: str) -> None:
	class MyTestClass:
		myint = Config('a', 42, unit='apples')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t = MyTestClass()

	t.myint = 1
	assert t.myint == 1
	config_file.save_file(fn_config)
	assert t.myint == 1

	t.myint = 2
	assert t.myint == 2

	config_file.load_file(fn_config)
	assert t.myint == 1

	t.myint = 3
	config_file.save_file(fn_config)
	assert t.myint == 3

	t.myint = 4
	assert t.myint == 4

	config_file.load_file(fn_config)
	assert t.myint == 3

def test_parse_int() -> None:
	i = Config('i', 0, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	config_file.parse_line('set i = 0x2a')
	assert i.value == 42

	i.value = 0
	config_file.parse_line('set i = 0o52')
	assert i.value == 42

	i.value = 0
	config_file.parse_line('set i = 0b101010')
	assert i.value == 42

	config_file.parse_line('set i = 1_000_000')
	assert i.value == 1_000_000

def test_save_and_load_bool(fn_config: str) -> None:
	class MyTestClass:
		mybool = Config('a', True)

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	config_file.save_file(fn_config)

	t = MyTestClass()
	assert t.mybool == True

	t.mybool = False
	assert t.mybool == False

	config_file.load_file(fn_config)
	assert t.mybool == True

	t.mybool = False
	assert t.mybool == False
	config_file.save_file(fn_config)
	assert t.mybool == False

	t.mybool = True
	assert t.mybool == True

	config_file.load_file(fn_config)
	assert t.mybool == False

def test_save_and_load_float(fn_config: str) -> None:
	class MyTestClass:
		myfloat = Config('a', 3.14159, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	config_file.save_file(fn_config)

	t = MyTestClass()
	config_file.save_file(fn_config)
	assert t.myfloat == pytest.approx(3.14159)

	t.myfloat = 1.414
	assert t.myfloat == pytest.approx(1.414)

	config_file.load_file(fn_config)
	assert t.myfloat == pytest.approx(3.14159)

def test_save_and_load_str(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', 'hello world')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t = MyTestClass()
	assert t.a == 'hello world'

	t.a = 'hi there'
	assert t.a == 'hi there'
	config_file.save_file(fn_config)
	assert t.a == 'hi there'

	t.a = 'huhu'
	assert t.a == 'huhu'

	config_file.load_file(fn_config)
	assert t.a == 'hi there'

def test_save_and_load_str_newline(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', '\n')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	config_file.save_file(fn_config)

	t = MyTestClass()
	assert t.a == '\n'

	t.a = 'hi there'
	assert t.a == 'hi there'

	config_file.load_file(fn_config)
	assert t.a == '\n'

def test_save_and_load_spaces(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', 'hello world')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t = MyTestClass()
	assert t.a == 'hello world'

	t.a = '   '
	assert t.a == '   '
	config_file.save_file(fn_config)
	assert t.a == '   '

	t.a = 'huhu'
	assert t.a == 'huhu'

	config_file.load_file(fn_config)
	assert t.a == '   '

def test_save_and_load_enum(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', COLOR.RED)

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t = MyTestClass()
	assert t.a is COLOR.RED

	t.a = COLOR.GREEN
	assert t.a is COLOR.GREEN
	config_file.save_file(fn_config)
	assert t.a is COLOR.GREEN

	t.a = COLOR.BLUE
	assert t.a is COLOR.BLUE

	config_file.load_file(fn_config)
	assert t.a is COLOR.GREEN  # type: ignore [comparison-overlap]  # mypy does not undertstand that config_file.load_file should have changed t.a

def test_save_and_load_int_with_allowed_values(fn_config: str) -> None:
	PUD_OFF  = 0
	PUD_DOWN = 1
	PUD_UP   = 2
	class GPIO:
		pud = Config('pull-up-or-down', PUD_OFF, allowed_values=dict(off=PUD_OFF, down=PUD_DOWN, up=PUD_UP))

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	gpio = GPIO()
	assert gpio.pud == PUD_OFF

	gpio.pud = PUD_UP
	assert gpio.pud == PUD_UP
	config_file.save_file(fn_config)
	assert gpio.pud == PUD_UP

	gpio.pud = PUD_DOWN
	assert gpio.pud == PUD_DOWN

	config_file.load_file(fn_config)
	assert gpio.pud == PUD_UP

def test_save_and_load_list_of_int(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', [42], unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t = MyTestClass()
	assert t.a == [42]

	t.a = [1, 2, 3]
	assert t.a == [1, 2, 3]
	config_file.save_file(fn_config)
	assert t.a == [1, 2, 3]

	t.a = [4]
	assert t.a == [4]

	config_file.load_file(fn_config)
	assert t.a == [1, 2, 3]

def test_save_and_load_list_of_int__with_allowed_values(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', [42], allowed_values=(1,2,3,4,5,42), unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t = MyTestClass()
	assert t.a == [42]

	t.a = [1, 2, 3]
	assert t.a == [1, 2, 3]
	config_file.save_file(fn_config)
	assert t.a == [1, 2, 3]

	t.a = [4]
	assert t.a == [4]

	config_file.load_file(fn_config)
	assert t.a == [1, 2, 3]

def test_save_and_load_list_of_enum(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', [COLOR.RED])

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t = MyTestClass()
	assert t.a == [COLOR.RED]

	t.a = [COLOR.BLUE, COLOR.GREEN]
	assert t.a == [COLOR.BLUE, COLOR.GREEN]
	config_file.save_file(fn_config)
	assert t.a == [COLOR.BLUE, COLOR.GREEN]

	t.a = [COLOR.RED, COLOR.BLUE]
	assert t.a == [COLOR.RED, COLOR.BLUE]

	config_file.load_file(fn_config)
	assert t.a == [COLOR.BLUE, COLOR.GREEN]


def test_save_and_load_dict_enum(fn_config: str) -> None:
	class MyTestClass:
		color = DictConfig('color', {COLOR.RED:1, COLOR.GREEN:2, COLOR.BLUE:3}, ignore_keys={COLOR.BLUE}, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t = MyTestClass()
	config_file.save_file(fn_config)
	assert t.color[COLOR.RED] == 1
	assert t.color[COLOR.GREEN] == 2
	assert t.color[COLOR.BLUE] == 3

	t.color[COLOR.RED] = 10
	t.color[COLOR.GREEN] = 20
	t.color[COLOR.BLUE] = 30
	assert t.color[COLOR.RED] == 10
	assert t.color[COLOR.GREEN] == 20
	assert t.color[COLOR.BLUE] == 30

	config_file.load_file(fn_config)
	assert t.color[COLOR.RED] == 1
	assert t.color[COLOR.GREEN] == 2
	assert t.color[COLOR.BLUE] == 30

def test_save_and_load_multi_dict_enum(fn_config: str) -> None:
	class MyTestClass:
		def __init__(self, config_id: str):
			self.config_id = ConfigId(config_id)
		color = MultiDictConfig('color', {COLOR.RED:1, COLOR.GREEN:2, COLOR.BLUE:3}, ignore_keys={COLOR.BLUE}, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t0 = MyTestClass('t0')
	assert t0.color[COLOR.RED] == 1
	assert t0.color[COLOR.GREEN] == 2
	assert t0.color[COLOR.BLUE] == 3

	t0.color[COLOR.RED] = -1
	t0.color[COLOR.GREEN] = -2
	with pytest.raises(TypeError):
		t0.color[COLOR.BLUE] = -3
	assert t0.color[COLOR.RED] == -1
	assert t0.color[COLOR.GREEN] == -2
	assert t0.color[COLOR.BLUE] == 3

	t1 = MyTestClass('t1')
	assert t1.color[COLOR.RED] == 1
	assert t1.color[COLOR.GREEN] == 2
	assert t1.color[COLOR.BLUE] == 3
	t1.color[COLOR.RED] = 11
	t1.color[COLOR.GREEN] = 12
	with pytest.raises(TypeError):
		t1.color[COLOR.BLUE] = 13
	assert t1.color[COLOR.RED] == 11
	assert t1.color[COLOR.GREEN] == 12
	assert t1.color[COLOR.BLUE] == 3
	assert t0.color[COLOR.RED] == -1
	assert t0.color[COLOR.GREEN] == -2
	assert t0.color[COLOR.BLUE] == 3

	config_file.save_file(fn_config)
	t0.color[COLOR.RED] = 100
	t0.color[COLOR.GREEN] = 200
	with pytest.raises(TypeError):
		t0.color[COLOR.BLUE] = 300
	assert t0.color[COLOR.RED] == 100
	assert t0.color[COLOR.GREEN] == 200
	assert t0.color[COLOR.BLUE] == 3
	assert t1.color[COLOR.RED] == 11
	assert t1.color[COLOR.GREEN] == 12
	assert t1.color[COLOR.BLUE] == 3

	t1.color[COLOR.RED] = 1100
	t1.color[COLOR.GREEN] = 1200
	with pytest.raises(TypeError):
		t1.color[COLOR.BLUE] = 1300
	assert t1.color[COLOR.RED] == 1100
	assert t1.color[COLOR.GREEN] == 1200
	assert t1.color[COLOR.BLUE] == 3
	assert t0.color[COLOR.RED] == 100
	assert t0.color[COLOR.GREEN] == 200
	assert t0.color[COLOR.BLUE] == 3

	t2 = MyTestClass('t2')
	assert t2.color[COLOR.RED] == 1
	assert t2.color[COLOR.GREEN] == 2
	assert t2.color[COLOR.BLUE] == 3

	config_file.load_file(fn_config)
	assert t0.color[COLOR.RED] == -1
	assert t0.color[COLOR.GREEN] == -2
	assert t0.color[COLOR.BLUE] == 3
	assert t1.color[COLOR.RED] == 11
	assert t1.color[COLOR.GREEN] == 12
	assert t1.color[COLOR.BLUE] == 3
	assert t2.color[COLOR.RED] == 1
	assert t2.color[COLOR.GREEN] == 2
	assert t2.color[COLOR.BLUE] == 3

def test_save_and_load_multi_config_default() -> None:
	class Foo:
		alphabet = MultiConfig('alphabet', 'abc')
		config_id = 'foo'

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.save()
	assert Foo().alphabet == 'abc'

	Foo.alphabet.value = 'def'
	assert Foo().alphabet == 'def'

	cf.load()
	assert Foo().alphabet == 'abc'


# ------- config groups -------

def test__multi_config(fn_config: str) -> None:
	class MyTestClass:

		context_dependent_int = MultiConfig('context-dependent-int', 0, unit='')
		global_int = Config('global-int', 0, unit='')

		def __init__(self, config_id: ConfigId) -> None:
			self.config_id = config_id

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t1 = MyTestClass(ConfigId('foo'))
	t2 = MyTestClass(ConfigId('bar'))
	assert t1.context_dependent_int == 0
	assert t2.context_dependent_int == 0
	assert t1.global_int == 0
	assert t2.global_int == 0

	t1.context_dependent_int = 1
	t2.context_dependent_int = 2
	t1.global_int = -1
	t2.global_int = 42
	config_file.save_file(fn_config)
	assert t1.context_dependent_int == 1
	assert t2.context_dependent_int == 2
	assert t1.global_int == 42
	assert t2.global_int == 42

	t1.context_dependent_int = 10
	t2.context_dependent_int = 20
	t1.global_int = -2
	t2.global_int = 0xFF
	assert t1.context_dependent_int == 10
	assert t2.context_dependent_int == 20
	assert t1.global_int == 0xFF
	assert t2.global_int == 0xFF

	config_file.load_file(fn_config)
	assert t1.context_dependent_int == 1
	assert t2.context_dependent_int == 2
	assert t1.global_int == 42
	assert t2.global_int == 42

def test__multi_config_dict__set_defaults(fn_config: str) -> None:
	class MyTestClass:
		directions = MultiDictConfig('directions', {
			'new' : '>',
			'del' : '>',
			'dir' : '=',
		}, ignore_keys='dir')

		def __init__(self, config_id: str) -> None:
			self.config_id = ConfigId(config_id)

	assert MyTestClass.directions['new'] == '>'
	assert MyTestClass.directions['del'] == '>'
	assert MyTestClass.directions['dir'] == '='

	MyTestClass.directions['new'] = '<'
	assert MyTestClass.directions['new'] == '<'

	MyTestClass.directions['dir'] = '<'
	assert MyTestClass.directions['dir'] == '<'

	t1 = MyTestClass('t1')
	assert t1.directions['new'] == '<'
	assert t1.directions['dir'] == '<'

	t1.directions['new'] = '>'
	assert t1.directions['new'] == '>'
	assert MyTestClass.directions['new'] == '<'

	with pytest.raises(TypeError):
		t1.directions['dir'] = '>'
	assert t1.directions['dir'] == '<'
	assert MyTestClass.directions['dir'] == '<'

def test__multi_config_dict__load_defaults(fn_config: str) -> None:
	class MyTestClass:
		directions = MultiDictConfig('directions', {
			'new' : '>',
			'del' : '>',
			'dir' : '=',
		}, ignore_keys='dir')

		def __init__(self, config_id: str) -> None:
			self.config_id = ConfigId(config_id)

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	assert MyTestClass.directions['new'] == '>'
	assert MyTestClass.directions['del'] == '>'
	assert MyTestClass.directions['dir'] == '='

	with open(fn_config, 'wt') as f:
		f.write('set directions.new = "<"')
	config_file.load_file(fn_config)
	assert MyTestClass.directions['new'] == '<'
	assert MyTestClass.directions['del'] == '>'
	assert MyTestClass.directions['dir'] == '='

	with open(fn_config, 'wt') as f:
		f.write('set directions.dir = "<"')
	with pytest.raises(ParseError):
		config_file.load_file(fn_config)
	assert MyTestClass.directions['new'] == '<'
	assert MyTestClass.directions['del'] == '>'
	assert MyTestClass.directions['dir'] == '='

	t1 = MyTestClass('t1')
	assert t1.directions['new'] == '<'
	assert t1.directions['del'] == '>'
	assert t1.directions['dir'] == '='

def test__multi_config__reset() -> None:
	class Widget:

		a = Config('a', '1')
		greeting = MultiConfig('greeting', 'hello world')

		def __init__(self, name: str) -> None:
			self.config_id = ConfigId(name)

	config_file = ConfigFile(appname='example')
	config_file.set_ui_callback(lambda msg: print(msg))

	foo = Widget('foo')
	assert foo.greeting == 'hello world'

	config_file.save()
	foo.greeting = 'you there'
	assert foo.greeting == 'you there'

	foo.a = 'a'
	assert foo.a == 'a'

	MultiConfig.reset()
	config_file.load()
	assert foo.greeting == 'hello world'
	assert foo.a == '1'


# ------- comments -------

def test_load_vim_comment(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', 1, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t = MyTestClass()
	assert t.a == 1

	with open(fn_config, 'wt') as f:
		f.write('"a = 2')
	config_file.load_file(fn_config)
	assert t.a == 1

def test_load_bash_comment(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', 1, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	t = MyTestClass()
	assert t.a == 1

	with open(fn_config, 'wt') as f:
		f.write('#a = 2')
	config_file.load_file(fn_config)
	assert t.a == 1


# ------- errors -------

def test__error__missing_quote() -> None:
	c = Config('foo', '42')
	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with pytest.raises(ParseError, match=re.escape("""No closing quotation in line 'set foo="hello world'""")):
		config_file.parse_line('set foo="hello world')
	assert c.value == '42'

def test__error__missing_quote_without_exception() -> None:
	c = Config('foo', '42')
	config_file = ConfigFile(appname='test')

	messages: 'list[Message]' = []
	config_file.set_ui_callback(messages.append)

	config_file.parse_line('set foo="hello world')
	assert len(messages) == 1
	assert messages[0].message == 'No closing quotation'
	assert c.value == '42'


def test_load_invalid_color(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', COLOR.RED)

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('set a = yellow')

	with pytest.raises(ParseError, match=re.escape("invalid value for a: 'yellow' (should be one of red, green, blue)")):
		config_file.load_file(fn_config)

def test_load_forbidden_color(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', COLOR.GREEN, allowed_values=(COLOR.GREEN, COLOR.BLUE))

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('set a = red')

	with pytest.raises(ParseError, match=re.escape("invalid value for a: 'red' (should be one of green, blue)")):
		config_file.load_file(fn_config)

def test_load_forbidden_int_with_allowed_values_dict(fn_config: str) -> None:
	PUD_OFF  = 0
	PUD_DOWN = 1
	PUD_UP   = 2
	class GPIO:
		pud = Config('pull-up-or-down', PUD_OFF, allowed_values=dict(off=PUD_OFF, down=PUD_DOWN, up=PUD_UP))

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('set pull-up-or-down = auto')

	with pytest.raises(ParseError, match=re.escape("invalid value for pull-up-or-down: 'auto' (should be one of off, down, up)")):
		config_file.load_file(fn_config)

def test_save_invalid_int_with_allowed_values_dict() -> None:
	PUD_OFF  = 0
	PUD_DOWN = 1
	PUD_UP   = 2
	class GPIO:
		pud = Config('pull-up-or-down', 42, allowed_values=dict(off=PUD_OFF, down=PUD_DOWN, up=PUD_UP))

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with pytest.raises(ValueError, match=re.escape("42 is not an allowed value, should be one of 0, 1, 2")):
		config_file.save()

def test_load_forbidden_color_in_list(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', [COLOR.GREEN], allowed_values=(COLOR.GREEN, COLOR.BLUE))

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('set a = red')

	with pytest.raises(ParseError, match=re.escape("invalid value for a: 'red' (should be one of green, blue)")):
		config_file.load_file(fn_config)

def test_load_undefined_color_in_list(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', [COLOR.GREEN])

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('set a = yellow')

	with pytest.raises(ParseError, match=re.escape("invalid value for a: 'yellow' (should be one of red, green, blue)")):
		config_file.load_file(fn_config)

def test_load_forbidden_number_in_list(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', [1], allowed_values=(1, 2, 3, 4), unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('set a = 1,5')

	with pytest.raises(ParseError, match=re.escape("invalid value for a: '5' (should be one of 1, 2, 3, 4) in line 1 'set a = 1,5'")):
		config_file.load_file(fn_config)

def test_load_forbidden_value_for_multi_dict_config(fn_config: str) -> None:
	class MyTestClass:

		a = MultiDictConfig('a', {
			1 : 'a',
			2 : 'b' ,
			3 : 'c' ,
		}, allowed_values='abc')

		def __init__(self, config_id: str) -> None:
			self.config_id = ConfigId(config_id)

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('set a.1=d')

	with pytest.raises(ParseError, match=re.escape("invalid value for a.1: 'd' (should be one of a, b, c)")):
		config_file.load_file(fn_config)

	t = MyTestClass('general')
	assert t.a[1] == 'a'
	assert t.a[2] == 'b'
	assert t.a[3] == 'c'

def test_continue_setting_after_error_on_same_line(fn_config: str) -> None:
	class MyTestClass:

		a = MultiDictConfig('a', {
			1 : 'a',
			2 : 'b' ,
			3 : 'c' ,
		}, allowed_values='abc')

		def __init__(self, config_id: str) -> None:
			self.config_id = ConfigId(config_id)

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('set a.1=d a.2=c')

	with pytest.raises(ParseError, match=re.escape("invalid value for a.1: 'd' (should be one of a, b, c)")):
		config_file.load_file(fn_config)

	t = MyTestClass('general')
	assert t.a[1] == 'a'
	assert t.a[2] == 'c'
	assert t.a[3] == 'c'

def test_load_invalid_int(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', 1, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('set a = 1e3')

	with pytest.raises(ParseError, match=re.escape("invalid literal for int")):
		config_file.load_file(fn_config)

def test_load_invalid_key(fn_config: str) -> None:
	class MyTestClass:
		a = Config('a', 1, unit='')

	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	with open(fn_config, 'wt') as f:
		f.write('set b = true')

	with pytest.raises(ParseError, match=re.escape("invalid key 'b'")):
		config_file.load_file(fn_config)

def test_load_include_loop() -> None:
	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	fn_config = config_file.get_save_path()
	with open(fn_config, 'wt') as f:
		f.write('include other')

	fn_other = os.path.join(os.path.dirname(fn_config), 'other')
	with open(fn_other, 'wt') as f:
		f.write('include config')

	with pytest.raises(ParseError, match=re.escape("circular include")):
		config_file.load_file(fn_config)



def test__notification_level(fn_config: str) -> None:
	notification_level = Config('notification-level', NotificationLevel.ERROR)
	align = Config('align', 'left')

	with open(fn_config, 'wt') as f:
		f.write('''\
set align = center
set wrap = clip
set notification-level = info
set align = right
''')

	cfg = ConfigFile(notification_level=notification_level, appname='test')
	cfg.load_file(fn_config)

	messages: 'list[tuple[NotificationLevel, str|BaseException]]' = []
	cfg.set_ui_callback(lambda msg: messages.append((msg.lvl, msg.format_msg_line())))
	assert messages == [
		(NotificationLevel.ERROR, "invalid key 'wrap' in line 2 'set wrap = clip'"),
		(NotificationLevel.INFO, "set notification-level to info in line 3 'set notification-level = info'"),
		(NotificationLevel.INFO, "set align to right in line 4 'set align = right'"),
	]


def test_unknown_env_variable(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('TEST_FOO', '42')

	cfg = ConfigFile(appname='test')
	cfg.load()

	messages: 'list[str]' = []
	cfg.set_ui_callback(lambda msg: messages.append(msg.format_msg_line()))
	assert messages == ["unknown environment variable TEST_FOO='42'"]

def test_invalid_value_in_env_variable(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('TEST_FOO', 'hello world')

	foo = Config('foo', 42, unit='')
	cfg = ConfigFile(appname='test')
	cfg.load()

	messages: 'list[str]' = []
	cfg.set_ui_callback(lambda msg: messages.append(msg.format_msg_line()))
	assert messages == ["invalid literal for int() with base 0: 'hello world' while trying to parse environment variable TEST_FOO='hello world'"]

def test_env_name_collides_with_standard_environment_variable() -> None:
	x = Config('config.path', 'x')

	cfg = ConfigFile(appname='test')
	with pytest.raises(ValueError, match="setting 'config.path' conflicts with environment variable 'TEST_CONFIG_PATH'"):
		cfg.load()

def test_env_name_collides_with_other_setting() -> None:
	x1 = Config('foo-x', 'x')
	x2 = Config('foo.x', 'x')

	cfg = ConfigFile(appname='test')
	with pytest.raises(ValueError, match="settings 'foo.x' and 'foo-x' result in the same environment variable 'TEST_FOO_X'"):
		cfg.load()


def test__error__empty_list() -> None:
	with pytest.raises(TypeError, match='I cannot infer the item type from an empty list. Please pass an argument to the type parameter.'):
		Config('l', [])

def test__error__set_normal_config_with_config_id() -> None:
	c = Config('foo', 1, unit='')
	m = MultiConfig('multi', '42')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)

	cf.parse_line('[invalid]')
	with pytest.raises(ParseError, match="foo cannot be set for specific groups, config_id must be the default 'general' not 'invalid'"):
		cf.parse_line('set foo=2')

	assert c.value == 1

def test__error__set_invalid_value_for_bool() -> None:
	c = Config('foo', True)

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)

	with pytest.raises(ParseError, match=re.escape("invalid value for foo: '1' (should be one of true, false) in line 'set foo=1'")):
		cf.parse_line('set foo=1')

	assert c.value == 1

def test__error__invalid_value_for_custom_type() -> None:
	class Regex:
		type_name = 'regular expression'
		def __init__(self, pattern: str) -> None:
			self.reo = re.compile(pattern)
		def __str__(self) -> str:
			return self.reo.pattern

	c = Config('greeting', Regex('hello .*'))

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)

	with pytest.raises(ParseError, match=re.escape("invalid value for greeting: '*' (nothing to repeat at position 0) in line 'set greeting=*'")):
		cf.parse_line('set greeting=*')


def test__error__unkown_command_without_default_command() -> None:
	cf = ConfigFile(appname='test', commands=[Set])
	cf.set_ui_callback(ui_callback)
	with pytest.raises(ParseError, match="unknown command 'toggle'"):
		cf.parse_line('toggle a')

def test__error__set_no_arguments() -> None:
	cf = ConfigFile(appname='test', commands=[Set])
	cf.set_ui_callback(ui_callback)
	with pytest.raises(ParseError, match="no settings given"):
		cf.parse_line('set')

def test__error__no_value() -> None:
	cf = ConfigFile(appname='test', commands=[Set])
	cf.set_ui_callback(ui_callback)
	with pytest.raises(ParseError, match="missing value or missing ="):
		cf.parse_line('set a')

def test__error__invalid_separator() -> None:
	cf = ConfigFile(appname='test', commands=[Set])
	cf.set_ui_callback(ui_callback)
	with pytest.raises(ParseError, match="separator between key and value should be =, not 'b'"):
		cf.parse_line('set a b c')

def test__error__set_too_many_arguments() -> None:
	cf = ConfigFile(appname='test', commands=[Set])
	cf.set_ui_callback(ui_callback)
	with pytest.raises(ParseError, match="too many arguments given or missing = in first argument in line 'set a = b  c'"):
		cf.parse_line('set a = b  c')

def test__error__multiple_errors_on_one_line() -> None:
	messages: 'list[Message]' = []
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(messages.append)
	cf.parse_line('set a=b c')

	assert [msg.message for msg in messages] == [
	"invalid key 'a'",
	"missing = in 'c'",
]


def test__error__include_no_such_file() -> None:
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	with pytest.raises(ParseError, match="no such file '/a/b/c'"):
		cf.parse_line('include /a/b/c')

def test__error__argparse_error() -> None:
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	with pytest.raises(ParseError, match="unrecognized arguments: b"):
		cf.parse_line('include a b')

def test__help_text_error_and_set() -> None:
	class Path:

		type_name = 'path'

		def __init__(self, ln: str) -> None:
			self.raw = ln

		def __str__(self) -> str:
			return self.raw

	class Color(Primitive[str]):

		ALLOWED_VALUES = ['black', 'white']

		def __init__(self) -> None:
			super().__init__(str, type_name='color', allowed_values=self.ALLOWED_VALUES)

	Config('path', Path('foo'))
	Config('text-color', 'white', type=Color())

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	with pytest.raises(NotImplementedError, match="No help for type path"):
		cf.save()

	Primitive.help_dict[Path] = 'The path to a file'
	fn = cf.save()
	with open(fn, 'rt') as f:
		assert f.read() == """\
# Data types
# ----------
# color:
#   One of black, white

# path:
#   The path to a file

# path
# ----
# a path
set path = foo

# text-color
# ----------
# a color
set text-color = white
"""

def test_error_for_type_name_without_allowed_values() -> None:
	class Hex(Primitive[int]):
		def __init__(self) -> None:
			super().__init__(int, type_name='hex', unit='')
		# parse_value and format_value are not relevant for this test

	c = Config('mask', 0xFFFF, type=Hex())

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	with pytest.raises(NotImplementedError, match="used 'type_name' without 'allowed_values', please override 'get_help'"):
		cf.save()


# ------- repr -------

def test__repr__dict_config() -> None:
	d = DictConfig('key', {'a':1, 'b':2}, unit='')
	assert repr(d) == "DictConfig({'a': 1, 'b': 2}, ignore_keys=set(), ...)"

def test__repr__config() -> None:
	foo = Config('key', 'val')
	assert repr(foo) == "Config('key', 'val', ...)"


# ------- load from environment variables -------

def test_load_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('FOO_BAUDRATE', '500_000')
	baudrate = Config('baudrate', 250_000, unit='per second')
	assert baudrate.value == 250_000

	cf = ConfigFile(appname='foo')
	cf.load()
	assert baudrate.value == 500_000

def test_dont_load_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('FOO_BAUDRATE', '500_000')
	baudrate = Config('baudrate', 250_000, unit='per second')
	assert baudrate.value == 250_000

	cf = ConfigFile(appname='foo')
	cf.load(env=False)
	assert baudrate.value == 250_000


# ------- complete test -------

def test__save_and_load__config_file_can_be_instantiated_before_normal_config() -> None:
	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	c = Config('greeting', 'hello world')
	assert c.value == 'hello world'

	config_file.save()
	c.value = 'foo'
	assert c.value == 'foo'

	config_file.load()
	assert c.value == 'hello world'

def test__save_and_load__config_file_can_be_instantiated_before_mutli_config_with_explicit_enable_config_id() -> None:
	config_file = ConfigFile(appname='test', enable_config_ids=True)
	config_file.set_ui_callback(ui_callback)

	class Foo:
		config_id = 'foo'
		greeting = MultiConfig('greeting', 'hello world')

	foo = Foo()
	foo.greeting = 'hi there'
	assert foo.greeting == 'hi there'

	config_file.save()
	foo.greeting = 'something else'
	assert foo.greeting == 'something else'

	config_file.load()
	assert foo.greeting == 'hi there'

def test__save_and_load__config_path_attr(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	fn = str(tmp_path / 'config')
	monkeypatch.setattr(ConfigFile, 'config_path', str(fn))
	assert not os.path.exists(fn)

	assert list(config_file.iter_config_paths()) == [fn]

	c = Config('greeting', 'hello world')
	config_file.save()
	assert os.path.exists(fn)
	assert c.value == 'hello world'

	c.value = 'hi there'
	assert c.value == 'hi there'

	config_file.load()
	assert c.value == 'hello world'

def test__save_and_load__config_directory_attr(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	monkeypatch.setattr(ConfigFile, 'config_directory', str(tmp_path))
	fn = str(tmp_path / 'config')
	assert not os.path.exists(fn)

	assert list(config_file.iter_user_site_config_paths()) == [str(tmp_path)]
	assert list(config_file.iter_config_paths()) == [fn]

	c = Config('greeting', 'hello world')
	config_file.save()
	assert os.path.exists(fn)
	assert c.value == 'hello world'

	c.value = 'hi there'
	assert c.value == 'hi there'

	config_file.load()
	assert c.value == 'hello world'

def test__save_and_load__config_name_attr(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
	config_file = ConfigFile(appname='test')
	config_file.set_ui_callback(ui_callback)

	monkeypatch.setattr(ConfigFile, 'config_directory', str(tmp_path))
	monkeypatch.setattr(ConfigFile, 'config_name', 'test.conf')
	fn = str(tmp_path / 'test.conf')
	assert not os.path.exists(fn)

	assert list(config_file.iter_config_paths()) == [fn]

	c = Config('greeting', 'hello world')
	config_file.save()
	assert os.path.exists(fn)
	assert c.value == 'hello world'

	c.value = 'hi there'
	assert c.value == 'hi there'

	config_file.load()
	assert c.value == 'hello world'

def test__save_and_load__config_path_env(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
	fn = str(tmp_path / 'config')
	monkeypatch.setenv('TEST_CONFIG_PATH', str(fn))
	monkeypatch.setattr(ConfigFile, 'config_path', 'this value is overridden by the environment variable')
	assert not os.path.exists(fn)

	c = Config('greeting', 'hello world')

	# I need to create a new object because the environment variable is checked in the constructor
	cf = ConfigFile(appname='test')

	assert list(cf.iter_config_paths()) == [fn]

	cf.save()
	assert os.path.exists(fn)
	assert c.value == 'hello world'

	c.value = 'hi there'
	assert c.value == 'hi there'

	cf.load()
	assert c.value == 'hello world'

def test__save_and_load__config_directory_env(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('TEST_CONFIG_DIRECTORY', str(tmp_path))
	monkeypatch.setattr(ConfigFile, 'config_directory', 'this value is overridden by the environment variable')
	fn = str(tmp_path / 'config')
	assert not os.path.exists(fn)

	c = Config('greeting', 'hello world')

	# I need to create a new object because the environment variable is checked in the constructor
	cf = ConfigFile(appname='test')

	assert list(cf.iter_user_site_config_paths()) == [str(tmp_path)]
	assert list(cf.iter_config_paths()) == [fn]

	cf.save()
	assert os.path.exists(fn)
	assert c.value == 'hello world'

	c.value = 'hi there'
	assert c.value == 'hi there'

	cf.load()
	assert c.value == 'hello world'

def test__save_and_load__config_name_env(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('TEST_CONFIG_DIRECTORY', str(tmp_path))
	monkeypatch.setenv('TEST_CONFIG_NAME', 'test.conf')
	monkeypatch.setattr(ConfigFile, 'config_name', 'this value is overridden by the environment variable')
	fn = str(tmp_path / 'test.conf')
	assert not os.path.exists(fn)

	c = Config('greeting', 'hello world')

	# I need to create a new object because the environment variable is checked in the constructor
	cf = ConfigFile(appname='test')

	assert list(cf.iter_config_paths()) == [fn]

	cf.save()
	assert os.path.exists(fn)
	assert c.value == 'hello world'

	c.value = 'hi there'
	assert c.value == 'hi there'

	cf.load()
	assert c.value == 'hello world'
