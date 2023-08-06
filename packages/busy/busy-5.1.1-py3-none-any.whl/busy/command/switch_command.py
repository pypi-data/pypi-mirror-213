from dataclasses import dataclass

from busy.command.command import QueueCommand


@dataclass
class SwitchCommand(QueueCommand):
    """
    Switch to a different queue. Note this only works in interactive UIs; the
    shell UI has no state so it's essentially a no-op.
    """

    name = "switch"
    key = "w"
    yes: bool = None

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        self._add_confirmation_arg(parser)

    def clean_args(self):
        self.newqueuename = self.ui.get_string("Switch to queue", "tasks")
        if not self.provided('yes'):
            if not self.storage.queue_exists(self.newqueuename):
                self.confirm(f"Switch to empty queue {self.newqueuename}")
            else:
                self.yes = True

    @QueueCommand.wrap
    def execute(self):
        if self.yes:
            self.queue = self.newqueuename
            self.status = f"Switched to queue {self.newqueuename}"
        else:
            self.status = "Switch operation canceled"
