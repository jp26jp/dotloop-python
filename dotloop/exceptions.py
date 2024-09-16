class DotloopAPIException(Exception):
    """
    Custom exception class for Dotloop API errors.
    """

    def __init__(self, message: str, status_code: int = None, error_code: str = None):
        """
        Initialize the DotloopAPIException.

        Args:
            message (str): The error message.
            status_code (int, optional): The HTTP status code associated with the error.
            error_code (str, optional): The Dotloop-specific error code, if available.
        """
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

    def __str__(self):
        """
        String representation of the exception.
        """
        error_str = f"DotloopAPIException: {self.message}"
        if self.status_code:
            error_str += f" (Status Code: {self.status_code})"
        if self.error_code:
            error_str += f" (Error Code: {self.error_code})"
        return error_str


class DotloopAuthException(DotloopAPIException):
    """
    Exception for authentication-related errors.
    """

    def __init__(self, message: str, status_code: int = 401):
        super().__init__(message, status_code)


class DotloopRateLimitException(DotloopAPIException):
    """
    Exception for rate limiting errors.
    """

    def __init__(self, message: str, status_code: int = 429):
        super().__init__(message, status_code)


class DotloopNotFoundException(DotloopAPIException):
    """
    Exception for resource not found errors.
    """

    def __init__(self, message: str, status_code: int = 404):
        super().__init__(message, status_code)
