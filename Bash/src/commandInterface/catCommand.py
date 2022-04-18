import os

from src.commandInterface.command import Command


class Cat(Command):
    """
    Display the content of file.
    Flags:
    -n -> numbers of lines.
    -s -> omit blank lines
    """
    flags = ['-n', '-s']

    @staticmethod
    def invoke(args: str) -> str:

        if not args:
            raise FileNotFoundError("No files to read from.")

        flagged = Command._flagged(Cat.flags, args)

        files = args.split()

        result = []

        for filename in files:
            if filename != flagged:

                try:
                    with open(filename) as file:
                        content = Cat._read_file(file, flagged)
                        result.append(content)
                except FileNotFoundError:
                    try:
                        with open(os.path.join(os.getcwd(), filename), "r") as f:
                            content = Cat._read_file(f, flagged)
                            result.append(content)
                    except FileNotFoundError:
                        raise FileNotFoundError(f"No such file: {filename}")

        output = ""
        for file_output in result:
            output = output.join(file_output)

        return output

    @staticmethod
    def _read_file(file, flag) -> list:
        result = []
        if flag == "-n":
            for index, line in enumerate(file):
                result.append(f'{index + 1} ' + line)
        elif flag == "-s":
            lines = [i for i in file.readlines() if i != '\n']
            result = lines
        else:
            result = file.readlines()

        return result
