import re
from collections import Counter, defaultdict
from copy import deepcopy

from src.commandParse.parseExceptions import AssignmentError, PipelineError, ImbalancedQuotesError
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
    command_list_tokens = ['cat', 'wc', 'pwd', 'echo', 'exit']

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
        regex = r"([^\|]*)"
        regex_quotes = r"""([^'"]*)(['"][^'"]*["'])*([^'"]*)"""

        raw_split_pipelines = [i.strip() for i in re.findall(regex, input_string)]
        num_of_pipes = 0
        for i in range(len(raw_split_pipelines) - 1):
            if raw_split_pipelines[i] != '' and raw_split_pipelines[i + 1] == '':
                continue
            num_of_pipes += 1

        split_pipelines = [i for i in raw_split_pipelines if i]
        pipelines_content = {k: v for k, v in enumerate(split_pipelines)}

        if num_of_pipes >= len(split_pipelines):
            raise PipelineError("Wrong pipeline syntax: empty pipeline detected.")

        for k, v in pipelines_content.items():
            if not v:
                raise PipelineError("Missing correct command in pipeline.")

        pipelines = {}

        if not split_pipelines or not split_pipelines[0]:
            raise PipelineError("Missing correct command in pipeline.")

        for order, elem in pipelines_content.items():
            command = elem.split()[0]

            if "let" in command or "=" in command or "$" in command:
                continue

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
            if not val:
                str_to_change = str_to_change.replace("$" + var, "", 1)
            else:
                substitute_dict[var] = val

        substitute_dict = {k: v for k, v in substitute_dict.items() if k}
        for var, values in substitute_dict.items():
            if values:
                regex = r"""("\$""" + var + r"\""")|(?!\')\$""" + var + r"""(?!\')"""
                str_to_change = re.sub(regex, str(values[-1]), str_to_change, c[var])
                str_to_change = re.sub("\\s+", ' ', str_to_change)

        regex_single_quote = r"""[\'][^\']*"""
        regex_double_quote = r"""[\"][^\"]*"""
        split_single_quote = re.split(regex_single_quote, str_to_change)
        split_double_quote = re.split(regex_double_quote, str_to_change)

        for i in range(len(split_single_quote)):
            if i == len(split_single_quote) - 1:
                if split_single_quote[i] == '' and split_single_quote[i - 1] != '':
                    raise ImbalancedQuotesError("Imbalanced single quote met.")
            else:
                if split_single_quote[i] == '':
                    if split_single_quote[i + 1] == '':
                        str_to_change = str_to_change.replace("'", '', 2)
                        continue
                    else:
                        raise ImbalancedQuotesError("Imbalanced single quote met.")

        for i in range(len(split_double_quote)):
            if i == len(split_double_quote) - 1:
                if split_double_quote[i] == '' and split_double_quote[i - 1] != '':
                    raise ImbalancedQuotesError("Imbalanced double quote met.")
            else:
                if split_double_quote[i] == '':
                    if split_double_quote[i + 1] == '':
                        str_to_change = str_to_change.replace('"', '', 2)
                        continue
                    else:
                        raise ImbalancedQuotesError("Imbalanced double quote met.")

        str_to_change = " ".join(str_to_change.split())
        str_to_change = str_to_change.strip()
        return str_to_change
