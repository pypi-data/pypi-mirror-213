import re
from dataclasses import KW_ONLY, dataclass
from datetime import date

from busy.util.date_util import absolute_date, relative_date


class ItemStateError(Exception):
    pass


@dataclass
class Item:

    description: str
    _: KW_ONLY
    state: str = 'todo'
    done_date: date = None
    plan_date: date = None

    def __str__(self):
        """Represent the item as its description"""
        return self.description

    def restricted(*allowed_states):
        """Restrict a method to a specific set of states"""
        def wrapper(method):
            def replacement(self, *args, **kwargs):
                if self.state in allowed_states:
                    return method(self, *args, **kwargs)
                else:
                    raise ItemStateError
            return replacement
        return wrapper

    FOLLOW_SPLIT = re.compile(r'\s*\-*\>\s*')
    REPEAT = re.compile(r'^\s*repeat(?:\s+[io]n)?\s+(.+)\s*$', re.I)

    def __setattr__(self, name, value):
        if self.__annotations__[name] == date:
            value = absolute_date(value)
        super().__setattr__(name, value)

    @property
    def first(self):
        return self.FOLLOW_SPLIT.split(self.description, maxsplit=1)[0]

    @property
    def _words(self):
        return self.first.split()

    @property
    def tags(self):
        wins = [w for w in self._words if w.startswith("#")]
        return {w[1:].lower() for w in wins}

    @property
    def resource(self):
        wins = [w for w in self._words if w.startswith("@")]
        return wins.pop()[1:] if wins else ""

    @property
    def base(self):
        wins = [w for w in self._words if w[0] not in '#@']
        return " ".join(wins)

    @property
    def next(self):
        """Second and successive segments, all but current"""
        split = self.FOLLOW_SPLIT.split(self.description, maxsplit=1)
        if len(split) > 1:
            return split[1]
        else:
            return ""

    @property
    def current(self):
        """The first segment, all but next"""
        split = self.FOLLOW_SPLIT.split(self.description, maxsplit=1)
        if split:
            return split[0]
        else:
            return ""

    @property
    def repeat(self):
        followon = self.next
        match = self.REPEAT.match(followon)
        if match:
            return match.group(1)
        else:
            return ""

    @property
    def repeat_date(self):
        repeat = self.repeat
        if repeat:
            return relative_date(repeat)

    @restricted('todo')
    def done(self, done_date: date):
        self.state = 'done'
        self.done_date = done_date
        if self.repeat:
            follow = Item(self.description, state='plan')
            follow.plan_date = relative_date(self.repeat)
            return follow
        if self.next:
            follow = Item(self.next)
            self.description = self.first
            return follow

    @restricted('done')
    def undone(self):
        self.state = 'todo'

    @restricted('todo')
    def skip(self):
        self.state = 'skip'

    @restricted('skip')
    def unskip(self):
        self.state = 'todo'

    @restricted('todo')
    def plan(self, plan_date: date):
        self.state = 'plan'
        self.plan_date = plan_date

    @restricted('plan')
    def unplan(self):
        self.state = 'todo'
