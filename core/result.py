from __future__ import annotations

from .error_type import ErrorType

class Result():
    def __init__(self, value, error_message: str | None, error_type: ErrorType | None):
        self.value = value
        self.error_message = error_message
        self.error_type = error_type

    def is_ok(self) -> bool:
        return self.value is not None
    
    def is_error(self) -> bool:
        return not self.is_ok()

    @staticmethod
    def successful(value) -> Result: 
        return Result(value, None, None)
    
    @staticmethod
    def failure(message: str, error_type: ErrorType = ErrorType.BAD_REQUEST) -> Result:
        return Result(None, message, error_type)
    
