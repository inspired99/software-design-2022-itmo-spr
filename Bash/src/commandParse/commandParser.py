import re
from copy import deepcopy

from src.commandInterface.command import Command
from src.commandParse.parseExceptions import PipelineError, AssignmentError
from src.env.env import Environment


class CommandParser:
    """
    Class which is responsible for parsing commands
    from standard input.
    """
    def __init__(self):
        self.env = Environment()

    @staticmethod
    def parse_bind(input_string: str) -> tuple:
        """
        Method which takes string and returns
        assignments of variables (using "let" or "=").
        :param input_string: raw string to find assignments
        :return: tuple with assignments of var name and it's value
        """
        is_present = "=" in input_string
        regex_eq = r"([^=]*\S)=([^=\s]*)"
        regex_let = r"let\s(\w*)=([^=\s]*)"

        if not is_present:
            return tuple()

        assignments_eq = [(i[0].strip(), i[1].strip()) for i in re.findall(regex_eq,
                                                                           input_string) if "let" not in i[0]]

        assignments_let = [(i[0].strip(), i[1].strip()) for i in re.findall(regex_let,
                                                                            input_string)]

        if is_present and not assignments_eq and not assignments_let:
            raise AssignmentError("Wrong assignment syntax.")

        for i in assignments_eq, assignments_let:
            for j in i:
                if (j[0] and not j[1]) or (j[1] and not j[0]):
                    raise AssignmentError("Wrong assignment syntax.")

        # implement subst
        return assignments_eq, assignments_let

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
                    args = val.replace(command_name, "").replace("'", "").replace('"', '').strip()
                    command_dict[key] = (command_name, args)

            if not is_command:
                raise PipelineError("Missing correct command in pipeline.")
        return command_dict

    def subst_vars(self, input_string: str) -> str:
        """
        Substitution of variables from environment via dollar sign.
        :param input_string: raw string.
        :return: string with replaced vars with their values.
        """
        str_to_change = deepcopy(input_string)
        regex_dollar_sign = r"(\$[^*]\w*)"
        regex_dollar_sign_and_quotes = r"('\$[^*]\w*')|(\$[^*]\w*)"
        replace_dict = {"$": "", '"': ''}

        ord_quoted = re.findall(regex_dollar_sign_and_quotes, input_string)
        to_subst = re.findall(regex_dollar_sign, input_string)

        for k, v in replace_dict.items():
            to_subst = [i.replace(k, v) for i in to_subst]
            ord_quoted = [(i[0].replace(k, v), i[1].replace(k, v)) for i in ord_quoted]

        to_subst = [i.strip() for i in to_subst if i]
        ord_quoted = [(i[0].strip(), i[1].strip()) for i in ord_quoted if i]

        substitute_dict = {}

        for var in to_subst:
            for symbol in ord_quoted:
                if var not in symbol[0]:
                    val = self.env.get_var(var)
                    substitute_dict[var] = val
                substitute_dict[symbol[0]] = [var]

        substitute_dict = {k: v for k, v in substitute_dict.items() if k}

        for var, values in substitute_dict.items():
            if values:
                if "'" in var:
                    str_to_change = str_to_change.replace(str(values[-1]), "'" + str(values[-1]) + "'", 1)
                str_to_change = str_to_change.replace("$" + var, str(values[-1]), 1)

        str_to_change = str_to_change.replace("'", '$', 1)
        str_to_change = str_to_change.replace("'", '')
        str_to_change = str_to_change.replace('"', '')

        return str_to_change
