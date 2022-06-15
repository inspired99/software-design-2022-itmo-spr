import sys

from src.commandInterface.catCommand import Cat
from src.commandInterface.command import Command
from src.commandInterface.commandExceptions import FlagError
from src.commandInterface.echoCommand import Echo
from src.commandInterface.exitCommand import Exit
from src.commandInterface.externalCommand import ExternalCommand
from src.commandInterface.pwdCommand import Pwd
from src.commandInterface.wcCommand import Wc
from src.commandParse.commandParser import CommandParser
from src.commandParse.parseExceptions import AssignmentError, ParseException, PipelineError


class CommandLine:
    """
    Class for command line functions.
    """

    def __init__(self):
        print('Command Line started. Hello!')
        self.parser = CommandParser()
        self.command_map = {'wc': Wc, 'pwd': Pwd, 'cat': Cat, 'echo': Echo, 'exit': Exit}

    def run(self, default_inp=None):
        exceptions_parser = (ParseException, PipelineError, AssignmentError)
        exceptions_command = (FileNotFoundError, FlagError)
        while True:
            if not default_inp:
                user_input = sys.stdin.readline()
            else:
                user_input = default_inp
            try:
                input_str = self.parser.subst_vars(user_input)
                self.parser.parse_bind(input_str)
                parsed_pipelines_and_commands = self.parser.parse_pipelines_and_commands(input_str)
            except exceptions_parser as e:
                print(str(e))
                continue

            results = []
            number_of_pipelines = len(parsed_pipelines_and_commands.keys()) - 1

            for command, args in parsed_pipelines_and_commands.items():
                Command.exit_status = False

                if command[0] not in self.command_map:
                    if results:
                        args = args or [results[-1]]
                    ExternalCommand.command_name = command[0]
                    res_ext = ExternalCommand.invoke(args)
                    results.append(res_ext)
                    continue

                else:
                    command_instance = self.command_map[command[0]]
                command_instance.has_args = False

                if args:
                    command_instance.has_args = True
                if results:
                    args = args or [results[-1]]

                command_instance.from_pipeline = False

                if number_of_pipelines > 0 and results:
                    command_instance.from_pipeline = True

                try:
                    result = command_instance.invoke(args)

                except exceptions_command as e:
                    print(str(e))
                    continue

                if number_of_pipelines > 0 and len(results) < number_of_pipelines:
                    results.append(result)
                    continue

                results.append(result)

            if not Command.exit_status and results:
                if results[-1]:
                    print(results[-1])
                else:
                    print()

            if parsed_pipelines_and_commands and Command.exit_status:
                sys.exit('Command Line is terminated. Goodbye!')

            if default_inp:
                if results:
                    return results[-1]
                else:
                    return
