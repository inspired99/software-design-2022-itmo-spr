from src.commandInterface.command import Command
import sys


class Exit(Command):
    """
    Exit command terminates bash.
    """
    @staticmethod
    def _invoke():
        return sys.exit('Command Line is terminated. Goodbye!')
