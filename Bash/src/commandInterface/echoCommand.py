from src.commandInterface.command import Command


class Echo(Command):
    """
    Display string that is passed as an argument.
    """
    def _invoke(self, *args):
        return print(args)