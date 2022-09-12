import os
from pathlib import Path

from src.command import Command
from src.protocols.terminal import Terminal
from src.utils.decorators import try_wrapper

from src.utils.formatting import print_table

@Command.command('cd', description='Navegar entre pastas')
@try_wrapper("Esse diretório não existe")
def change_directory(term: Terminal, directory: str):
	dirs = ['.', '..', *os.listdir(term.current_path)]
	if (directory not in dirs): raise Exception

	term.current_path = term.join_current_path(directory).resolve().absolute()

@Command.command('pwd', description='Mostra o caminho da pasta atual')
def show_current_folder_path(term: Terminal):
	print(term.current_path)

@Command.command('ls', description='Mostrar os arquivos e pastas do diretório atual')
def list_directory(term: Terminal, path: str = './'):
	directory = map(lambda f: Path(f), os.listdir(term.join_current_path(path).resolve()))
	for f in directory:
		if ('.' not in str(f)[1:]):
			print(str(f) + '/', end='  ')
		else:
			print(f, end='  ')
	
	print()

@Command.command('mkdir', description='Criar um novo diretório')
@try_wrapper()
def create_directory(term: Terminal, directory_name: str):
	os.mkdir(term.join_current_path(directory_name))

@Command.command('rmdir', description='Remover um diretório existente')
@try_wrapper()
def remove_directory(term: Terminal, directory_name: str):
	os.removedirs(term.join_current_path(directory_name))

@Command.command('touch', description='Criar um novo arquivo')
@try_wrapper()
def create_file(term: Terminal, filename: str):
	with open(term.join_current_path(filename), 'w') as f:
		...

@Command.command('rm', description='Remover um arquivo existente')
@try_wrapper()
def remove_file(term: Terminal, filename: str):
	os.remove(term.join_current_path(filename))

@Command.command('cat', description='Mostrar o conteúdo de um arquivo')
@try_wrapper()
def read_file_content(term: Terminal, filename: str):
	with open(term.join_current_path(filename), 'r', encoding='utf-8') as f:
		print(''.join(f.readlines()).replace('\t', '  '))

@Command.command('exit', description='Sair do explorador de arquivos')
def exit_from_explorer(term: Terminal):
	exit()

@Command.command('clear', description='Limpar o explorador de arquivos')
def clear_terminal(term: Terminal):
	os.system('clear')

@Command.command('whoami', description='Mostra o nome do usuário do sistema')
def show_system_username(term: Terminal):
	print(os.getlogin())

@Command.command('echo', description='Escreve um texto no terminal ou em um arquivo')
def echo_text(term: Terminal, *args):
	if ('>' in args):
		idx = args.index('>')
		text = ' '.join(args[:idx])
		filename = args[-1]
		with open(filename.strip(), 'a+', encoding='utf-8') as f:
			f.write(text.strip() + '\n')
	
	else:
		print(' '.join(args).strip())

@Command.command('history', description='Mostra o histórico de comandos')
def show_command_history(term: Terminal):
	for idx, instruction in enumerate(term.history):
		print(f'{idx+1:>5} {instruction}')

@Command.command('help', description='Listagem dos comandos e suas descrições')
def help_command(term: Terminal, command_name: str = None):
	if (command_name != None):
		command = Command.get_command(command_name)

		if (command == None): return print(f'Não existe um comando com o nome {command_name!r}')

		print(f'-----| {command_name} |-----')
		print(command.description)
		print('|-----------------------------|')
		
		return

	all_commands = Command.get_all_commands()

	print('-----| Lista de Comandos |-----')
	commands = list(map(lambda cmd: [cmd.name, cmd.description], all_commands.values()))
	print_table(commands)
	print('|-----------------------------|')

@Command.command('invoke', description='Envoca e executa um comando', invokable=False)
def invoke_command(term: Terminal, command_name: str, *args, **kwargs):
	success = Command.invoke(command_name, *args, **kwargs)
	if (not success): print('Não foi possível envocar esse comando')

@Command.command('test', description='Comando para testar as entradas de parâmetros')
def test_command(term: Terminal, *args, **kwargs):
	print(args, kwargs)