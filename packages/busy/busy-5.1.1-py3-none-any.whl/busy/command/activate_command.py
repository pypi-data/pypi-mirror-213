from dataclasses import dataclass

from busy.command.command import QueueCommand
from busy.util import date_util


def is_today_or_earlier(plan):
    return plan.plan_date <= date_util.today()


@dataclass
class ActivateCommand(QueueCommand):

    timing: str = ""
    yes: bool = None
    collection_state: str = 'plan'
    name = 'activate'
    key = 'c'
    default_criteria = [is_today_or_earlier]

    @classmethod
    def set_parser(self, parser):
        super().set_parser(parser)
        # parser.add_argument('--timing', '-t', default='today')
        self._add_confirmation_arg(parser)

    def clean_args(self):
        # def update_timing():
        #     self.timing = self.ui.get_string("Timing", "today")
        super().clean_args()
        # For now, handling criteria as normal
        if self.selection:
            if not self.provided('yes'):
                items = self.collection.items(self.selection)
                self.ui.output('\n'.join([str(i) for i in items]))
                intro = f"Activate {self.count()}"
                # self.confirm(intro, update_timing)
                self.confirm(intro)

    @QueueCommand.wrap
    def execute(self):
        if not self.selection:
            self.status = "Activated nothing"
        elif self.yes is False:
            self.status = "Activate command canceled"
        else:
            todos = self.storage.get_collection(self.queue)
            activated = self.collection.delete(self.selection)
            for item in activated:
                item.state = 'todo'
            todos[0:0] = activated
            self.status = f"Activated {self.count()}"
