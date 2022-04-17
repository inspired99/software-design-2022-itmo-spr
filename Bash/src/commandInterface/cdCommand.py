import os

from src.commandInterface.command import Command


class Cd(Command):
    """
    Changes current directory.
    """
    @staticmethod
    def invoke(args: str) -> str:
        if not args:
            return ""
        if len(args.split()) > 1:  # what if ' ' in filepath?
            raise RuntimeError("Too many arguments for cd command")
        os.chdir(args)
        return ''
