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
    flags = ['-l', '-c', '-w']

    @staticmethod
    def invoke(args: list) -> str:
        flagged = Command._flagged(Wc.flags, args)

        result = ""
        for filename in args:
            if filename != flagged:
                file = Wc.read_file(filename)

                res = Wc.count_l_w_c(file)
                file_title = filename.split('/')[-1]
                new_line = '\n'
                if flagged:
                    result = result + f" {res[flagged]}" + f" {file_title} " + f"{new_line}"
                else:
                    result = result + f" {res['-l']}" + f" {res['-w']}" + f" {res['-c']}  {file_title}" + f"{new_line}"

        result = result.lstrip()
        return result

    @staticmethod
    def read_file(path):
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
