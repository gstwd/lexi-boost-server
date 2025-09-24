class APIException(Exception):
    """Base API exception class - all API responses use HTTP 200 with business error codes"""
    error_code = 1
    message = "API Error"

    def __init__(self, message=None, error_code=None):
        super().__init__()
        if message is not None:
            self.message = message
        if error_code is not None:
            self.error_code = error_code

class ValidationError(APIException):
    error_code = 1001
    message = "Validation failed"

class NotFoundError(APIException):
    error_code = 1002
    message = "Resource not found"

class DatabaseError(APIException):
    error_code = 1003
    message = "Database operation failed"

class AuthenticationError(APIException):
    error_code = 1004
    message = "Authentication failed"

class AuthorizationError(APIException):
    error_code = 1005
    message = "Access denied"