from src.commandInterface.commandExceptions import FlagError


class Command:
    """
    Common command interface for all deriving commands.
    """
    command_list = ['cat', 'wc', 'pwd', 'echo', 'exit', 'grep']
    from_pipeline = False
    args_previous = []
    has_args = False

    @staticmethod
    def invoke(args):
        """
        Execution of a command, each command
        has it's own realization of this method.
        :param args: input string of args
        """
        return ""

    @staticmethod
    def _flagged(flags: list, args: list) -> list:
        """
        Method to determine flag.
        :param flags: list of flags
        :param args:  input string of args
        :return: empty flag if flag is absent or determined flag
        """
        if not args:
            return []

        flagged = False
        flag_commands = []

        for flag in flags:
            if flag in args:
                flagged = True
                flag_commands.append(flag)

        if flagged:
            if not args[0].startswith("-"):
                raise FlagError("Wrong position of flag.")

        for arg in args:
            if arg.startswith("-"):
                if not flagged:
                    raise FlagError("No such flag supported for this command.")

        return flag_commands
