from collections import defaultdict
from src.env.envExceptions import MissingVariableError


class Environment:
    """
    Environment class to access assigned variables via env.
    """
    def __init__(self):
        self.__env_vars = defaultdict(list)

    def get_var(self, var):
        res = self.__env_vars[var]
        if not res:
            raise MissingVariableError(f"No such variable in environment: {var}")
        return res

    def set_var(self, var, val):
        self.__env_vars[var].append(val)
