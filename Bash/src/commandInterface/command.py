from src.commandInterface.commandExceptions import FlagError


class Command:
    """
    Common command interface for all deriving commands.
    """
    command_list = ['cat', 'wc', 'pwd', 'echo', 'exit']

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def _invoke(self, args: str):
        """
        Execution of a command, each command
        has it's own realization of this method.
        """
        return

    @staticmethod
    def _flagged(flags: list, args: str):
        flagged = False
        flag_command = ""

        for flag in flags:
            if flag in args.split():
                if flagged:
                    raise FlagError("Too many flags for this command.")
                flagged = True
                flag_command = flag

        if "-" in args and not flagged:
            if args[args.find("-") + 1] and not args[args.find("-") + 2]:
                raise FlagError("No such flag supported by this command.")

        return flag_command
