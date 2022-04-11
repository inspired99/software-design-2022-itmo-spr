import sys

from src.commandInterface.catCommand import Cat
from src.commandInterface.echoCommand import Echo
from src.commandInterface.exitCommand import Exit
from src.commandInterface.pwdCommand import Pwd
from src.commandInterface.wcCommand import Wc
from src.commandParse.commandParser import CommandParser


class CommandLine:
    """
    Class for command line functions.
    """

    def __init__(self):
        print('Command Line started. Hello!')
        self.parser = CommandParser()
        self.command_map = {'wc': Wc, 'pwd': Pwd, 'cat': Cat, 'echo': Echo, 'exit': Exit}

    def run(self, default_inp=None) -> None:
        while True:
            if not default_inp:
                user_input = sys.stdin.readline()
            else:
                user_input = default_inp
            input_str = self.parser.subst_vars(user_input)
            self.parser.parse_bind(input_str)
            parsed_pipelines_and_commands = self.parser.parse_pipelines_and_commands(input_str)
            results = []
            number_of_pipelines = len(parsed_pipelines_and_commands.keys()) - 1

            for order, command_args in parsed_pipelines_and_commands.items():
                command = command_args[0].lower()
                if results:
                    args = command_args[1] or results[-1]
                else:
                    args = command_args[1]
                if command not in self.command_map:
                    continue
                command_instance = self.command_map[command]
                result = command_instance.invoke(args)
                if number_of_pipelines > 0 and len(results) < number_of_pipelines:
                    results.append(result)
                    continue
                results.append(result)
                print(results[-1])

            if default_inp:
                if results:
                    return results[-1]
                else:
                    return
