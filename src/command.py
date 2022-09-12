from typing import Any

from src.protocols.terminal import Terminal

class Command:
	commands: dict[str, 'Command'] = {}
	terminal: Terminal = None

	@classmethod
	def command(cls: 'Command', command_name: str, *, description: str = None, **kwargs):
		def f(func: callable):
			Command.commands[command_name] = cls(command_name, description, func=func, **kwargs)

			def wrapper(*args, **kwargs):
				return func(*args, **kwargs)

			return wrapper

		return f
	
	@staticmethod
	def set_terminal(terminal):
		Command.terminal = terminal

	@staticmethod
	def get_all_commands(): return Command.commands

	@staticmethod
	def get_command(command_name: str) -> 'Command':
		return Command.commands.get(command_name, None)

	@staticmethod
	def invoke(command_name: str, *args, **kwargs) -> bool:
		command = Command.get_command(command_name)
		if (command == None or not command.invokable): return False

		command.execute(Command.terminal, *args, **kwargs)
		return True

	""" ------------------------------------------- """

	def __init__(
		self,
		command_name: str,
		description: str,
		func: callable,
		*,
		invokable: bool = True
	) -> None:
		self.name = command_name
		self.description = description
		self.func = func

		self.invokable = invokable
	
	def execute(self, *args, **kwargs) -> Any:
		return self.func(*args, **kwargs)