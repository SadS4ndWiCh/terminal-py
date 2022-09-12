from pathlib import Path
from typing import Protocol

class Terminal(Protocol):
	current_path: str
	history: list[str]

	@staticmethod
	def join_current_path(*paths: str) -> Path:
		...

	@staticmethod
	def get_current_folder() -> str:
		...

	@staticmethod
	def get_folder_range() -> str:
		...
	
	@staticmethod
	def get_enviroments_infos() -> dict:
		...