import sys

from src.commandInterface.command import Command


class Exit(Command):
    """
    Exit command terminates bash.
    """

    @staticmethod
    def invoke(args=None) -> str:
        return sys.exit('Command Line is terminated. Goodbye!')
