import subprocess

from src.commandInterface.command import Command


class ExternalCommand(Command):
    """
    External commands from real bash.
    """

    @staticmethod
    def invoke(args: list):

        try:
            bash = subprocess.run([ExternalCommand.external_command_name, *args])
            return bash.stdout
        except (OSError, TypeError) as e:
            print(str(e))

