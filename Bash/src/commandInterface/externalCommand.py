import subprocess

from src.commandInterface.command import Command


class ExternalCommand(Command):
    """
    External commands from real bash.
    """
    command_name = None

    @staticmethod
    def invoke(args: list):

        try:
            external_bash = subprocess.run([ExternalCommand.command_name, *args], stdout=subprocess.PIPE, text=True)
            return external_bash.stdout.rstrip()

        except (OSError, TypeError) as e:
            print(str(e))
