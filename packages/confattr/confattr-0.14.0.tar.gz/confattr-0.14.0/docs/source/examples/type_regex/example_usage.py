#!../../../../venv/bin/python3
# ------- start -------
from confattr import Config, ConfigFile
from confattr.types import Regex

class App:

	greeting = Config('greeting', Regex(r'(?i)(hello|hi)\b'), help='determine whether the user is polite or not')

	def __init__(self) -> None:
		self.config_file = ConfigFile(appname='example')
		self.config_file.set_ui_callback(print)
		self.config_file.load()

	def save(self) -> None:
		self.config_file.save()

	def main(self) -> None:
		inp = input('>>> ')
		if self.greeting.match(inp):
			print('nice to meet you')
		else:
			print('you are rude')

if __name__ == '__main__':
	a = App()
	a.main()
