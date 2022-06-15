import os

from src.commandInterface.command import Command


class Cat(Command):
    """
    Display the content of file.
    Flags:
    -n -> numbers of lines.
    -s -> omit blank lines
    """
    flags = ['-s', '-n']

    @staticmethod
    def invoke(args) -> str:

        if not args:
            raise FileNotFoundError("No files to read from.")

        flagged = Command._flagged(Cat.flags, args)
        files = args
        result = Cat._read_files(files, flagged)
        output = "".join(result)

        return output

    @staticmethod
    def _extract_context(file, flags) -> list:
        result = file.readlines()
        if not flags:
            return result

        for flag in flags:
            cur_result = []
            if flag == "-s":
                lines = [i for i in result if i != '\n' and i != '']
                cur_result.extend(lines)

            if flag == "-n":
                ind = 1
                temp_data = []
                if not cur_result:
                    cur_result = result

                for line in cur_result:
                    line = (f'{ind} ' + line)
                    ind += 1
                    temp_data.append(line)
                cur_result = temp_data

            result = cur_result

        return result

    @staticmethod
    def _read_files(files, flags: list) -> list:
        result = []

        for filename in files:
            if Cat.from_pipeline:
                Cat.from_pipeline = False
                return filename

            if filename not in flags:
                content = []
                try:
                    with open(filename) as file:
                        content = Cat._extract_context(file, flags)
                except FileNotFoundError:
                    try:
                        if not content:
                            with open("".join((os.getcwd(), filename))) as f:
                                content = Cat._extract_context(f, flags)
                    except FileNotFoundError:
                        raise FileNotFoundError(f"No such file: {filename}")
                result += content

        return result
