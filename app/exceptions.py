class APIException(Exception):
    """Base API exception class carrying business code and HTTP status."""
    error_code = 1
    message = "API Error"
    def __init__(self, message=None, error_code=None):
        resolved_message = message or self.message
        super().__init__(resolved_message)

        if message is not None:
            self.message = message
        if error_code is not None:
            self.error_code = error_code

class ValidationError(APIException):
    error_code = 1001
    message = "Validation failed"