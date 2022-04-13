from src.commandInterface.command import Command


class Echo(Command):
    """
    Display string that is passed as an argument.
    """

    @staticmethod
    def invoke(args: str) -> str:
        return args
