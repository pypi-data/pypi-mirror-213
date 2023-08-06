#!../../../../venv/bin/python3

# ------- start -------
from confattr import Config, ConfigFile
from confattr.types import SubprocessCommandWithAlternatives as Command

class App:

	editor = Config('editor', Command.editor(visual=False),
	                help="The editor to be used when opening the config file")

	def __init__(self) -> None:
		self.config_file = ConfigFile(appname='example-app')
		self.config_file.load()

	def edit_config(self) -> None:
		self.editor \
			.replace(Command.WC_FILE_NAME, self.config_file.save(if_not_existing=True)) \
			.run(context=None)

if __name__ == '__main__':
	app = App()
	app.edit_config()
