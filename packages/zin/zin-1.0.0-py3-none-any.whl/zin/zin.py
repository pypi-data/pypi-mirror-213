import pathlib
from dataclasses import dataclass
from rich.console import Console
from zin import __app_name__, __version__

from .handler import Handler

console = Console()


@dataclass
class Zin:
    project_file = 'zin.yaml'
    zin_config_file: pathlib.Path = pathlib.Path('zin.yaml')
    handler: Handler = None

    def setup(self, project_file):
        self.project_file = pathlib.Path(project_file)
        try:
            if not self.project_file.exists():
                console.print(
                    f"[bold yellow]zin.yaml file not found. Please make sure the file exists in the project root directory[/bold yellow]")
                self.handler = None  # Set handler to None if project file doesn't exist
                return
            else:
                self.handler = Handler(project_file=self.project_file)
        except Exception as e:
            console.print(
                f"[bold red]An error occurred: {e}[/bold red]")
            self.handler = None # Set handler to None if project file doesn't exist

    def version(self):
        # Print the zin version
        print(f'{__app_name__.title()} {__version__}')

    def run(self, cmd: str, *args: str, **kwargs):
        # Execute a command(s)
        self.setup(self.project_file)
        if self.handler is not None:
            self.handler.run(cmd, *args, **kwargs)

    def list(self):
        # List all available commands in the config file
        self.setup(self.project_file)
        if self.handler is not None:
            self.handler.list()
