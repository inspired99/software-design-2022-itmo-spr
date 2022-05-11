from src.commandInterface.command import Command


class Echo(Command):
    """
    Display string that is passed as an argument.
    """

    @staticmethod
    def invoke(args: list) -> str:
        result = ''
        if Echo.from_pipeline:
            if Echo.has_args:
                result = "".join(args)
        else:
            result = "".join(args)

        Echo.from_pipeline = False
        return result
