class APIException(Exception):
    status_code = 400
    error_code = 1
    message = "API Error"

    def __init__(self, message=None, status_code=None, error_code=None):
        super().__init__()
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        if error_code is not None:
            self.error_code = error_code

class ValidationError(APIException):
    status_code = 400
    error_code = 1001
    message = "Validation failed"

class NotFoundError(APIException):
    status_code = 404
    error_code = 1002
    message = "Resource not found"

class DatabaseError(APIException):
    status_code = 500
    error_code = 1003
    message = "Database operation failed"

class AuthenticationError(APIException):
    status_code = 401
    error_code = 1004
    message = "Authentication failed"

class AuthorizationError(APIException):
    status_code = 403
    error_code = 1005
    message = "Access denied"