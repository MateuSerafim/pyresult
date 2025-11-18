from enum import Enum
class ErrorType(Enum):
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CRITICAL_ERROR = 500