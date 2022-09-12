FOREGROUND = {
	'f_black': '\033[30m',
	'f_red': '\033[31m',
	'f_green': '\033[32m',
	'f_yellow': '\033[33m',
	'f_blue': '\033[34m',
	'f_purple': '\033[35m',
	'f_cyan': '\033[36m',
	'f_white': '\033[37m',
}

BACKGROUND = {
	'b_black': '\033[40m',
	'b_red': '\033[41m',
	'b_green': '\033[42m',
	'b_yellow': '\033[43m',
	'b_blue': '\033[44m',
	'b_purple': '\033[45m',
	'b_cyan': '\033[46m',
	'b_white': '\033[47m',
}

STYLES = {
	'normal': '\033[0m',
	'bold': '\033[1m',
	'light': '\033[2m',
	'italic': '\033[3m',
	'underline': '\033[4m',
	'blink': '\033[5m',
	'reset': '\033[m'
}

COLORS = { **FOREGROUND, **BACKGROUND, **STYLES }