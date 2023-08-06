class APIConnectionError(Exception):
    """
    Raised when some error occurs during API connection.
    """

    def __init__(self, message='API connection error'):
        super().__init__(message)


class ConfigFileError(Exception):
    """
    Raised when some error occurs during reading the configuration file.
    """

    def __init__(self, message='Config file error'):
        super().__init__(message)


class Base64Error(Exception):
    """
    Raised when some error occurs during Base64 encoding.
    """

    def __init__(self, message='Base64 error'):
        super().__init__(message)


class AuthenticationError(Exception):
    """
    Raised when user is not authenticated.
    """

    def __init__(self, message='Authentication Error'):
        super().__init__(message)


class ExecutionObjectError(Exception):
    """
    Raised when some error occurs reading an Execution object.
    """

    def __init__(self, message='Execution Object Error'):
        super().__init__(message)