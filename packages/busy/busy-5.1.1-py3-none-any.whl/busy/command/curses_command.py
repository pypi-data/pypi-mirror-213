from ..command.command import Command


class CursesCommand(Command):

    name = 'curses'
    uitype = 'curses'

    def execute(self):
        """Start the Curses UI"""
        self.ui.start()
        print(f'Session complete: {self.ui.name}')
