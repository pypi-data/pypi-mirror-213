from busy.command.command import CollectionCommand
from busy.util.checklist import Checklist


class PrintCommand(CollectionCommand):
    """Generate a Checklist PDF"""

    default_criteria = ["1-"]
    name = "print"

    @CollectionCommand.wrap
    def execute(self):
        checklist = Checklist()
        collection = self.storage.get_collection(
            self.queue, self.collection_state)
        indices = collection.select(*self.criteria)
        if indices:
            items = [collection[i].base for i in indices]
        else:
            self.status = f"Queue '{self.queue}' has " + \
                    f"no {self.collection_state} items that meet the criteria"
        queue = self.queue.capitalize()
        state = self.collection_state.capitalize()
        criteria = (": "+",".join(self.criteria)) \
            if (self.criteria != self.default_criteria) else ""
        title = f"{queue} ({state}{criteria})"
        checklist.generate(title, items)
