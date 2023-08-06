from dataclasses import dataclass

from busy.command.command import CollectionCommand


@dataclass
class EditorCommandBase(CollectionCommand):

    @CollectionCommand.wrap
    def execute(self):
        if not self.selection:
            self.status = "Edited nothing"
        else:
            edited = self.ui.edit_items(self.collection, self.selection)
            self.status = f"Edited {self.count(edited)}"


# Special case versions of EditCommand to edit just the top item or the whole
# queue. In the shell you'd just type "edit" or "edit 1-" but this is
# convenient in curses.

class EditCommand(EditorCommandBase):

    name = "edit"
    key = "e"


class EditAllCommand(EditorCommandBase):

    name = 'manage'
    key = 'm'
    default_criteria = ["1-"]
