class APIException(Exception):
    """Base API exception class carrying business code and HTTP status."""
    error_code = 1
    message = "API Error"
    status_code = 400

    def __init__(self, message=None, error_code=None, status_code=None):
        resolved_message = message or self.message
        super().__init__(resolved_message)

        if message is not None:
            self.message = message
        if error_code is not None:
            self.error_code = error_code
        if status_code is not None:
            self.status_code = status_code


class ValidationError(APIException):
    error_code = 1001
    message = "Validation failed"
    status_code = 400
