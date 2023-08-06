#!/usr/bin/env python3

import re
import copy
import abc
import enum
import typing
import builtins
from collections.abc import Iterable, Iterator, Sequence, Mapping, Callable

if typing.TYPE_CHECKING:
	from .configfile import ConfigFile
	from typing_extensions import Self

try:
	Collection = typing.Collection
except:  # pragma: no cover
	from collections.abc import Collection


TYPES_REQUIRING_UNIT = {int, float}

VALUE_TRUE = 'true'
VALUE_FALSE = 'false'

def format_primitive_value(value: object) -> str:
	if isinstance(value, enum.Enum):
		return value.name.lower().replace('_', '-')
	if isinstance(value, bool):
		return VALUE_TRUE if value else VALUE_FALSE
	return str(value)


# mypy rightfully does not allow AbstractFormatter to be declared as covariant with respect to T because
#     def format_value(self, t: AbstractFormatter[object], val: object):
#         return t.format_value(self, val)
#     ...
#     config_file.format_value(Hex(), "boom")
# would typecheck ok but crash
T = typing.TypeVar('T')

class AbstractFormatter(typing.Generic[T]):

	config_key: 'str|None' = None

	@abc.abstractmethod
	def format_value(self, config_file: 'ConfigFile', value: 'T') -> str:
		raise NotImplementedError()

	@abc.abstractmethod
	def expand_value(self, config_file: 'ConfigFile', value: 'T', format_spec: str) -> str:
		'''
		:param config_file: has e.g. the :attr:`~confattr.configfile.ConfigFile.ITEM_SEP` attribute
		:param value: The value to be formatted
		:param format_spec: A format specifier
		:return: :paramref:`~confattr.formatters.AbstractFormatter.expand_value.value` formatted according to :paramref:`~confattr.formatters.AbstractFormatter.expand_value.format_spec`
		:raises ValueError, LookupError: If :paramref:`~confattr.formatters.AbstractFormatter.expand_value.format_spec` is invalid
		'''
		raise NotImplementedError()

	@abc.abstractmethod
	def parse_value(self, config_file: 'ConfigFile', value: str) -> 'T':
		raise NotImplementedError()

	@abc.abstractmethod
	def get_description(self, config_file: 'ConfigFile') -> str:
		raise NotImplementedError()

	@abc.abstractmethod
	def get_completions(self, config_file: 'ConfigFile', start_of_line: str, start: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		raise NotImplementedError()

	@abc.abstractmethod
	def get_primitives(self) -> 'Sequence[Primitive[typing.Any]]':
		'''
		If self is a Primitive data type, return self.
		If self is a Collection, return self.item_type.
		'''
		raise NotImplementedError()

	def set_config_key(self, config_key: str) -> None:
		'''
		In order to generate a useful error message if parsing a value fails the key of the setting is required.
		This method is called by the constructor of :class:`~confattr.config.Config`.
		This method must not be called more than once.

		:raises TypeError: If :attr:`~confattr.formatters.AbstractFormatter.config_key` has already been set.
		'''
		if self.config_key:
			raise TypeError(f"config_key has already been set to {self.config_key!r}, not setting to {config_key!r}")
		self.config_key = config_key


class CopyableAbstractFormatter(AbstractFormatter[T]):

	@abc.abstractmethod
	def copy(self) -> 'Self':
		raise NotImplementedError()


class Primitive(CopyableAbstractFormatter[T]):

	PATTERN_ONE_OF = "one of {}"
	PATTERN_ALLOWED_VALUES_UNIT = "{allowed_values} (unit: {unit})"
	PATTERN_TYPE_UNIT = "{type} in {unit}"

	#: Help for data types. This is used by :meth:`~confattr.formatters.Primitive.get_help`.
	help_dict: 'dict[type[typing.Any]|Callable[..., typing.Any], str]' = {
		str : 'A text. If it contains spaces it must be wrapped in single or double quotes.',
		int : '''\
			An integer number in python 3 syntax, as decimal (e.g. 42), hexadecimal (e.g. 0x2a), octal (e.g. 0o52) or binary (e.g. 0b101010).
			Leading zeroes are not permitted to avoid confusion with python 2's syntax for octal numbers.
			It is permissible to group digits with underscores for better readability, e.g. 1_000_000.''',
		#bool,
		float : 'A floating point number in python syntax, e.g. 23, 1.414, -1e3, 3.14_15_93.',
	}


	#: If this is set it is used in :meth:`~confattr.formatters.Primitive.get_description` and the list of possible values is moved to the output of :meth:`~confattr.formatters.Primitive.get_help`.
	type_name: 'str|None'

	#: The unit of a number
	unit: 'str|None'

	#: :class:`str`, :class:`int`, :class:`float`, :class:`bool`, a subclass of :class:`enum.Enum` or any class that follows the pattern of :class:`confattr.types.AbstractType`
	type: 'type[T]|Callable[..., T]'

	#: If this is set and a value read from a config file is not contained it is considered invalid. If this is a mapping the keys are the string representations used in the config file.
	allowed_values: 'Collection[T]|dict[str, T]|None'

	def __init__(self, type: 'builtins.type[T]|Callable[..., T]', *, allowed_values: 'Collection[T]|dict[str, T]|None' = None, unit: 'str|None' = None, type_name: 'str|None' = None) -> None:
		if type in TYPES_REQUIRING_UNIT and unit is None and not isinstance(allowed_values, dict):
			raise TypeError(f"missing argument unit for {self.config_key}, pass an empty string if the number really has no unit")

		self.type = type
		self.type_name = type_name
		self.allowed_values = allowed_values
		self.unit = unit

	def copy(self) -> 'Self':
		out = copy.copy(self)
		out.config_key = None
		return out

	def format_value(self, config_file: 'ConfigFile', value: 'T') -> str:
		if isinstance(self.allowed_values, dict):
			for key, val in self.allowed_values.items():
				if val == value:
					return key
			raise ValueError('%r is not an allowed value, should be one of %s' % (value, ', '.join(repr(v) for v in self.allowed_values.values())))

		if isinstance(value, str):
			return value.replace('\n', r'\n')

		return format_primitive_value(value)

	def expand_value(self, config_file: 'ConfigFile', value: 'T', format_spec: str) -> str:
		'''
		This method simply calls the builtin :func:`format`.
		'''
		return format(value, format_spec)

	def parse_value(self, config_file: 'ConfigFile', value: str) -> 'T':
		if isinstance(self.allowed_values, dict):
			try:
				return self.allowed_values[value]
			except KeyError:
				raise ValueError(f'invalid value for {self.config_key}: {value!r} (should be {self.get_description(config_file)})')
		elif self.type is str:
			value = value.replace(r'\n', '\n')
			out = typing.cast(T, value)
		elif self.type is int:
			out = typing.cast(T, int(value, base=0))
		elif self.type is float:
			out = typing.cast(T, float(value))
		elif self.type is bool:
			if value == VALUE_TRUE:
				out = typing.cast(T, True)
			elif value == VALUE_FALSE:
				out = typing.cast(T, False)
			else:
				raise ValueError(f'invalid value for {self.config_key}: {value!r} (should be {self.get_description(config_file)})')
		elif isinstance(self.type, type) and issubclass(self.type, enum.Enum):
			for i in self.type:
				enum_item = typing.cast(T, i)
				if self.format_value(config_file, enum_item) == value:
					out = enum_item
					break
			else:
				raise ValueError(f'invalid value for {self.config_key}: {value!r} (should be {self.get_description(config_file)})')
		else:
			try:
				out = self.type(value)  # type: ignore [call-arg]
			except Exception as e:
				raise ValueError(f'invalid value for {self.config_key}: {value!r} ({e})')

		if self.allowed_values is not None and out not in self.allowed_values:
			raise ValueError(f'invalid value for {self.config_key}: {value!r} (should be {self.get_description(config_file)})')
		return out


	def get_description(self, config_file: 'ConfigFile', *, plural: bool = False, article: bool = True) -> str:
		'''
		:param config_file: May contain some additional information how to format the allowed values.
		:param plural: Whether the return value should be a plural form.
		:param article: Whether the return value is supposed to be formatted with :meth:`~confattr.formatters.Primitive.format_indefinite_singular_article` (if :meth:`~confattr.formatters.Primitive.get_type_name` is used) or :attr:`~confattr.formatters.Primitive.PATTERN_ONE_OF` (if :meth:`~confattr.formatters.Primitive.get_allowed_values` returns an empty sequence). This is assumed to be false if :paramref:`~confattr.formatters.Primitive.get_description.plural` is true.
		:return: A short description which is displayed in the help/comment for each setting explaining what kind of value is expected.
		         In the easiest case this is just a list of allowed value, e.g. "one of true, false".
		         If :attr:`~confattr.formatters.Primitive.type_name` has been passed to the constructor this is used instead and the list of possible values is moved to the output of :meth:`~confattr.formatters.Primitive.get_help`.
		         If a unit is specified it is included, e.g. "an int in km/h".

		You can customize the return value of this method by overriding :meth:`~confattr.formatters.Primitive.get_type_name`, :meth:`~confattr.formatters.Primitive.join` or :meth:`~confattr.formatters.Primitive.format_indefinite_singular_article`
		or by changing the value of :attr:`~confattr.formatters.Primitive.PATTERN_ONE_OF`, :attr:`~confattr.formatters.Primitive.PATTERN_ALLOWED_VALUES_UNIT` or :attr:`~confattr.formatters.Primitive.PATTERN_TYPE_UNIT`.
		'''
		if plural:
			article = False

		if not self.type_name:
			out = self.format_allowed_values(config_file, article=article)
			if out:
				return out

		out = self.get_type_name()
		if self.unit:
			out = self.PATTERN_TYPE_UNIT.format(type=out, unit=self.unit)
		if article:
			out = self.format_indefinite_singular_article(out)
		return out

	def format_allowed_values(self, config_file: 'ConfigFile', *, article: bool = True) -> 'str|None':
		allowed_values = self.get_allowed_values()
		if not allowed_values:
			return None

		out = self.join(self.format_value(config_file, v) for v in allowed_values)
		if article:
			out = self.PATTERN_ONE_OF.format(out)
		if self.unit:
			out = self.PATTERN_ALLOWED_VALUES_UNIT.format(allowed_values=out, unit=self.unit)
		return out

	def get_type_name(self) -> str:
		'''
		Return the name of this type (without :attr:`~confattr.formatters.Primitive.unit` or :attr:`~confattr.formatters.Primitive.allowed_values`).
		This can be used in :meth:`~confattr.formatters.Primitive.get_description` if the type can have more than just a couple of values.
		If that is the case a help should be provided by :meth:`~confattr.formatters.Primitive.get_help`.

		:return: :paramref:`~confattr.formatters.Primitive.type_name` if it has been passed to the constructor, the value of an attribute of :attr:`~confattr.formatters.Primitive.type` called ``type_name`` if existing or the lower case name of the class stored in :attr:`~confattr.formatters.Primitive.type` otherwise
		'''
		if self.type_name:
			return self.type_name
		return getattr(self.type, 'type_name', self.type.__name__.lower())

	def join(self, names: 'Iterable[str]') -> str:
		'''
		Join several values which have already been formatted with :meth:`~confattr.formatters.Primitive.format_value`.
		'''
		return ', '.join(names)

	def format_indefinite_singular_article(self, type_name: str) -> str:
		'''
		Getting the article right is not so easy, so a user can specify the correct article with a str attribute called ``type_article``.
		Alternatively this method can be overridden.
		This also gives the possibility to omit the article.
		https://en.wiktionary.org/wiki/Appendix:English_articles#Indefinite_singular_articles

		This is used in :meth:`~confattr.formatters.Primitive.get_description`.
		'''
		if hasattr(self.type, 'type_article'):
			article = getattr(self.type, 'type_article')
			if not article:
				return type_name
			assert isinstance(article, str)
			return article + ' ' + type_name
		if type_name[0].lower() in 'aeio':
			return 'an ' + type_name
		return 'a ' + type_name


	def get_help(self, config_file: 'ConfigFile') -> 'str|None':
		'''
		The help for the generic data type, independent of the unit.
		This is displayed once at the top of the help or the config file (if one or more settings use this type).

		For example the help for an int might be:

			An integer number in python 3 syntax, as decimal (e.g. 42), hexadecimal (e.g. 0x2a), octal (e.g. 0o52) or binary (e.g. 0b101010).
			Leading zeroes are not permitted to avoid confusion with python 2's syntax for octal numbers.
			It is permissible to group digits with underscores for better readability, e.g. 1_000_000.

		Return None if (and only if) :meth:`~confattr.formatters.Primitive.get_description` returns a simple list of all possible values and not :meth:`~confattr.formatters.Primitive.get_type_name`.

		:return: The corresponding value in :attr:`~confattr.formatters.Primitive.help_dict`, the value of an attribute called ``help`` on the :attr:`~confattr.formatters.Primitive.type` or None if the return value of :meth:`~confattr.formatters.Primitive.get_allowed_values` is empty.
		:raises TypeError: If the ``help`` attribute is not a str. If you have no influence over this attribute you can avoid checking it by adding a corresponding value to :attr:`~confattr.formatters.Primitive.help_dict`.
		:raises NotImplementedError: If there is no help or list of allowed values. If this is raised add a ``help`` attribute to the class or a value for it in :attr:`~confattr.formatters.Primitive.help_dict`.
		'''

		if self.type_name:
			allowed_values = self.format_allowed_values(config_file)
			if not allowed_values:
				raise NotImplementedError("used 'type_name' without 'allowed_values', please override 'get_help'")
			return allowed_values[:1].upper() + allowed_values[1:]

		if self.type in self.help_dict:
			return self.help_dict[self.type]
		elif hasattr(self.type, 'help'):
			out = getattr(self.type, 'help')
			if not isinstance(out, str):
				raise TypeError(f"help attribute of {self.type.__name__!r} has invalid type {type(out).__name__!r}, if you cannot change that attribute please add an entry in Primitive.help_dict")
			return out
		elif self.get_allowed_values():
			return None
		else:
			raise NotImplementedError('No help for type %s' % self.get_type_name())


	def get_completions(self, config_file: 'ConfigFile', start_of_line: str, start: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		completions = [config_file.quote(config_file.format_any_value(self, val)) for val in self.get_allowed_values()]
		completions = [v for v in completions if v.startswith(start)]
		return start_of_line, completions, end_of_line

	def get_allowed_values(self) -> 'Collection[T]':
		if isinstance(self.allowed_values, dict):
			return self.allowed_values.values()
		if self.allowed_values:
			return self.allowed_values
		if self.type is bool:
			return (typing.cast(T, True), typing.cast(T, False))
		if isinstance(self.type, type) and issubclass(self.type, enum.Enum):
			return self.type
		return ()

	def get_primitives(self) -> 'tuple[Self]':
		return (self,)

class Hex(Primitive[int]):

	def __init__(self, *, allowed_values: 'Collection[int]|None' = None) -> None:
		super().__init__(int, allowed_values=allowed_values, unit='')

	def format_value(self, config_file: 'ConfigFile', value: int) -> str:
		return '%X' % value

	def parse_value(self, config_file: 'ConfigFile', value: str) -> int:
		return int(value, base=16)

	def get_description(self, config_file: 'ConfigFile', *, plural: bool = False, article: bool = True) -> str:
		out = 'hexadecimal number'
		if plural:
			out += 's'
		elif article:
			out = 'a ' + out
		return out

	def get_help(self, config_file: 'ConfigFile') -> None:
		return None


class AbstractCollection(AbstractFormatter[Collection[T]]):

	def __init__(self, item_type: 'Primitive[T]') -> None:
		self.item_type = item_type

	def split_values(self, config_file: 'ConfigFile', values: str) -> 'Iterable[str]':
		return values.split(config_file.ITEM_SEP)

	def get_completions(self, config_file: 'ConfigFile', start_of_line: str, start: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if config_file.ITEM_SEP in start:
			first, start = start.rsplit(config_file.ITEM_SEP, 1)
			start_of_line += first + config_file.ITEM_SEP
		return self.item_type.get_completions(config_file, start_of_line, start, end_of_line)

	def get_primitives(self) -> 'tuple[Primitive[T]]':
		return (self.item_type,)

	def set_config_key(self, config_key: str) -> None:
		super().set_config_key(config_key)
		self.item_type.set_config_key(config_key)


	# ------- expand ------

	def expand_value(self, config_file: 'ConfigFile', values: 'Collection[T]', format_spec: str) -> str:
		'''
		:paramref:`~confattr.formatters.AbstractCollection.expand_value.format_spec` supports the following features:

		- Filter out some values, e.g. ``-foo,bar`` expands to all items except for ``foo`` and ``bar``, it is no error if ``foo`` or ``bar`` are not contained
		- Get the length, ``len`` expands to the number of items
		- Get extreme values, ``min`` expands to the smallest item and ``max`` expands to the biggest item, raises :class:`TypeError` if the items are not comparable
		
		To any of the above you can append another format_spec after a colon to specify how to format the items/the length.
		'''
		m = re.match(r'(-(?P<exclude>[^[:]*)|(?P<func>[^[:]*))(:(?P<format_spec>.*))?$', format_spec)
		if m is None:
			raise ValueError('Invalid format_spec for collection: %r' % format_spec)

		format_spec = m.group('format_spec') or ''
		func = m.group('func')
		if func == 'len':
			return self.expand_length(config_file, values, format_spec)
		elif func:
			return self.expand_min_max(config_file, values, func, format_spec)

		exclude = m.group('exclude')
		if exclude:
			return self.expand_exclude_items(config_file, values, exclude, format_spec)

		return self.expand_parsed_items(config_file, values, format_spec)

	def expand_length(self, config_file: 'ConfigFile', values: 'Collection[T]', int_format_spec: str) -> str:
		return format(len(values), int_format_spec)

	def expand_min_max(self, config_file: 'ConfigFile', values: 'Collection[T]', func: str, item_format_spec: str) -> str:
		if func == 'min':
			v = min(values)  # type: ignore [type-var]  # The TypeError is caught in ConfigFile.expand_config_match
		elif func == 'max':
			v = max(values)  # type: ignore [type-var]  # The TypeError is caught in ConfigFile.expand_config_match
		else:
			raise ValueError(f'Invalid format_spec for collection: {func!r}')

		return self.expand_parsed_items(config_file, [v], item_format_spec)

	def expand_exclude_items(self, config_file: 'ConfigFile', values: 'Collection[T]', items_to_be_excluded: str, item_format_spec: str) -> str:
		exclude = {self.item_type.parse_value(config_file, item) for item in items_to_be_excluded.split(',')}
		out = [v for v in values if v not in exclude]
		return self.expand_parsed_items(config_file, out, item_format_spec)

	def expand_parsed_items(self, config_file: 'ConfigFile', values: 'Collection[T]', item_format_spec: str) -> str:
		if not item_format_spec:
			return self.format_value(config_file, values)
		return config_file.ITEM_SEP.join(format(v, item_format_spec) for v in values)

class List(AbstractCollection[T]):

	def get_description(self, config_file: 'ConfigFile') -> str:
		return 'a comma separated list of ' + self.item_type.get_description(config_file, plural=True)

	def format_value(self, config_file: 'ConfigFile', values: 'Collection[T]') -> str:
		return config_file.ITEM_SEP.join(config_file.format_any_value(self.item_type, i) for i in values)

	def expand_value(self, config_file: 'ConfigFile', values: 'Sequence[T]', format_spec: str) -> str:  # type: ignore [override]  # supertype defines the argument type as "Collection[T]", yes because type vars depending on other type vars is not supported yet https://github.com/python/typing/issues/548
		'''
		:paramref:`~confattr.formatters.List.expand_value.format_spec` supports all features inherited from :meth:`AbstractCollection.expand_value() <confattr.formatters.AbstractCollection.expand_value>` as well as the following:

		- Access a single item, e.g. ``[0]`` expands to the first item, ``[-1]`` expands to the last item [1]
		- Access several items, e.g. ``[0,2,5]`` expands to the items at index 0, 2 and 5, if the list is not that long an :class:`IndexError` is raised
		- Access a slice of items, e.g. ``[:3]`` expands to the first three items or to as many items as the list is long if the list is not that long [1]
		- Access a slice of items with a step, e.g. ``[::-1]`` expands to all items in reverse order [1]

		To any of the above you can append another format_spec after a colon to specify how to format the items.

		[1] For more information see the `common slicing operations of sequences <https://docs.python.org/3/library/stdtypes.html#common-sequence-operations>`__.
		'''
		m = re.match(r'(\[(?P<indices>[^]]+)\])(:(?P<format_spec>.*))?$', format_spec)
		if m is None:
			return super().expand_value(config_file, values, format_spec)

		format_spec = m.group('format_spec') or ''
		indices = m.group('indices')
		assert isinstance(indices, str)
		return self.expand_items(config_file, values, indices, format_spec)

	def expand_items(self, config_file: 'ConfigFile', values: 'Sequence[T]', indices: str, item_format_spec: str) -> str:
		out = [v for sl in self.parse_slices(indices) for v in values[sl]]
		return self.expand_parsed_items(config_file, out, item_format_spec)

	def parse_slices(self, indices: str) -> 'Iterator[slice]':
		for s in indices.split(','):
			yield self.parse_slice(s)

	def parse_slice(self, s: str) -> 'slice':
		sl = [int(i) if i else None for i in s.split(':')]
		if len(sl) == 1 and isinstance(sl[0], int):
			i = sl[0]
			return slice(i, i+1)
		return slice(*sl)

	def parse_value(self, config_file: 'ConfigFile', values: str) -> 'list[T]':
		return [self.item_type.parse_value(config_file, i) for i in self.split_values(config_file, values)]

class Set(AbstractCollection[T]):

	def get_description(self, config_file: 'ConfigFile') -> str:
		return 'a comma separated set of ' + self.item_type.get_description(config_file, plural=True)

	def format_value(self, config_file: 'ConfigFile', values: 'Collection[T]') -> str:
		try:
			sorted_values = sorted(values)  # type: ignore [type-var]  # values may be not comparable but that's what the try/except is there for
		except TypeError:
			return config_file.ITEM_SEP.join(sorted(config_file.format_any_value(self.item_type, i) for i in values))

		return config_file.ITEM_SEP.join(config_file.format_any_value(self.item_type, i) for i in sorted_values)

	def parse_value(self, config_file: 'ConfigFile', values: str) -> 'set[T]':
		return {self.item_type.parse_value(config_file, i) for i in self.split_values(config_file, values)}


T_key = typing.TypeVar('T_key')
T_val = typing.TypeVar('T_val')
class Dict(AbstractFormatter['dict[T_key, T_val]']):

	def __init__(self, key_type: 'Primitive[T_key]', value_type: 'Primitive[T_val]') -> None:
		self.key_type = key_type
		self.value_type = value_type

	def get_description(self, config_file: 'ConfigFile') -> str:
		return 'a dict of %s:%s' % (self.key_type.get_description(config_file, article=False), self.value_type.get_description(config_file, article=False))

	def format_value(self, config_file: 'ConfigFile', values: 'Mapping[T_key, T_val]') -> str:
		return config_file.ITEM_SEP.join(config_file.format_any_value(self.key_type, key) + config_file.KEY_SEP + config_file.format_any_value(self.value_type, val) for key, val in values.items())

	def parse_value(self, config_file: 'ConfigFile', values: str) -> 'dict[T_key, T_val]':
		return dict(self.parse_item(config_file, i) for i in self.split_values(config_file, values))

	def split_values(self, config_file: 'ConfigFile', values: str) -> 'Iterable[str]':
		return values.split(config_file.ITEM_SEP)

	def parse_item(self, config_file: 'ConfigFile', item: str) -> 'tuple[T_key, T_val]':
		key_name, val_name = item.split(config_file.KEY_SEP, 1)
		key = self.key_type.parse_value(config_file, key_name)
		val = self.value_type.parse_value(config_file, val_name)
		return key, val

	def get_primitives(self) -> 'tuple[Primitive[T_key], Primitive[T_val]]':
		return (self.key_type, self.value_type)

	def get_completions(self, config_file: 'ConfigFile', start_of_line: str, start: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if config_file.ITEM_SEP in start:
			first, start = start.rsplit(config_file.ITEM_SEP, 1)
			start_of_line += first + config_file.ITEM_SEP
		if config_file.KEY_SEP in start:
			first, start = start.rsplit(config_file.KEY_SEP, 1)
			start_of_line += first + config_file.KEY_SEP
			return self.value_type.get_completions(config_file, start_of_line, start, end_of_line)

		return self.key_type.get_completions(config_file, start_of_line, start, end_of_line)

	def expand_value(self, config_file: 'ConfigFile', values: 'Mapping[T_key, T_val]', format_spec: str) -> str:
		'''
		:paramref:`~confattr.formatters.Dict.expand_value.format_spec` supports the following features:

		- Get a single value, e.g. ``[key1]`` expands to the value corresponding to ``key1``, a :class:`KeyError` is raised if ``key1`` is not contained in the dict
		- Get a single value or a default value, e.g. ``[key1|default]`` expands to the value corresponding to ``key1`` or to ``default`` if ``key1`` is not contained
		- Get values with their corresponding keys, e.g. ``{key1,key2}`` expands to ``key1:val1,key2:val2``, if a key is not contained it is skipped
		- Filter out elements, e.g. ``{^key1}`` expands to all ``key:val`` pairs except for ``key1``
		- Get the length, ``len`` expands to the number of items

		To any of the above you can append another format_spec after a colon to specify how to format the items/the length.
		'''
		m = re.match(r'(\[(?P<key>[^]|]+)(\|(?P<default>[^]]+))?\]|\{\^(?P<filter>[^}]+)\}|\{(?P<select>[^}]*)\}|(?P<func>[^[{:]+))(:(?P<format_spec>.*))?$', format_spec)
		if m is None:
			raise ValueError('Invalid format_spec for dict: %r' % format_spec)

		item_format_spec = m.group('format_spec') or ''

		key = m.group('key')
		if key:
			default = m.group('default')
			return self.expand_single_value(config_file, values, key, default, item_format_spec)

		keys_filter = m.group('filter')
		if keys_filter:
			return self.expand_filter(config_file, values, keys_filter, item_format_spec)

		keys_select = m.group('select')
		if keys_select:
			return self.expand_select(config_file, values, keys_select, item_format_spec)

		func = m.group('func')
		if func == 'len':
			return self.expand_length(config_file, values, item_format_spec)

		raise ValueError('Invalid format_spec for dict: %r' % format_spec)

	def expand_single_value(self, config_file: 'ConfigFile', values: 'Mapping[T_key, T_val]', key: str, default: 'str|None', item_format_spec: str) -> str:
		'''
		Is called by :meth:`~confattr.formatters.Dict.expand_value` if :paramref:`~confattr.formatters.Dict.expand_value.format_spec` has the pattern ``[key]`` or ``[key|default]``.
		'''
		parsed_key = self.key_type.parse_value(config_file, key)
		try:
			v = values[parsed_key]
		except KeyError:
			if default is not None:
				return default
			# The message of a KeyError is the repr of the missing key, nothing more.
			# Therefore I am raising a new exception with a more descriptive message.
			# I am not using KeyError because that takes the repr of the argument.
			raise LookupError(f"key {key!r} is not contained in {self.config_key!r}")

		if not item_format_spec:
			return self.value_type.format_value(config_file, v)
		return format(v, item_format_spec)

	def expand_filter(self, config_file: 'ConfigFile', values: 'Mapping[T_key, T_val]', keys_filter: str, item_format_spec: str) -> str:
		'''
		Is called by :meth:`~confattr.formatters.Dict.expand_value` if :paramref:`~confattr.formatters.Dict.expand_value.format_spec` has the pattern ``{^key1,key2}``.
		'''
		parsed_filter_keys = {self.key_type.parse_value(config_file, key) for key in keys_filter.split(',')}
		values = {k:v for k,v in values.items() if k not in parsed_filter_keys}
		return self.expand_selected(config_file, values, item_format_spec)

	def expand_select(self, config_file: 'ConfigFile', values: 'Mapping[T_key, T_val]', keys_select: str, item_format_spec: str) -> str:
		'''
		Is called by :meth:`~confattr.formatters.Dict.expand_value` if :paramref:`~confattr.formatters.Dict.expand_value.format_spec` has the pattern ``{key1,key2}``.
		'''
		parsed_select_keys = {self.key_type.parse_value(config_file, key) for key in keys_select.split(',')}
		values = {k:v for k,v in values.items() if k in parsed_select_keys}
		return self.expand_selected(config_file, values, item_format_spec)

	def expand_selected(self, config_file: 'ConfigFile', values: 'Mapping[T_key, T_val]', item_format_spec: str) -> str:
		'''
		Is called by :meth:`~confattr.formatters.Dict.expand_filter` and :meth:`~confattr.formatters.Dict.expand_select` to do the formatting of the filtered/selected values
		'''
		if not item_format_spec:
			return self.format_value(config_file, values)
		return config_file.ITEM_SEP.join(self.key_type.format_value(config_file, k) + config_file.KEY_SEP + format(v, item_format_spec) for k, v in values.items())

	def expand_length(self, config_file: 'ConfigFile', values: 'Collection[T]', int_format_spec: str) -> str:
		'''
		Is called by :meth:`~confattr.formatters.Dict.expand_value` if :paramref:`~confattr.formatters.Dict.expand_value.format_spec` is ``len``.
		'''
		return format(len(values), int_format_spec)
