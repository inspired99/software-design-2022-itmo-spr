import re
from collections import Counter, defaultdict
from copy import deepcopy

from src.commandInterface.command import Command
from src.commandParse.parseExceptions import AssignmentError, CommandNotFoundError, PipelineError
from src.env.env import Environment


class CommandParser:
    """
    This class is responsible for parsing commands
    from standard input with following steps:
    1) Make substitutions from environment
    2) Parse ordered pipelines
    3) Parse commands inside each pipeline
    4) Parse bindings to update or add variables inside environment
    """

    def __init__(self):
        self.env = Environment()

    def parse_bind(self, input_string: str) -> None:
        """
        Method which takes string and returns
        assignments of variables (using "let" or "=").
        :param input_string: raw string to find assignments
        :return: tuple with assignments of var name and it's value
        """
        input_string = deepcopy(input_string)
        is_present = "=" in input_string
        regex_eq = r"([^=]*\S)=([^=\s]*)"
        regex_let = r"let\s(\w*)=([^=\s]*)"

        if not is_present:
            return

        assignments_eq = [(i[0].strip(), i[1].strip()) for i in re.findall(regex_eq,
                                                                           input_string) if "let" not in i[0]]

        assignments_let = [(i[0].strip(), i[1].strip()) for i in re.findall(regex_let,
                                                                            input_string)]
        indexes_eq = []
        for index_eq in re.finditer(regex_eq, input_string):
            indexes_eq.append(index_eq.end())

        indexes_let = []
        for index_let in re.finditer(regex_let, input_string):
            indexes_let.append(index_let.end())

        if is_present and not assignments_eq and not assignments_let:
            raise AssignmentError("Wrong assignment syntax.")

        for i in assignments_eq, assignments_let:
            for j in i:
                if (j[0] and not j[1]) or (j[1] and not j[0]):
                    raise AssignmentError("Wrong assignment syntax.")

        if max(indexes_eq + [0]) > max(indexes_let + [0]):
            for assignment in assignments_let:
                self.env.set_var(assignment[0], assignment[1])
            for assignment in assignments_eq:
                self.env.set_var(assignment[0], assignment[1])
        else:
            for assignment in assignments_eq:
                self.env.set_var(assignment[0], assignment[1])
            for assignment in assignments_let:
                self.env.set_var(assignment[0], assignment[1])

        return

    @staticmethod
    def parse_pipelines_and_commands(input_string: str) -> dict:
        """
        Method to parse pipelines regarding to their
        order and content - commands and arguments.
        :param input_string: raw string to find pipelines
        :return: dict with order of pipeline and it's content
        """
        if not input_string.strip():
            return {}
        regex = r"([^|]*)"
        command_list = Command.command_list + ['let', '=', "$"]
        regex_quotes = r"""([^'"]*)(['"][^'"]*["'])*([^'"]*)"""

        split_pipelines = [i.strip() for i in re.findall(regex, input_string) if i]
        pipelines_content = {k: v for k, v in enumerate(split_pipelines)}
        for k, v in pipelines_content.items():
            if not v:
                raise PipelineError("Missing correct command in pipeline.")

        pipelines = {}

        if not split_pipelines or not split_pipelines[0]:
            raise PipelineError("Missing correct command in pipeline.")

        for order, elem in pipelines_content.items():
            command = elem.split()[0]
            is_command = False
            if command in command_list:
                is_command = True

            if "let" in command or "=" in command or "$" in command:
                continue

            if not is_command:
                raise CommandNotFoundError(f"Command not found: {command}")

            elem = elem.replace(command, '', 1)
            all_args = re.findall(regex_quotes, elem)
            args = []
            for tuple_arg in all_args:
                for arg in tuple_arg:
                    if arg.strip():
                        args.append(arg.strip())

            pipelines[(command, order)] = args

        command_dict = defaultdict(list)

        replace_dict = {"'": '', '"': ""}
        for command, args in pipelines.items():
            cleaned_args = []
            for arg in args:
                to_be_replaced = False
                for k, v in replace_dict.items():
                    if k in arg:
                        to_be_replaced = True
                        arg_start = arg.find(k)
                        arg = arg.replace(k, v, 1)
                        arg_end = arg.find(k)
                        new_arg = arg[arg_start:arg_end]
                        new_arg = new_arg.replace(k, v, 1)
                        cleaned_args.append(new_arg)

                if not to_be_replaced:
                    cleaned_args.extend(arg.split())
            command_dict[command].extend(cleaned_args)

        return command_dict

    def subst_vars(self, input_string: str) -> str:
        """
        Substitution of variables from environment via dollar sign.
        :param input_string: raw string.
        :return: string with replaced vars with their values from env.
        """
        str_to_change = " " + (deepcopy(input_string))
        regex_dollar_sign = r"([^']\$[\S]*)"
        replace_dict = {"$": " ", '"': ' '}
        to_subst = re.findall(regex_dollar_sign, str_to_change)
        for k, v in replace_dict.items():
            to_subst = [i.replace(k, v) + " " for i in to_subst]
            to_subst = [i.strip().split() for i in to_subst]
            to_subst = [item for sublist in to_subst for item in sublist]

        substitute_dict = {}
        c = Counter(to_subst)

        for var in set(to_subst):
            val = self.env.get_var(var)
            substitute_dict[var] = val
        substitute_dict = {k: v for k, v in substitute_dict.items() if k}
        for var, values in substitute_dict.items():
            if values:
                regex = r"""("\$""" + var + r""")|(?!\')\$""" + var + r"""(?!\')"""
                str_to_change = re.sub(regex, str(values[-1]), str_to_change, c[var])
                print(str_to_change)
                str_to_change = re.sub("\\s+", ' ', str_to_change)

        stop_symbols = ["'", '"']
        for symbol in stop_symbols:
            str_to_change = str_to_change.replace(symbol, '')

        str_to_change = " ".join(str_to_change.split())
        str_to_change = str_to_change.strip()

        return str_to_change
