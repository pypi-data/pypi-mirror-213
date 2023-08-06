from busy.command.command import CollectionCommand


class ShowCommand(CollectionCommand):
    """Show just the description"""

    name = 'show'

    @CollectionCommand.wrap
    def execute(self):
        return self.output_items(lambda i: i.description)
