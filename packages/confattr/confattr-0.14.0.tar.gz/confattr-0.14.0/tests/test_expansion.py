#!../venv/bin/pytest -s

from confattr import Config, ConfigFile, Message

import sys
import pytest


class ParseError(ValueError):
	pass

def ui_callback(msg: Message) -> None:
	raise ParseError(msg)

def list_messages(cf: ConfigFile) -> 'list[str|BaseException]':
	messages: 'list[Message]' = []
	cf.set_ui_callback(messages.append)
	return [m.message for m in messages]


# ------- expand_config -------

def test_expand_config() -> None:
	a = Config('a', 42, unit='')
	b = Config('b', 'foo')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="a is %a%"')
	assert b.value == 'a is 42'

def test_expand_config_format_value() -> None:
	a = Config('a', 42, unit='')
	b = Config('b', 'foo')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="%a% = 0x%a:02X%"')
	assert b.value == '42 = 0x2A'

def test_expand_config_format_default() -> None:
	a = Config('a', True)
	b = Config('b', 'foo')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="|%a!:^20%|"')
	assert b.value == '|        true        |'

def test_expand_config_format_repr() -> None:
	a = Config('a', 'hello world')
	b = Config('b', 'foo')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="and I say %a!r%"')
	assert b.value == "and I say 'hello world'"

@pytest.mark.skipif(sys.version_info < (3, 7), reason='str.isascii requires Python 3.7 or newer')
def test_expand_config_format_ascii() -> None:
	a = Config('a', 'hällo wörld')
	b = Config('b', 'foo')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="and I say %a!a%"')
	assert not a.value.isascii()
	assert 'and I say' in b.value
	assert b.value.isascii()

def test_expand_config_format_str() -> None:
	a = Config('a', True)
	b = Config('b', 'foo')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="a is %a!s%"')
	assert b.value == "a is True"

def test_expand_config_format_invalid_conversion() -> None:
	a = Config('a', True)
	b = Config('b', 'foo')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	with pytest.raises(ParseError, match=r"invalid conversion 'foo'"):
		cf.parse_line('set b="a is %a!foo%"')
	assert b.value == "foo"

def test_expand_invalid_key() -> None:
	a = Config('a', 42, unit='')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.parse_line('set b=%foo%')

	messages: 'list[Message]' = []
	cf.set_ui_callback(messages.append)
	assert len(messages) == 1
	assert messages[0].message == "invalid key 'foo'"

def test_expand_odd_number_of_percent_characters() -> None:
	a = Config('a', 42, unit='')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.parse_line('set b=%a%%')

	messages: 'list[Message]' = []
	cf.set_ui_callback(messages.append)
	assert len(messages) == 1
	assert messages[0].message.startswith("uneven number of percent characters")   # type: ignore [union-attr]  # BaseException has no attribute "startswith"


# ------- expand_config: list -------

def test_expand_list_length_without_int_format() -> None:
	l = Config('l', ['a', 'b', 'c', 'd', 'e'])

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %l:len%')

	msg, = list_messages(cf)
	assert msg == '5'

def test_expand_list_length_with_int_format() -> None:
	l = Config('l', ['a', 'b', 'c', 'd', 'e'])

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %l:len:b%')

	msg, = list_messages(cf)
	assert msg == '101'

def test_expand_list_one_item() -> None:
	l = Config('l', ['a', 'b', 'c', 'd', 'e'])

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %l:[1]%')

	msg, = list_messages(cf)
	assert msg == 'b'

def test_expand_list_slice_open_beginning() -> None:
	l = Config('l', ['a', 'b', 'c', 'd', 'e'])

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %l:[:3]%')

	msg, = list_messages(cf)
	assert msg == 'a,b,c'

def test_expand_list_slice_open_end() -> None:
	l = Config('l', ['a', 'b', 'c', 'd', 'e'])

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %l:[-2:]%')

	msg, = list_messages(cf)
	assert msg == 'd,e'

def test_expand_list_slice_reverse() -> None:
	l = Config('l', ['a', 'b', 'c', 'd', 'e'])

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %l:[::-1]%')

	msg, = list_messages(cf)
	assert msg == 'e,d,c,b,a'

def test_expand_list_items_to_be_excluded() -> None:
	l = Config('l', ['a', 'b', 'c', 'd', 'e'])

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %l:-a,c,f%')

	msg, = list_messages(cf)
	assert msg == 'b,d,e'

def test_expand_list_min_max() -> None:
	l = Config('fruits', ['oranges', 'apples', 'strawberries', 'bananas'])

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %fruits:min%')
	cf.parse_line('echo %fruits:max:^20%')

	msg_min, msg_max = list_messages(cf)
	assert msg_min == 'apples'
	assert msg_max == 'strawberries'.center(20)


def test_expand_list__empty_list_spec__item_spec() -> None:
	l = Config('l', [0x1, 0x23, 0xFF], unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo "%l::02x%"')

	msg, = list_messages(cf)
	assert msg == '01,23,ff'

def test_expand_list__slice__item_spec() -> None:
	l = Config('l', [0x1, 0x23, 0xFF], unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo "%l:[1]:02x%"')

	msg, = list_messages(cf)
	assert msg == '23'


def test_error_invalid_format_spec_with_primitive() -> None:
	greeting = Config('greeting', 'hello')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %greeting:invalid%')

	msg, = list_messages(cf)
	assert isinstance(msg, str)
	assert msg.startswith("Invalid format specifier")

def test_error_invalid_format_spec_with_stringifier() -> None:
	greeting = Config('greeting', 'hello')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %greeting!s:invalid%')

	msg, = list_messages(cf)
	assert isinstance(msg, str)
	assert msg.startswith("Invalid format specifier")

def test_error_invalid_format_spec_for_list__invalid_function() -> None:
	l = Config('l', ['a', 'b', 'c', 'd', 'e'])

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %l:invalid%')

	msg, = list_messages(cf)
	assert msg == "Invalid format_spec for collection: 'invalid'"

def test_error_invalid_format_spec_for_list__no_match() -> None:
	l = Config('l', ['a', 'b', 'c', 'd', 'e'])

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %l:[foo]invalid%')

	msg, = list_messages(cf)
	assert msg == "Invalid format_spec for collection: '[foo]invalid'"

def test_error_min_with_not_comparable_type() -> None:
	class Path:
		def __init__(self, path: str) -> None:
			self.path = path

		def expand(self) -> str:
			return self.path

	l = Config('paths', [Path('/'), Path('~')])

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %paths:min%')

	msg, = list_messages(cf)
	assert msg == "'<' not supported between instances of 'Path' and 'Path'"


# ------- expand_config: set -------

def test_expand_set__items_to_be_excluded() -> None:
	l = Config('l', {'e', 'c', 'b', 'd', 'a'})

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %l:-a,c,f%')

	msg, = list_messages(cf)
	assert msg == 'b,d,e'

def test_expand_set__length_without_int_format() -> None:
	l = Config('l', {'e', 'c', 'b', 'd', 'a'})

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %l:len%')

	msg, = list_messages(cf)
	assert msg == '5'

def test_expand_set__min_max() -> None:
	l = Config('fruits', {'oranges', 'apples', 'strawberries', 'bananas'})

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %fruits:min%')
	cf.parse_line('echo %fruits:max:^20%')

	msg_min, msg_max = list_messages(cf)
	assert msg_min == 'apples'
	assert msg_max == 'strawberries'.center(20)

def test_expand_set__empty_set_spec__item_spec() -> None:
	l = Config('l', {0x1, 0x23, 0xFF}, unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo "%l::02x%"')

	msg, = list_messages(cf)
	assert msg == '01,23,ff'


# ------- expand_config: dict -------

def test_expand_dict__single_value__without_format_spec() -> None:
	mydict = Config('mydict', dict(a=1, b=2, c=3), unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %mydict:[b]%')

	msg, = list_messages(cf)
	assert msg == '2'

def test_expand_dict__single_value__with_format_spec() -> None:
	mydict = Config('mydict', dict(a=1, b=2, c=3), unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %mydict:[b]:b%')

	msg, = list_messages(cf)
	assert msg == '10'

def test_expand_dict__single_value__default() -> None:
	mydict = Config('mydict', dict(a=1, b=2, c=3), unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %mydict:[d|foo]:b%')

	msg, = list_messages(cf)
	assert msg == 'foo'

def test_expand_dict__single_value__format() -> None:
	mydict = Config('mydict', dict(a=1, b=2, c=3), unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %mydict:[c|foo]:b%')

	msg, = list_messages(cf)
	assert msg == '11'

def test_expand_dict__filter_keys() -> None:
	mydict = Config('mydict', dict(a=1, b=2, c=3), unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %mydict:{^c}%')

	msg, = list_messages(cf)
	assert msg == 'a:1,b:2'

def test_expand_dict__select_keys__without_format_spec() -> None:
	mydict = Config('mydict', dict(a=1, b=2, c=3), unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %mydict:{a,b,d}%')

	msg, = list_messages(cf)
	assert msg == 'a:1,b:2'

def test_expand_dict__select_keys__with_format_spec() -> None:
	mydict = Config('mydict', dict(a=1, b=2, c=3), unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %mydict:{a,b,d}:b%')

	msg, = list_messages(cf)
	assert msg == 'a:1,b:10'

def test_expand_dict__len__without_format_spec() -> None:
	mydict = Config('mydict', dict(a=1, b=2, c=3), unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %mydict:len%')

	msg, = list_messages(cf)
	assert msg == '3'

def test_expand_dict__len__with_format_spec() -> None:
	mydict = Config('mydict', dict(a=1, b=2, c=3), unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %mydict:len:02d%')

	msg, = list_messages(cf)
	assert msg == '03'


def test_expand_dict__no_match() -> None:
	mydict = Config('mydict', dict(a=1, b=2, c=3), unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %mydict:{}a,b,d}%')

	msg, = list_messages(cf)
	assert msg == "Invalid format_spec for dict: '{}a,b,d}'"

def test_expand_dict__invalid_func() -> None:
	mydict = Config('mydict', dict(a=1, b=2, c=3), unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %mydict:invalid%')

	msg, = list_messages(cf)
	assert msg == "Invalid format_spec for dict: 'invalid'"

def test_expand_dict__key_not_contained() -> None:
	mydict = Config('mydict', dict(a=1, b=2, c=3), unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo %mydict:[d]%')

	msg, = list_messages(cf)
	assert msg == "key 'd' is not contained in 'mydict'"


# ------- expand_env -------

def test_expand_defined_env_normal(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', 'world')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO}"')

	assert b.value == 'hello world'

def test_expand_undefined_env_normal() -> None:
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO}"')

	assert b.value == 'hello '


def test_expand_defined_env_default_value_with_colon(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', 'universe')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:-world}"')

	assert b.value == 'hello universe'

def test_expand_undefined_env_default_value_with_colon() -> None:
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:-world}"')

	assert b.value == 'hello world'

def test_expand_empty_env_default_value_with_colon(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', '')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:-world}"')

	assert b.value == 'hello world'

def test_expand_empty_env_default_value_without_colon(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', '')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO-world}"')

	assert b.value == 'hello '


def test_expand_defined_env_assign_value_with_colon(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', 'universe')
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:=world}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert b.value == 'hello universe'
	assert c.value == 'hello universe'

def test_expand_undefined_env_assign_value_with_colon(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO' ,'')  # reset the value that I will assign during this test at the end of the test
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:=world}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert b.value == 'hello world'
	assert c.value == 'hello world'


def test_expand_defined_env_indicate_error(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', 'world')
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:?}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert b.value == 'hello world'
	assert c.value == 'hello world'

def test_expand_undefined_env_indicate_error_with_default_message() -> None:
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	messages: 'list[Message]' = []
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(messages.append)
	cf.parse_line('set b="hello ${HELLO:?}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert len(messages) == 1
	assert messages[0].message == 'environment variable HELLO is unset'

	assert b.value == 'foo'
	assert c.value == 'hello '

def test_expand_empty_env_indicate_error_with_default_message(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', '')
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	messages: 'list[Message]' = []
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(messages.append)
	cf.parse_line('set b="hello ${HELLO:?}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert len(messages) == 1
	assert messages[0].message == 'environment variable HELLO is empty'

	assert b.value == 'foo'
	assert c.value == 'hello '

def test_expand_undefined_env_indicate_error_with_custom_message() -> None:
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	messages: 'list[Message]' = []
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(messages.append)
	cf.parse_line('set b="hello ${HELLO:?HELLO is required}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert len(messages) == 1
	assert messages[0].message == 'HELLO is required'

	assert b.value == 'foo'
	assert c.value == 'hello '


def test_expand_defined_env_use_alternative(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', 'universe')
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:+world}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert b.value == 'hello world'
	assert c.value == 'hello universe'

def test_expand_undefined_env_use_alternative() -> None:
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:+world}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert b.value == 'hello '
	assert c.value == 'hello '


# ------- raw -------

def test_raw_vim_style() -> None:
	a = Config('a', 42, unit='')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set --raw b=%foo%')

	assert b.value == '%foo%'

def test_raw_vim_style_partly() -> None:
	a = Config('a', 42, unit='')
	b = Config('b', 'foo')
	c = Config('c', 'bar')
	d = Config('d', 'baz')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b=%a% -r c=%foo% d=%a:02X%')

	assert b.value == '42'
	assert c.value == '%foo%'
	assert d.value == '%a:02X%'

def test_raw_ranger_style() -> None:
	a = Config('a', 42, unit='')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set -r b 10%-20%')

	assert b.value == '10%-20%'


# ------- echo -------

def test__echo() -> None:
	Config('c', 42, unit='')

	cf = ConfigFile(appname='test')
	cf.parse_line('echo "c=%c:02X%"')

	messages: 'list[Message]' = []
	cf.set_ui_callback(messages.append)
	assert len(messages) == 1
	assert messages[0].message == "c=2A"
