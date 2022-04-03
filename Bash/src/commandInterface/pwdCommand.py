from src.commandInterface.command import Command
import os


class Pwd(Command):
    """
    Shows current working directory.
    """
    def _invoke(self):
        return os.getcwd()

