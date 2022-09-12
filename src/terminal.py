import json
from pathlib import Path
from runpy import run_path
from os import getcwd, listdir

from src.command import Command

from src.utils.formatting import parse_instruction
from src.utils.template import get_template_data
from src.utils.enviroments import get_enviroment_type

class Terminal:
	current_path: Path = Path(getcwd())
	envs: dict[str, Path] = []
	configs: dict = None
	history: list[str] = []
	
	@staticmethod
	def join_current_path(*paths: str):
		return Path(Terminal.current_path.joinpath(*paths))
	
	@staticmethod
	def get_folder_range(folder_range: int):
		return '/'.join(str(Terminal.current_path.absolute()).split("\\")[-folder_range:])
	
	@staticmethod
	def add_to_history(instruction: str):
		Terminal.history.append(instruction)
		if (len(Terminal.history) > Terminal.configs['history_limit']):
			Terminal.history = Terminal.history[1:]

	@staticmethod
	def render():
		Terminal.envs = get_enviroment_type(Terminal.current_path, {})

		theme_blocks = Terminal.configs['theme']['blocks']
		for block in theme_blocks:
			block_env = block.get('enviroment', 'None')

			if (not block_env == 'None' and not block_env in Terminal.envs): continue

			content = block['content'].format(**get_template_data(Terminal))

			if (block['newline']): print()
			if (block['type'] == 'header'):
				print(content, end=' ')
			elif (block['type'] == 'input'):
				instruction = input(content + ' ')
				Terminal.add_to_history(instruction)

				cmd_name, params = parse_instruction(instruction)

				success = Command.invoke(cmd_name, *params)
				if (not success): print('Não foi possível envocar esse comando')

	@staticmethod
	def load_configs():
		Terminal.configs = json.load(open('src/terminal.config.json', 'r', encoding='utf-8'))

	@staticmethod
	def load_commands():
		for filename in listdir('src/commands/'):
			if (filename.endswith('.py') and not filename.startswith('_')):
				run_path(f'src/commands/{filename}', init_globals=globals())

	@staticmethod
	def setup():
		Terminal.load_configs()
		Terminal.load_commands()

	@staticmethod
	def run():
		Terminal.setup()

		while (True):
			Terminal.render()

Command.set_terminal(Terminal)