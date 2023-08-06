from argparse import ArgumentParser
from io import StringIO

from wizlib.rlinput import rlinput

from busy.ui.ui import TerminalUI
from busy.ui.ui import UserCancelError
from busy.ui.ui import Prompt


class ShellUI(TerminalUI):

    """The UI to execute one command passed in through the shell. There will be
    limited interactivity, if the user omits an argument on the command line,
    but otherwise this is a run and done situation.
    """

    name = "shell"

    def output(self, intro=""):
        """Print some regular output"""
        if intro:
            print(intro)

    def get_string(self, intro, default=""):
        prompt = Prompt(intro=intro)
        return rlinput(prompt=self._prompt_string(prompt), default=default)

    def get_option(self, chooser):
        """Get a choice from the user"""
        key = rlinput(prompt=self._prompt_string(chooser))
        return chooser.choice_by_key(key)

    def _prompt_string(self, prompt):
        result = []
        if prompt.intro:
            result.append(prompt.intro)
        if prompt.default:
            result.append(f"[{prompt.default}]")
        for choice in prompt.choices:
            if choice.word == prompt.default:
                continue
            pre, it, post = choice.word.partition(choice.key)
            result.append(f"{pre}({it}){post}")
        return " ".join(result) + ": "

    def write_prompt(self, prompt):
        """Output the prompt"""
        print(self._prompt_string(prompt), end="")
