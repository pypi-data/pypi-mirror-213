#!./runmodule.sh

'''
This module contains classes and functions that :mod:`confattr` uses internally but which might be useful for other python projects, too.
'''

import re
import argparse
import inspect
import textwrap
import shlex
import functools
import enum
import typing

if typing.TYPE_CHECKING:
	from typing_extensions import Unpack, Self


# ---------- shlex quote ----------

def readable_quote(value: str) -> str:
	'''
	This function has the same goal like :func:`shlex.quote` but tries to generate better readable output.

	:param value: A value which is intended to be used as a command line argument
	:return: A POSIX compliant quoted version of :paramref:`~confattr.utils.readable_quote.value`
	'''
	out = shlex.quote(value)
	if out == value:
		return out

	if '"\'"' in out and '"' not in value:
		return '"' + value + '"'

	return out


# ---------- sorted enum ----------

@functools.total_ordering
class SortedEnum(enum.Enum):

	'''
	By default it is assumed that the values are defined in ascending order ``ONE='one'; TWO='two'; THREE='three'``.
	If you want to define them in descending order ``THREE='three'; TWO='two'; ONE='one'`` you can pass ``descending = True`` to the subclass.
	This requires Python 3.10.0a4 or newer.
	On older versions it causes a ``TypeError: __prepare__() got an unexpected keyword argument 'descending'``.
	This was fixed in `commit 6ec0adefad <https://github.com/python/cpython/commit/6ec0adefad60ec7cdec61c44baecf1dccc1461ab>`__.
	'''

	descending: bool

	@classmethod
	def __init_subclass__(cls, descending: bool = False):
		cls.descending = descending

	def __lt__(self, other: typing.Any) -> bool:
		if self.__class__ is other.__class__:
			l: 'tuple[SortedEnum, ...]' = tuple(type(self))
			if self.descending:
				left = other
				right = self
			else:
				left = self
				right = other
			return l.index(left) < l.index(right)
		return NotImplemented

	def __add__(self, other: object) -> 'Self':
		if isinstance(other, int):
			l: 'tuple[Self, ...]' = tuple(type(self))
			i = l.index(self)
			if self.descending:
				other = -other
			i += other
			if i < 0:
				i = 0
			elif i >= len(l):
				i = len(l) - 1
			return l[i]
		return NotImplemented

	def __sub__(self, other: object) -> 'Self':
		if isinstance(other, int):
			return self + (-other)
		return NotImplemented



# ---------- argparse help formatter ----------

class HelpFormatter(argparse.RawDescriptionHelpFormatter):

	'''
	A subclass of :class:`argparse.HelpFormatter` which keeps paragraphs
	separated by an empty line as separate paragraphs and
	and which does *not* merge different list items to a single line.

	Lines are wrapped to not exceed a length of :attr:`~confattr.utils.HelpFormatter.max_width` characters,
	although not strictly to prevent URLs from breaking.

	If a line ends with a double backslash this line will not be merged with the following line
	and the double backslash (and spaces directly before it) will be removed.

	As the doc string of :class:`argparse.HelpFormatter` states

		Only the name of this class is considered a public API.
		All the methods provided by the class are considered an implementation detail.

	Therefore I may be forced to change the methods' signatures if :class:`argparse.HelpFormatter` is changed.
	But I hope that I can keep the class attributes backward compatible so that you can create your own formatter class
	by subclassing this class and changing the values of the class variables.

	If you want to use this class pass it to the constructor of :class:`~confattr.utils.HelpFormatterWrapper` and use that instead.
	'''

	#: Wrap lines so that they are no longer than this number of characters.
	max_width = 70

	#: This value is assigned to :attr:`textwrap.TextWrapper.break_long_words`. This defaults to False to prevent URLs from breaking.
	break_long_words = False

	#: This value is assigned to :attr:`textwrap.TextWrapper.break_on_hyphens`. This defaults to False to prevent URLs from breaking.
	break_on_hyphens = False

	#: If a match is found this line is not merged with the following and the match is removed. This may *not* contain any capturing groups.
	regex_linebreak = re.escape(r'\\') + '(?:\n|$)'

	#: If a match is found this line is not merged with the preceeding line. This regular expression must contain exactly one capturing group. This group defines the indentation. Everything that is matched but not part of that group is removed.
	regex_list_item = '(?:^|\n)' + r'(\s*(?:[-+*!/.]|[0-9]+[.)])(?: \[[ x~]\])? )'

	def __init__(self,
		prog: str,
		indent_increment: int = 2,
		max_help_position: int = 24,
		width: 'int|None' = None,
	) -> None:
		'''
		:param prog: The name of the program
		:param width: Wrap lines so that they are no longer than this number of characters. If this value is None or bigger than :attr:`~confattr.utils.HelpFormatter.max_width` then :attr:`~confattr.utils.HelpFormatter.max_width` is used instead.
		'''
		if width is None or width >= self.max_width:
			width = self.max_width
		super().__init__(prog, indent_increment, max_help_position, width)


	# ------- override methods of parent class -------

	def _fill_text(self, text: str, width: int, indent: str) -> str:
		'''
		This method joins the lines returned by :meth:`~confattr.utils.HelpFormatter._split_lines`.

		This method is used to format text blocks such as the description.
		It is *not* used to format the help of arguments—see :meth:`~confattr.utils.HelpFormatter._split_lines` for that.
		'''
		return '\n'.join(self._split_lines(text, width, indent=indent))

	def _split_lines(self, text: str, width: int, *, indent: str = '') -> 'list[str]':
		'''
		This method cleans :paramref:`~confattr.utils.HelpFormatter._split_lines.text` with :func:`inspect.cleandoc` and
		wraps the lines with :meth:`textwrap.TextWrapper.wrap`.
		Paragraphs separated by an empty line are kept as separate paragraphs.

		This method is used to format the help of arguments and
		indirectly through :meth:`~confattr.utils.HelpFormatter._fill_text` to format text blocks such as description.

		:param text: The text to be formatted
		:param width: The maximum width of the resulting lines (Depending on the values of :attr:`~confattr.utils.HelpFormatter.break_long_words` and :attr:`~confattr.utils.HelpFormatter.break_on_hyphens` this width can be exceeded in order to not break URLs.)
		:param indent: A str to be prepended to all lines. The original :class:`argparse.HelpFormatter` does not have this parameter, I have added it so that I can use this method in :meth:`~confattr.utils.HelpFormatter._fill_text`.
		'''
		lines = []
		# The original implementation does not use cleandoc
		# it simply gets rid of all indentation and line breaks with
		# self._whitespace_matcher.sub(' ', text).strip()
		# https://github.com/python/cpython/blob/main/Lib/argparse.py
		text = inspect.cleandoc(text)
		wrapper = textwrap.TextWrapper(width=width,
			break_long_words=self.break_long_words, break_on_hyphens=self.break_on_hyphens)
		for par in re.split('\n\\s*\n', text):
			for ln in re.split(self.regex_linebreak, par):
				wrapper.initial_indent = indent
				wrapper.subsequent_indent = indent
				pre_bullet_items = re.split(self.regex_list_item, ln)
				lines.extend(wrapper.wrap(pre_bullet_items[0]))
				for i in range(1, len(pre_bullet_items), 2):
					bullet = pre_bullet_items[i]
					item = pre_bullet_items[i+1]
					add_indent = ' ' * len(bullet)
					wrapper.initial_indent = indent + bullet
					wrapper.subsequent_indent = indent + add_indent
					item = item.replace('\n'+add_indent, '\n')
					lines.extend(wrapper.wrap(item))
			lines.append('')

		lines = lines[:-1]

		return lines


if typing.TYPE_CHECKING:
	class HelpFormatterKwargs(typing.TypedDict, total=False):
		prog: str
		indent_increment: int
		max_help_position: int
		width: int


class HelpFormatterWrapper:

	'''
	The doc string of :class:`argparse.HelpFormatter` states:

	    Only the name of this class is considered a public API.
	    All the methods provided by the class are considered an implementation detail.

	This is a wrapper which tries to stay backward compatible even if :class:`argparse.HelpFormatter` changes.
	'''

	def __init__(self, formatter_class: 'type[argparse.HelpFormatter]', **kw: 'Unpack[HelpFormatterKwargs]') -> None:
		'''
		:param formatter_class: :class:`argparse.HelpFormatter` or any of it's subclasses (:class:`argparse.RawDescriptionHelpFormatter`, :class:`argparse.RawTextHelpFormatter`, :class:`argparse.ArgumentDefaultsHelpFormatter`, :class:`argparse.MetavarTypeHelpFormatter` or :class:`~confattr.utils.HelpFormatter`)
		:param prog: The name of the program
		:param indent_increment: The number of spaces by which to indent the contents of a section
		:param max_help_position: The maximal indentation of the help of arguments. If argument names + meta vars + separators are longer than this the help starts on the next line.
		:param width: Maximal number of characters per line
		'''
		kw.setdefault('prog', '')
		self.formatter = formatter_class(**kw)


	# ------- format directly -------

	def format_text(self, text: str) -> str:
		'''
		Format a text and return it immediately without adding it to :meth:`~confattr.utils.HelpFormatterWrapper.format_help`.
		'''
		return self.formatter._format_text(text)

	def format_item(self, bullet: str, text: str) -> str:
		'''
		Format a list item and return it immediately without adding it to :meth:`~confattr.utils.HelpFormatterWrapper.format_help`.
		'''
		# apply section indentation
		bullet = ' ' * self.formatter._current_indent + bullet
		width = max(self.formatter._width - self.formatter._current_indent, 11)

		# _fill_text does not distinguish between textwrap's initial_indent and subsequent_indent
		# instead I am using bullet for both and then replace the bullet with whitespace on all but the first line
		text = self.formatter._fill_text(text, width, bullet)
		pattern_bullet = '(?<=\n)' + re.escape(bullet)
		indent = ' ' * len(bullet)
		text = re.sub(pattern_bullet, indent, text)
		return text + '\n'


	# ------- input -------

	def add_start_section(self, heading: str) -> None:
		'''
		Start a new section.

		This influences the formatting of following calls to :meth:`~confattr.utils.HelpFormatterWrapper.add_text` and :meth:`~confattr.utils.HelpFormatterWrapper.add_item`.

		You can call this method again before calling :meth:`~confattr.utils.HelpFormatterWrapper.add_end_section` to create a subsection.
		'''
		self.formatter.start_section(heading)

	def add_end_section(self) -> None:
		'''
		End the last section which has been started with :meth:`~confattr.utils.HelpFormatterWrapper.add_start_section`.
		'''
		self.formatter.end_section()

	def add_text(self, text: str) -> None:
		'''
		Add some text which will be formatted when calling :meth:`~confattr.utils.HelpFormatterWrapper.format_help`.
		'''
		self.formatter.add_text(text)

	def add_start_list(self) -> None:
		'''
		Start a new list which can be filled with :meth:`~confattr.utils.HelpFormatterWrapper.add_item`.
		'''
		# nothing to do, this exists only as counter piece for add_end_list

	def add_item(self, text: str, bullet: str = '- ') -> None:
		'''
		Add a list item which will be formatted when calling :meth:`~confattr.utils.HelpFormatterWrapper.format_help`.
		A list must be started with :meth:`~confattr.utils.HelpFormatterWrapper.add_start_list` and ended with :meth:`~confattr.utils.HelpFormatterWrapper.add_end_list`.
		'''
		self.formatter._add_item(self.format_item, (bullet, text))

	def add_end_list(self) -> None:
		'''
		End a list. This must be called after the last :meth:`~confattr.utils.HelpFormatterWrapper.add_item`.
		'''
		def identity(x: str) -> str:
			return x
		self.formatter._add_item(identity, ('\n',))

	# ------- output -------

	def format_help(self) -> str:
		'''
		Format everything that has been added with :meth:`~confattr.utils.HelpFormatterWrapper.add_start_section`, :meth:`~confattr.utils.HelpFormatterWrapper.add_text` and :meth:`~confattr.utils.HelpFormatterWrapper.add_item`.
		'''
		return self.formatter.format_help()
