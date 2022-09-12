def parse_params(params: str):
	splitted = params.split(' ')
	parsed = []

	_open = False
	for text in splitted:
		if (text.startswith("'")):
			_open = True
			parsed.append(text.replace("'", ''))
		
		elif (_open):
			parsed[-1] = (parsed[-1] + ' ' + text).replace("'", '')

			if (text.endswith("'")):
				_open = False
		
		else:
			parsed.append(text)
	
	return parsed

def parse_instruction(instruction: str):
	cmd, *params = parse_params(instruction)

	return cmd, params

def print_table(data: list[list], gap: int = 2) -> None:
	columns_sizes = [0 for _ in range(len(data[0]))]

	for row in data:
		for idx, column in enumerate(row):
			length = len(str(column))

			if (length > columns_sizes[idx]):
				columns_sizes[idx] = length
	
	for row in data:
		for idx, column in enumerate(row):
			size = columns_sizes[idx] + gap
			print(f'{column:{size}s}', end='')
		print()