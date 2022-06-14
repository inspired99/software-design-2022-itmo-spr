from src.commandInterface.command import Command


class Exit(Command):
    """
    Exit command terminates bash.
    """

    @staticmethod
    def invoke(args=None) -> None:
        Command.exit_status = True
