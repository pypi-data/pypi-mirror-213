from dataclasses import dataclass

from busy.command.command import CollectionCommand


@dataclass
class DeleteCommand(CollectionCommand):

    yes: bool = None
    name = 'delete'
    key = 'd'
    default_criteria = [1]

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        parser.add_argument('--yes', action='store_true', default=None)

    def clean_args(self):
        super().clean_args()
        if self.selection:
            items = self.collection.items(self.selection)
            self.ui.output('\n'.join([str(i) for i in items]))
            self.confirm(f"Delete {self.count()}")

    # Assume the indices have been already set, before confirmation.

    @CollectionCommand.wrap
    def execute(self):
        if self.yes:
            deleted = self.collection.delete(self.selection)
            self.status = f"Deleted {self.count(deleted)}"
        else:
            self.status = "Delete command canceled"
