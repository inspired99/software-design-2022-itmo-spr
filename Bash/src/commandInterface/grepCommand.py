import os
import re

from src.commandInterface.command import Command
from src.commandInterface.commandExceptions import FlagError


class Grep(Command):
    """
    Searches for pattern inside file or files and displays strings,
    which contain it.
    First argument has to be a pattern.
    Other arguments can be files or arguments from pipeline.
    Flags:
    -i -> ignored-case matching
    -w -> only if the word matches
    -A [NUM] -> print NUM lines after matched string
    """
    flags = ['-i', '-w', '-A']
    pattern = ''

    @staticmethod
    def invoke(args: list) -> str:
        args += Grep.args_previous
        if not args:
            raise FileNotFoundError('No files to read from.')
        Grep.pattern = ''
        flagged = Command._flagged(Grep.flags, args)

        output = []

        files, optional = Grep.split_flags_args(args, flagged)

        for filename in files:
            if Grep.from_pipeline:
                file_content = filename
            else:
                file_content = Grep.read_file(filename)

            if not flagged:
                res = Grep.search_in_text(file_content, Grep.pattern, "")

                output.extend(res)
            else:
                output = file_content
                for flag in flagged:
                    if optional:
                        optional = int(optional)
                        num = optional
                        output = (Grep.search_in_text(output, Grep.pattern, flag, num))
                    else:
                        output = (Grep.search_in_text(output, Grep.pattern, flag))

        return "".join(output).rstrip()

    @staticmethod
    def split_flags_args(args, flags) -> tuple:
        args_without_flags = [i for i in args if i not in flags]
        optional = 0

        if len(args_without_flags) < 2:
            raise FileNotFoundError('No file or pattern provided for grep.')

        if "-A" in flags:
            Grep.pattern = args_without_flags[1]
            files = args_without_flags[2:]
            optional = args_without_flags[0]
            if not optional.isnumeric() or int(optional) < 0:
                raise FlagError("Wrong option for flag A.")

        else:
            Grep.pattern = args_without_flags[0]
            files = args_without_flags[1:]

        return files, optional

    @staticmethod
    def search_in_text(text_content: list, pattern: str, flag: str, optional=0) -> list:
        result = []
        if not list:
            return result

        if isinstance(text_content, str):
            text_content = [text_content]

        if not flag:
            result = [i for i in text_content if pattern in i]
            return result

        if flag == "-i":
            result = [i for i in text_content if pattern.lower() in i.lower()]

        if flag == "-w":
            regex_word = re.compile(r"\b" + pattern + r"\b")
            result = [i for i in text_content if re.findall(regex_word, i)]

        if flag == "-A":
            num = 0
            for line in text_content:
                if int(num) > 0:
                    result.append(line)
                    num -= 1

                    if pattern in line:
                        num = optional
                    continue

                if pattern in line:
                    result.append(line)
                    num = optional

        if not result:
            result = [i for i in text_content if re.findall(pattern, i)]

        return result

    @staticmethod
    def read_file(filename) -> list:
        result = []
        try:
            with open(filename) as file:
                content = file.readlines()
        except FileNotFoundError:
            try:
                with open("".join((os.getcwd(), filename))) as f:
                    content = f.readlines()
            except FileNotFoundError:
                raise FileNotFoundError(f"No such file: {filename}")

        result.extend(content)
        return result
