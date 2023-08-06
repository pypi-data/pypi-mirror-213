# ------- start -------
import os

class Path:

	type_name = 'path'
	help = 'The path to a file or directory'

	def __init__(self, value: str) -> None:
		self.raw = value

	def __str__(self) -> str:
		return self.raw

	def __repr__(self) -> str:
		return '%s(%r)' % (type(self).__name__, self.raw)

	def expand(self) -> str:
		return os.path.expanduser(self.raw)
