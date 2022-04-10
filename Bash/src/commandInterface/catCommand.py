from src.commandInterface.command import Command
import os


class Cat(Command):
    """
    Display the content of file.
    Flags:
    -n -> numbers of lines.
    -s -> omit blank lines
    """
    flags = ['n', 's']

    def _invoke(self, args: str) -> str:
        if not args:
            raise FileNotFoundError("No files to read from.")

        flagged = self._flagged(Cat.flags, args)
        files = args.split()
        result = []

        for filename in files:
            try:
                with open(filename) as file:
                    content = self._read_file(file, flagged)
                    result.append(content)
            except FileNotFoundError:
                try:
                    with open(os.path.join(os.getcwd(), "my_file.txt"), "r") as f:
                        content = f.read()
                        result.append(content)
                except FileNotFoundError:
                    raise FileNotFoundError(f"No such file: {filename}")

        output = ""
        for file_output in result:
            output.join(file_output)

        return output

    @staticmethod
    def _read_file(file, flag) -> list:
        result = []
        if flag == "-n":
            for index, line in enumerate(file):
                result.append('index ' + line)
        elif flag == "-s":
            lines = [i for i in file.readlines() if i]
            result = lines
        else:
            result = file.readlines()

        return result
