#!../venv/bin/pytest -s

import typing

from confattr import Config, MultiConfig, MultiDictConfig, ConfigFile, ConfigId, ParseException


def test_error_invalid_config_id() -> None:
	def check_config_id(config_id: ConfigId) -> None:
		if not config_id.endswith('car'):
			raise ParseException('only cars are supported')

	cf = ConfigFile(appname='test', check_config_id=check_config_id)
	with open(cf.get_save_path(), 'wt') as f:
		f.write('[my-bike]\n')
		f.write('[%s]\n' % Config.default_config_id)
	cf.load()

	errors = []
	cf.set_ui_callback(lambda msg: errors.append(str(msg.message)))
	assert errors == ['only cars are supported']

def test_error_set_multi_config_in_invalid_config_id() -> None:
	def check_config_id(config: 'MultiConfig[typing.Any]', config_id: ConfigId) -> None:
		if not config_id.endswith('car'):
			raise ParseException(f'{config.key} applies to cars only, not to {config_id!r}')

	MultiConfig('fuel', 'gasoline', check_config_id=check_config_id)

	cf = ConfigFile(appname='test')
	with open(cf.get_save_path(), 'wt') as f:
		f.write('''
set fuel = hydrogen

[alices-car]
set fuel = diesel

[bobs-bike]
set fuel = electricity
''')
	cf.load()

	errors = []
	cf.set_ui_callback(lambda msg: errors.append(str(msg.message)))
	assert errors == ["fuel applies to cars only, not to 'bobs-bike'"]

def test_error_set_multi_dict_config_in_invalid_config_id() -> None:
	def check_config_id(config: 'MultiConfig[typing.Any]', config_id: ConfigId) -> None:
		if not config_id.startswith('foo'):
			raise ParseException(f'invalid config id {config_id!r}')

	class Foo:

		color = MultiDictConfig('color', {'red': 242, 'green': 121, 'blue': 60}, unit='', check_config_id=check_config_id)

		def __init__(self, config_id: str) -> None:
			self.config_id = ConfigId(config_id)

	cf = ConfigFile(appname='test')
	with open(cf.get_save_path(), 'wt') as f:
		f.write('''
set color.red = 0

[foo]
set color.green = 0

[bar]
set color.blue = 0
''')
	cf.load()

	errors = []
	cf.set_ui_callback(lambda msg: errors.append(str(msg.message)))
	assert errors == ["invalid config id 'bar'"]

	foo = Foo('foo')
	assert foo.color['red']   ==   0
	assert foo.color['green'] ==   0
	assert foo.color['blue']  ==  60

	bar = Foo('bar')
	assert bar.color['red']   ==   0
	assert bar.color['green'] == 121
	assert bar.color['blue']  ==  60

	other = Foo('other')
	assert other.color['red']   ==   0
	assert other.color['green'] == 121
	assert other.color['blue']  ==  60
