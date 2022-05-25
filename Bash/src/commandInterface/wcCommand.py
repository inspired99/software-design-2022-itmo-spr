import os

from src.commandInterface.command import Command


class Wc(Command):
    """
    Count the number of lines, words, characters
    in given files or input.
    Flags:
    -l -> number of lines in file.
    -c -> number of characters in file.
    -w -> number of words in file.
    """
    flags = ['-l', '-w', '-c']

    @staticmethod
    def invoke(args: list) -> str:
        if not args:
            raise FileNotFoundError("No files to read from.")

        flag_commands = Command._flagged(Wc.flags, args)

        flagged = flag_commands != []

        result = ""
        for filename in args:
            if filename not in flag_commands:
                file = Wc.read_file(filename)

                res = Wc.count_l_w_c(file)
                file_title = filename.split('/')[-1]
                new_line = '\n'

                if not Wc.from_pipeline:
                    if flagged:
                        for flag in flag_commands:
                            result = result + f" {res[flag]}"
                        result = result + f" {file_title}" + f"{new_line}"
                    else:
                        result = result + f" {res['-l']}" + f" {res['-w']}" + f" {res['-c']}  {file_title}" + \
                                 f"{new_line}"
                else:
                    if flagged:
                        for flag in flag_commands:
                            result = result + f" {res[flag]}"
                        result = result + f" {file_title}" + f"{new_line}"
                    else:
                        result = result + f" {res['-l']}" + f" {res['-w']}" + f" {res['-c']}" + f"{new_line}"

        Wc.from_pipeline = False
        result = result.strip()
        return result

    @staticmethod
    def read_file(path):

        if Wc.from_pipeline:
            return path

        try:
            with open(path) as file:
                result = file.read()
        except FileNotFoundError:
            try:
                with open("".join((os.getcwd(), path))) as f:
                    result = f.read()
            except FileNotFoundError:
                raise FileNotFoundError(f"No such file: {path}")
        result = result.rstrip('\n')
        return result

    @staticmethod
    def count_l_w_c(file):
        counter = dict()
        lines = len(file.split('\n'))
        words = len(file.split())
        characters = 1
        for _ in file:
            characters += 1

        counter['-l'] = lines
        counter['-w'] = words
        counter['-c'] = characters

        return counter
