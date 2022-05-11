import subprocess

from src.commandInterface.command import Command


class ExternalCommand(Command):
    """
    External commands from real bash.
    """
    external_commands_list = ['git', 'vim', 'nano']
    external_command_name = None
    external_output = None

    @staticmethod
    def invoke(args: list):

        try:
            if ExternalCommand.external_command_name in ExternalCommand.external_commands_list:
                bash = subprocess.run([ExternalCommand.external_command_name, *args])
                ExternalCommand.external_output = bash.stdout

        except (OSError, TypeError) as e:
            print(str(e))
