# A Command class handles argparse stuff (ArgumentParser and Namespace) on
# behalf of a method somewhere in the model (i.e. on Queue) and returns text
# that can be used in a UI. A Command class rarely performs an actual
# operation.
#
# Command classes must have the following class-level attributes:
#
# ui - Name of the UI associated with this Command. Default is 'shell', set in
# base class. Inside the command, self._ui refers to the UI object itself.
#
# name - Name of the command. Used in the original Shell UI and also as the
# name of the methods on the queue.
#
# Commands must implement the following methods:
#
# @classmethod set_parser(parser) - Receives an ArgumentParser (actually a
# subparser, but that's irrelevant here), adds arguments to it as appropriate
# for that command, and keeps a reference to it in self.parser.
#
# execute(namespace) - Perform the command. It might use the namespace from the
# Handler, or it might accept a new Namespace, in the event of interactive UIs.
# The execute method is expected to set a property "status" with a one-line
# string description of what happened.
#
# A Command might implement the following methods:
#
# clean_args() - Examine the self._namespace and use the UI to request any args
# that are omitted. Tends to be command-specific.
#
# They might have the following class attributes:
#
# key - For the Curses UI. What key the user should press.
#
# TODO: Move the base class to __init__.py

from argparse import Namespace
from dataclasses import dataclass

from busy.model.collection import Collection
from busy.storage import Storage
from busy.ui.ui import UI
from busy.util.class_family import ClassFamily
from busy.util.super_wrapper import SuperWrapper


@dataclass
class Command(ClassFamily, SuperWrapper):
    """
    Base class for all commands

    Parameters:

    storage - A Busy Storage object (required)

    ui - A Busy UI object
    """

    storage: Storage
    ui: UI = None
    status = ''
    uitype = 'shell'

    @classmethod
    def set_parser(self, parser):
        self.parser = parser

    @classmethod
    def _add_confirmation_arg(self, parser):
        """Add argparse argument for confirmation"""
        parser.add_argument('--yes', '-y', action='store_true')

    def execute(self, method, *args, **kwargs):
        """Actually perform the command, using SuperWrapper"""
        self.clean_args()
        result = method(self, *args, **kwargs)
        return result

    # The clean_args method serves 3 purposes.
    #
    # (1) If any arguments are missing from the command, ask the user to
    # provide them through the UI. For example, when adding a new item to a
    # queue, if a description is not yet provided, ask the user to provide one.
    #
    # (2) This is where defaulting happens. Defaults should generally not be
    # applied in the model, but rather here in the command layer, closer to the
    # user.
    #
    # (3) Call for confirmation from the user (using is_confirmed) if
    # appropriate.
    #
    # The default is to do nothing, as this is essentially an abstract method
    # ripe for override.

    def clean_args(self):
        pass

    def provided(self, argument):
        """Was an argument provided?"""
        value = None
        if hasattr(self, argument):
            value = getattr(self, argument)
        return bool(value)

    def confirm(self, verb, other_action=None):
        """Ensure that a command is confirmed by the user"""
        if self.provided('yes'):
            return self.yes
        else:
            chooser = self.ui.get_chooser(intro=f"{verb}?", default="ok")
            chooser.add_choice(keys=['y', '\n', ''], words=['ok'], action=True)
            chooser.add_choice(keys=['c'], words=['cancel'], action=False)
            if other_action:
                chooser.add_choice(keys=['o'], words=[
                                   'other'], action=other_action)
            choice = self.ui.get_option(chooser)
            if type(choice) == bool:
                self.yes = choice
            return choice


@dataclass
class QueueCommand(Command):
    """Base for commands that work on the default collection of one queue"""

    queue: str = 'tasks'
    collection_state: str = 'todo'
    criteria: list = None
    default_criteria = [1]

    @property
    def collection(self):
        """Return the collection object being queried"""
        if not hasattr(self, '_collection'):
            self._collection = self.storage.get_collection(
                self.queue, self.collection_state)
        return self._collection

    @property
    def selection(self):
        """Indices of objects within the query collection that match the
        criteria"""
        if not hasattr(self, '_selection'):
            self._selection = self.collection.select(*self.criteria)
        return self._selection

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        parser.add_argument('queue', default='tasks', nargs='?')
        parser.add_argument('--criteria', '-c', action='store', nargs="*")

    def clean_args(self):
        """Apply default criteria"""
        super().clean_args()
        if not self.provided('criteria'):
            self.criteria = self.default_criteria

    @Command.wrap
    def execute(self, method, *args, **kwargs):
        """Execute the command then save the collection(s)"""
        result = method(self, *args, **kwargs)
        self.storage.save()
        return result

    def count(self, items=None):
        """Return a friendly string count of some items"""
        if items is None:
            items = self.selection
        if len(items) == 1:
            return "1 item"
        if len(items) > 1:
            return str(len(items)) + " items"
        return "nothing"


@dataclass
class CollectionCommand(QueueCommand):
    """Base for commands that work on a user-specified collection"""

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        states = Collection.family_attrs('state')
        parser.add_argument(
            '--state', '-s', action='store', default='todo',
            dest='collection_state', choices=states)

    def output_items(self, func, with_index=False):
        """Return some attribute of all the items in the collection"""
        collection = self.storage.get_collection(
            self.queue, self.collection_state)
        indices = collection.select(*self.criteria)
        if indices:
            if with_index:
                return '\n'.join([func(collection[i], i) for i in indices])
            else:
                return '\n'.join([func(collection[i]) for i in indices])
        else:
            self.status = f"Queue '{self.queue}' has " + \
                    f"no {self.collection_state} items"
