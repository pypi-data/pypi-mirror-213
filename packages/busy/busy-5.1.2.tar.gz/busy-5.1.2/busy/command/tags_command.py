from busy.command.command import QueueCommand
from busy.model.collection import Collection


class TagsCommand(QueueCommand):

    name = 'tags'

    @QueueCommand.wrap
    def execute(self):
        tags = set()
        for state in Collection.family_attrs('state'):
            collection = self.storage.get_collection(self.queue, state)
            for item in collection:
                tags |= item.tags
        return '\n'.join(sorted(tags))
