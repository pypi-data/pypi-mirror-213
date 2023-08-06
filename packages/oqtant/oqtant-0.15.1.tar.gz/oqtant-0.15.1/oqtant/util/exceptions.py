class JobReadError(Exception):
    def __init__(self, message):
        super().__init__(message)


class AuthorizationError(Exception):
    def __init__(self, message=None):
        super().__init__(message)


class ValidationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class JobWriteError(Exception):
    pass


class DatabaseError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ParameterError(Exception):
    def __init__(self, message):
        super().__init__(message)


class JobError(Exception):
    pass


class JobPlotFitError(JobError):
    def __init__(self):
        super().__init__(
            "PLOT FIT RESULTS: failed to generate model from provided parameters"
        )


class JobPlotFitMismatchError(JobError):
    def __init__(self):
        super().__init__("PLOT FIT RESULTS: mismatched parameters and model type")


class VersionWarning(Warning):
    def __init__(self, message):
        super().__init__(message)
