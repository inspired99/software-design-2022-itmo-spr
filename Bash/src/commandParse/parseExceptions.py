class ParseException(ValueError):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class PipelineError(ParseException):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class AssignmentError(ParseException):
    def __init__(self, message):
        self.message = message
        super().__init__(message)