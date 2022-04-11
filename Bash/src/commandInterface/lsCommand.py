import os

from src.commandInterface.command import Command
from src.commandInterface.commandExceptions import CommandExecutionError


class Ls(Command):
    """
    List of objects in current directory.
    """
    def _invoke(self, args: str):
        if not self.args:
            return '\n'.join(os.listdir())
        if len(self.args) > 1:
            raise CommandExecutionError("Too many arguments for ls command")
        try:
            path = os.path.join(os.getcwd(), self.args[0])
            return '\n'.join(os.listdir(path))
        except FileNotFoundError as e:
            raise CommandExecutionError from e
