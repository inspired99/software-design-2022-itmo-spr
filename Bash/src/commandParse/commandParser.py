import re
from collections import Counter
from copy import deepcopy

from src.commandInterface.command import Command
from src.commandParse.parseExceptions import PipelineError, AssignmentError
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
        split_pipelines = [i.strip() for i in re.findall(regex, input_string) if i]

        pipelines_content = {k: v for k, v in enumerate(split_pipelines)}
        command_dict = {}
        command_list = Command.command_list + ['let', '=']

        for key, val in pipelines_content.items():
            is_command = False
            for command_name in command_list:
                if command_name == "=" and "=" in input_string:
                    is_command = True
                if command_name == "let" and "let" in input_string:
                    is_command = True

                if command_name in val.split():
                    is_command = True
                    args = val.replace(command_name, "", 1)
                    replace_dict = {"'": "", '"': ''}
                    for k, v in replace_dict.items():
                        args = args.replace(k, v)
                    args = args.strip()
                    command_dict[key] = (command_name, args)

            if not is_command:
                raise PipelineError("Missing correct command in pipeline.")
        return command_dict

    def subst_vars(self, input_string: str) -> str:
        """
        Substitution of variables from environment via dollar sign.
        :param input_string: raw string.
        :return: string with replaced vars with their values from env.
        """
        str_to_change = deepcopy(input_string)
        regex_dollar_sign = r"([^']\$\w*)"

        replace_dict = {"$": "", '"': ''}
        indexes_to_change = []
        for ind in re.finditer(regex_dollar_sign, str_to_change):
            indexes_to_change.append((ind.start(), ind.end()))

        to_subst = re.findall(regex_dollar_sign, input_string)
        for k, v in replace_dict.items():
            to_subst = [i.replace(k, v) for i in to_subst]

        to_subst = [i.strip() for i in to_subst if i]

        substitute_dict = {}
        c = Counter(to_subst)

        for var in set(to_subst):
            val = self.env.get_var(var)
            substitute_dict[var] = val

        substitute_dict = {k: v for k, v in substitute_dict.items() if k}

        for var, values in substitute_dict.items():
            if values:
                regex = r'[\s^"]\$' + var + r"""[\S]*"""
                str_to_change = re.sub(regex, " " + str(values[-1]), str_to_change, c[var])
                str_to_change = re.sub("\\s+", ' ', str_to_change)

        stop_symbols = ["'", '"']
        for symbol in stop_symbols:
            str_to_change = str_to_change.replace(symbol, '')

        return str_to_change
