import sys
import yaml
import pathlib
import subprocess
from typing import Optional
from dataclasses import dataclass
from rich.console import Console

console = Console()


@dataclass
class Handler:
    join_arg: str = ' && '
    _file: pathlib.Path = None
    _project: dict = None
    extension: str = None

    def __init__(self, project_file: pathlib.Path, join_arg: str = ' && ', extension: Optional[str] = None):
        super().__init__()
        self.join_arg = join_arg
        self._file = project_file
        self.extension = extension
        self._project = self.load_project()

    def load_project(self):
        # Load the project data from the YAML file
        with open(self._file, 'r', encoding='utf8') as f:
            return yaml.safe_load(f)

    def get_scripts(self):
        # Check if self._project is None
        if self._project is None:
            return {}
        # Retrieve the scripts section from the project data
        return self._project.get('scripts', {})

    def join_commands(self, commands: list[str]) -> str:
        # Join multiple commands using the join argument
        return self.join_arg.join(commands)

    def list(self):
        # List the available commands and their corresponding values
        scripts = self.get_scripts()
        if scripts:
            print('')
            console.print('available commands:', '\n', style='bold green')
            for cmd, value in scripts.items():
                if isinstance(value, list):
                    print(f'> {cmd}')
                    print(f'    {self.join_commands(value)}')
                else:
                    print(f'> {cmd}')
                    print(f'    {value}')
        else:
            console.print(
                'no commands found. please configure commands.', style='bold red')

    def run(self, cmd: str, *args: str, **kwargs):
        # Execute a command with optional arguments
        scripts = self.get_scripts()
        if cmd not in scripts:
            console.print(
                'command does not exist. please check your configuration.', style='bold red')
            return
        commands = scripts[cmd]
        if isinstance(commands, list):
            if isinstance(args, tuple):
                commands = [f'{cmd} {" ".join(args)}' for cmd in commands]
            commands = self.join_commands(commands)
        elif isinstance(commands, str):
            if isinstance(args, tuple):
                commands = f'{commands} {" ".join(args)}'
        console.print(f'> running {cmd}', style='bold green')
        print(f'> {commands}', '\n')
        try:
            subprocess.run(commands, shell=True)
        except KeyboardInterrupt:
            sys.exit(0)
