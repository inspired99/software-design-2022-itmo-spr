import os

from src.commandInterface.command import Command


class Pwd(Command):
    """
    Shows current working directory.
    """

    @staticmethod
    def invoke(args="") -> str:
        path = os.getcwd()
        return path
