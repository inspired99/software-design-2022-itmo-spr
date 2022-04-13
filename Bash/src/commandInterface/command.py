from src.commandInterface.commandExceptions import FlagError


class Command:
    """
    Common command interface for all deriving commands.
    """
    command_list = ['cat', 'wc', 'pwd', 'echo', 'exit']

    def __init__(self, name, args):
        self.name = name
        self.args = args

    @staticmethod
    def invoke(args: str) -> str:
        """
        Execution of a command, each command
        has it's own realization of this method.
        :param args: input string of args
        """
        return ""

    @staticmethod
    def _flagged(flags: list, args: str):
        """
        Method to determine flag.
        :param flags: list of flags
        :param args:  input string of args
        :return: empty flag if flag is absent or determined flag
        """
        flagged = False
        flag_command = ""

        for flag in flags:
            if flag in args.split():
                if flagged:
                    raise FlagError("Too many flags for this command.")
                flagged = True
                flag_command = flag

        if "-" in args:
            if not flagged:
                if args[args.find("-") + 1]:
                    try:
                        if args[args.find("-") + 2].isspace():
                            raise FlagError("No such flag supported by this command.")
                    except IndexError:
                        raise FlagError("Wrong position of flag.")
            if flagged:
                if args.split().index(flag_command) != 0:
                    raise FlagError("Wrong position of flag.")

        return flag_command
