# ------- start -------
import re
from collections.abc import Callable


Regex: 'Callable[[str], re.Pattern[str]]'
class Regex:  # type: ignore [no-redef]

	type_name = 'regular expression'
	help = '''
	A regular expression in python syntax.
	You can specify flags by starting the regular expression with `(?aiLmsux)`.
	https://docs.python.org/3/library/re.html#regular-expression-syntax
	'''

	def __init__(self, pattern: str) -> None:
		self._compiled_pattern: 're.Pattern[str]' = re.compile(pattern)

	def __getattr__(self, attr: str) -> object:
		return getattr(self._compiled_pattern, attr)

	def __str__(self) -> str:
		return self._compiled_pattern.pattern

	def __repr__(self) -> str:
		return f'{type(self).__name__}({self._compiled_pattern.pattern!r})'
