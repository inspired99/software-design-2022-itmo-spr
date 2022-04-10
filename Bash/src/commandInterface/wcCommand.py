from src.commandInterface.command import Command
from src.commandInterface.commandExceptions import FlagError


class Wc(Command):
    """
    Count the number of lines, words, characters
    in given files or input.
    Flags:
    -l -> number of lines in file.
    -c -> number of characters in file.
    -w -> number of words in file.
    """
    flags = ['-l', '-c', 'w']

    def _invoke(self, args: str) -> str:
        flagged = self._flagged(Wc.flags, args)

        result = ""
        for file in args.split():
            res = self.count_l_w_c(file)
            if flagged:
                result = result + f" {res[flagged]}" + f" {file} \n"
            else:
                result = result + f" {res['l']}" + f" {res['w']}" + f" {res['c']} \n"

        return result

    @staticmethod
    def count_l_w_c(filename):
        counter = dict()
        lines = 0
        words = 0
        characters = 0

        try:
            with open(filename) as file:
                for line in file:
                    lines += 1
                    words += len(line.split())
                    characters += len(line.strip())
                counter['l'] = lines
                counter['w'] = words
                counter['c'] = characters

        except FileNotFoundError:
            raise FileNotFoundError(f"No such file: {filename}")

        return counter
