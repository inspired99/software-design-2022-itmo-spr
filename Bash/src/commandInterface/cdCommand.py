import os

from src.commandInterface.command import Command
from src.commandInterface.commandExceptions import CommandExecutionError


class Cd(Command):
    """
    Changes current directory.
    """
    def _invoke(self, args: str):
        if not self.args:
            return ""
        if len(self.args) > 1:
            raise CommandExecutionError("Too many arguments for cd command")
        try:
            os.chdir(self.args[0])
        except FileNotFoundError as e:
            raise CommandExecutionError from e
