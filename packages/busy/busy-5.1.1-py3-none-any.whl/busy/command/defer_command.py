from dataclasses import dataclass

from busy.command.command import QueueCommand
from busy.util import date_util


@dataclass
class DeferCommand(QueueCommand):

    timing: str = ""
    yes: bool = None
    name = 'defer'
    key = 'f'

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        parser.add_argument('--timing', '-t', default='tomorrow')
        self._add_confirmation_arg(parser)

    def clean_args(self):
        def update_deferral():
            self.timing = self.ui.get_string("Timing", "tomorrow")
        super().clean_args()
        if self.selection:
            items = self.collection.items(self.selection)
            self.ui.output('\n'.join([str(i) for i in items]))
            if not self.provided('timing'):
                self.timing = 'tomorrow'
            while not self.provided('yes'):
                intro = f"Defer {self.count()} to {self.date}"
                self.confirm(intro, update_deferral)

    @property
    def date(self):
        """Absolute date for deferral"""
        # Don't cache this!
        return date_util.relative_date(self.timing)

    @QueueCommand.wrap
    def execute(self):
        if not self.selection:
            self.status = "Deferred nothing"
        elif self.yes is False:
            self.status = "Defer operation unconfirmed"
        else:
            plans = self.storage.get_collection(self.queue, 'plan')
            deferred = self.collection.delete(self.selection)
            for item in deferred:
                item.plan_date = self.date
                item.state = 'plan'
            plans.extend(deferred)
            self.status = f"Deferred {self.count(deferred)} to {self.date}"
