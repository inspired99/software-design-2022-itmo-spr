class Command:
    """
    Common command interface for all deriving commands.
    """
    command_list = ['cat', 'wc', 'pwd', 'echo', 'exit']

    def __init__(self, name, args):
        self.name = name
        self.args = []

    def _invoke(self, *args):
        """
        Execution of a command, each command
        has it's own realization of this method.
        """
        return
