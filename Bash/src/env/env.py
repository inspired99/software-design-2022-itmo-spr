from collections import defaultdict


class Environment:
    """
    Environment class to access assigned variables via env.
    """

    def __init__(self):
        self.__env_vars = defaultdict(list)

    def get_var(self, var):
        res = self.__env_vars[var]
        if not res:
            return ""
        return res

    def set_var(self, var, val):
        self.__env_vars[var].append(val)
        
