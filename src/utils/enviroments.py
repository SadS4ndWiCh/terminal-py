import json
from enum import Enum
from os import listdir
from pathlib import Path
from configparser import ConfigParser

from src.protocols.terminal import Terminal

class EnviromentsFile(Enum):
  python = 'venv'
  git = '.git'
  nodejs = 'package.json'

class EnviromentsData(Enum):
  python = 'pyversion'
  git = 'gitbranch'
  nodejs = 'nodeversion'

def get_enviroment_type(path: Path | str, found_envs={}):
  archives_envs = {
    EnviromentsFile.python.value: EnviromentsFile.python.name,
    EnviromentsFile.git.value: EnviromentsFile.git.name,
    EnviromentsFile.nodejs.value: EnviromentsFile.nodejs.name,
  }

  directory = listdir(path)
  for arch in directory:
    if (arch in archives_envs):
      found_envs[archives_envs[arch]] = path

  if (not path == path.home()):
    return get_enviroment_type(path.joinpath('..').resolve(), found_envs)
  
  return found_envs

def get_nodejs_package_version(path: Path | str):
  if (path == None or not 'package.json' in listdir(path)): return

  package = json.load(open(path.joinpath('package.json'), 'r', encoding='utf-8'))
  return package.get('version', '0.0.0')

def get_git_branch(path: Path | str):
  if (path == None or not '.git' in listdir(path)): return

  with open(path.joinpath('.git/HEAD'), 'r', encoding='utf-8') as f:
    branch = f.readline().replace('ref: refs/heads', '').replace('\n', '')
  
  return branch

def get_venv_version(path: Path | str):
  if (path == None or not 'venv' in listdir(path)): return

  with open(path.joinpath('venv/pyvenv.cfg'), 'r') as f:
    config_string = '[dummy_section]\n' + f.read()

  config = ConfigParser()
  config.read_string(config_string)

  return config.get('dummy_section', 'version')

# --------------------------------------------------------

@staticmethod
def get_enviroments_infos(term: Terminal):
  envs_funcs = {
    'python': [get_venv_version, EnviromentsData.python.value],
    'git': [get_git_branch, EnviromentsData.git.value],
    'nodejs': [get_nodejs_package_version, EnviromentsData.nodejs.value],
  }

  datas = {}

  for env, path in term.envs.items():
    if (env in envs_funcs):
      datas[envs_funcs[env][1]] = envs_funcs[env][0](path)
		
  return datas