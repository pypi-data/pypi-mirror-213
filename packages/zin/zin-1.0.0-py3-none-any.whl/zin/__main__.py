import argparse

from .zin import Zin


class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog='zin', description='A tool for managing and running custom scripts. Streamline your command execution experience with ease.')
        self.zin = Zin()
        # Subparsers for different commands
        self.subparsers = self.parser.add_subparsers(
            dest='command', metavar='')
        # Version command
        self.version_parser = self.parser.add_argument(
            '-v', '--version', help='Show version information', action='store_true')
        # Run command
        self.run_parser = self.subparsers.add_parser(
            'run', help='Run a command')
        self.run_parser.add_argument(
            'command_name', type=str, help='Name of the command to run')
        self.run_parser.set_defaults(func=self.run_command)
        # List command
        self.list_parser = self.subparsers.add_parser(
            'list', help='List all available commands')
        self.list_parser.set_defaults(func=self.list_commands)

    def show_version(self, args):
        self.zin.version()

    def run_command(self, args):
        self.zin.run(args.command_name)

    def list_commands(self, args):
        self.zin.list()

    def main(self):
        # Parse the command-line arguments
        args = self.parser.parse_args()

        # Execute the appropriate function based on the command
        if hasattr(args, 'func'):
            args.func(args)
        elif args.version:
            self.show_version(args)
        else:
            self.parser.print_help()


def main():
    cli = CLI()
    cli.main()


if __name__ == '__main__':
    main()
