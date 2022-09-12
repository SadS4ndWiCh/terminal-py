from runpy import run_path

from src.command import Command
from src.protocols.terminal import Terminal

@Command.command('pyproject', description='Cria um projeto com python')
def create_python_project(term: Terminal, option: str, filepath: str = None):
	if (option == 'run'):
		run_path(term.join_current_path(filepath), init_globals=None)
