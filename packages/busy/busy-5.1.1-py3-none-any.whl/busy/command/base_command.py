from busy.command.command import CollectionCommand

# Returns the top task from the queue, without tags, a resource, or followons.


class BaseCommand(CollectionCommand):

    name = "base"

    @CollectionCommand.wrap
    def execute(self):
        return self.output_items(lambda i: i.base)
