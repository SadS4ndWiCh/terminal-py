from os import getlogin
from datetime import datetime

from src.protocols.terminal import Terminal

from src.utils.enviroments import get_enviroments_infos
from src.utils.colors import COLORS
from src.utils.emojis import EMOJIS

def get_template_data(term: Terminal):
	now = datetime.now()

	return {
		"login": getlogin(),
		"current_folder": term.get_folder_range(1),
		"with_prev_folder": term.get_folder_range(2),
		"with_three_folder": term.get_folder_range(3),
		"path": term.current_path,
		"now": now,
		**term.get_enviroments_infos(),
		**COLORS,
		**EMOJIS
	}

