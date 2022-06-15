class ParseException(ValueError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class PipelineError(ParseException):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ImbalancedQuotesError(ParseException):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class AssignmentError(ParseException):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class SubstitutionError(ParseException):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
