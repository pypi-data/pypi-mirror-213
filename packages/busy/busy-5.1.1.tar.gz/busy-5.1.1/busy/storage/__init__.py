from busy.model.collection import Collection


class Storage:
    """Abstract base class for Storage classes"""

    def get_collection(self, queue: str, state: str = 'todo') -> Collection:
        pass

    def save(self):
        pass
