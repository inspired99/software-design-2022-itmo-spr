import sys

from src.commandInterface.catCommand import Cat
from src.commandInterface.commandExceptions import FlagError
from src.commandInterface.echoCommand import Echo
from src.commandInterface.exitCommand import Exit
from src.commandInterface.externalCommand import ExternalCommand
from src.commandInterface.grepCommand import Grep
from src.commandInterface.pwdCommand import Pwd
from src.commandInterface.wcCommand import Wc
from src.commandParse.commandParser import CommandParser
from src.commandParse.parseExceptions import AssignmentError, ParseException, PipelineError, CommandNotFoundError


class CommandLine:
    """
    Class for command line functions.
    """

    def __init__(self):
        print('Command Line started. Hello!')
        self.parser = CommandParser()
        self.command_map = {'wc': Wc, 'pwd': Pwd, 'cat': Cat, 'echo': Echo, 'exit': Exit, 'grep': Grep}
        self.external_commands = {'vim': ExternalCommand,
                                  'nano': ExternalCommand, 'git': ExternalCommand}

    def run(self, default_inp=None):
        exceptions_parser = (ParseException, PipelineError, AssignmentError, CommandNotFoundError)
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
                is_external = False
                if command[0] not in self.command_map and command[0] not in self.external_commands:
                    continue

                if command[0] in self.external_commands:
                    command_instance = self.external_commands[command[0]]
                    command_instance.external_command_name = command[0]
                    is_external = True

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
                    if result:
                        result = result.rstrip()

                except exceptions_command as e:
                    print(str(e))
                    continue

                if number_of_pipelines > 0 and len(results) < number_of_pipelines:
                    results.append(result)
                    continue

                if not is_external:
                    results.append(result)
                    print(results[-1])

            if default_inp:
                if results:
                    return results[-1]
                else:
                    return
