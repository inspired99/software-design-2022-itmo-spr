from src.commandInterface.command import Command
import sys


class Exit(Command):
    """
    Exit command terminates bash.
    """
    def _invoke(self, args: str):
        return sys.exit('Command Line is terminated. Goodbye!')
