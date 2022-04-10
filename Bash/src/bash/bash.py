from src.commandParse.commandParser import CommandParser
import sys


class CommandLine:
    """
    Class for command line functions.
    """
    def __init__(self):
        print('Command Line started. Hello!')
        self.parser = CommandParser()

    def __run__(self):
        while True:
            user_input = sys.stdin.read()
            input_str = self.parser.subst_vars(user_input)
            self.parser.parse_bind(input_str)
            parsed_pipelines_and_commands = self.parser.parse_pipelines_and_commands(input_str)



