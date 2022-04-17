import os

from src.commandInterface.command import Command


class Ls(Command):
    """
    List of objects in current directory.
    """
    @staticmethod
    def invoke(args: str) -> str:
        if not args:
            return '\n'.join(os.listdir())
        if len(args.split()) > 1:  # what if ' ' in filepath?
            raise RuntimeError("Too many arguments for ls command")
        return '\n'.join(os.listdir(args))
