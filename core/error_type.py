from enum import Enum
class ErrorType(Enum):
    UNSPECIFIED = 000
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CRITICAL_ERROR = 500

class ResultError():
    """
    Represent a error in an operation.
    Has to principal values:

    - ErrorType
    - ErrorMessage
    """

    __slots__ = ("error_message", "error_type")

    def __init__(self, error_message: str, 
                 error_type: ErrorType = ErrorType.BAD_REQUEST):
        
        self.error_message = error_message
        self.error_type = error_type