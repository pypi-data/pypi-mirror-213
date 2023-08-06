from ..command.command import Command


class QueuesCommand(Command):

    name = 'queues'

    @Command.wrap
    def execute(self):
        """Get the names of the queues. Cache nothing."""
        names = sorted(self.storage.queue_names)
        return '\n'.join(names)
