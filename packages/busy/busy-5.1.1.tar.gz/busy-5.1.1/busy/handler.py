# The Handler is the core control class for a single execution of the busy
# program. It's called when busy is run, and there are some functions to get
# things configured and started. Then one Handler is instantiated. This is the
# only place that imports the UI, Command, and Root classes. So the handler
# instance is passed around, and other classes can access what they need from
# there. Keeping the imports in one place allows the class families to be more
# modular.
#
# A Handler instance provides the following properties. For the most part, these
# properties are how commands access other class families. Remember that the
# Namespace from the Handler is the original Namespace, so use the one passed in
# to the execute() method of the Command for actual usage in an interactive UI.


import sys
from argparse import ArgumentParser
from pathlib import Path
from sys import argv

from busy.command.command import Command
from busy.storage.file_storage import FileStorage
from busy.ui.ui import UI, UserCancelError
from busy.util.python_version import confirm_python_version

PYTHON_VERSION = (3, 6, 5)


def main(*args):
    """Start everything from the command line

    args - optional entry point for testing
    """
    args = args if args else argv[1:]
    confirm_python_version(PYTHON_VERSION)
    parser = get_parser()
    namespace = parser.parse_args(args)
    try:
        handler = Handler(namespace)
        handler.execute()
    except (RuntimeError, ValueError) as error:
        print(f"Error: {str(error)}")


def get_parser():
    """Return the CLI parser"""
    parser = ArgumentParser(prog='busy')
    parser.add_argument('--root', action='store',
                        help='file system path to busy data',
                        default=None)
    subparsers = parser.add_subparsers(dest='command')
    for command in Command.family_members('name'):
        key = command.get_member_attr('key')
        aliases = [key] if key else []
        subparser = subparsers.add_parser(command.name, aliases=aliases)
        command.set_parser(subparser)
    return parser


class Handler():

    def __init__(self, namespace):
        """
        namespace - ArgParse Namespace from initial CLI entry
        """
        nsvars = vars(namespace)
        self.storage = FileStorage(nsvars.pop('root'))
        command = nsvars.pop('command')
        command = command if command else 'curses'
        command_class = Command.family_member('name', command)
        if not command_class:
            raise RuntimeError(f"Unknown command {command}")
        self.ui = UI.family_member('name', command_class.uitype)(self)
        self.command = command_class(
            storage=self.storage, ui=self.ui, **nsvars)

    def execute(self):
        """Handle the command and output its final status"""
        result = self.command.execute()
        if result:
            print(result)
        if self.command.status:
            print(self.command.status)

    # Some useful methods so other components don't need to import from
    # different class families

    def get_commands(self, *attributes):
        return Command.family_members(*attributes)

    # A method for commands within interactive UIs. Use our own storage but the UI
    # is passed in. Returns None if attribute value doesn't resolve.

    def get_command(self, attribute, value, **kwargs):
        member = Command.family_member(attribute, value)
        if member:
            args = {'storage': self.storage} | kwargs
            return member(**kwargs)
