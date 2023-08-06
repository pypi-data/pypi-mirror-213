from busy.command.command import CollectionCommand


class ResourceCommand(CollectionCommand):
    """Get the resource (URL) for items in a collection"""

    name = "resource"

    @CollectionCommand.wrap
    def execute(self):
        return self.output_items(lambda i: i.resource)
