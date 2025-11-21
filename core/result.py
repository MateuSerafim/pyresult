from __future__ import annotations
from typing import Generic, TypeVar, Callable
from .error_type import ErrorType, ResultError

DEFAULT_NOT_FOUND_MESSAGE = "Value not found!"
DEFAULT_UNKNOWN_ERROR_MESSAGE = "Unknown error message!"

T = TypeVar("T")
U = TypeVar("U")

class Result(Generic[T]):
    """
    Result object basead in Result Pattern. 
    
    Define only to scenarios for one operation: **Success** and **Fail**.
    
    - On **success**, the object can contain a value resulting of operation.
    - In case of **fail**, the object can be take a list of errors.
    """

    __slots__ = ("value", "errors")

    value: T | None
    errors: list[ResultError] | None

    @property
    def is_ok(self) -> bool:
        return self.value is not None

    @property
    def is_error(self) -> bool:
        return not self.is_ok

    @staticmethod
    def successful(value: T | None = None) -> Result[T]:
        """
        Generate a Result ok with value **T**.
        
        Args:
            value (T nullable): value of operation result.

        Returns:
            Result[T]:

        .. warning:: In case of a **None** value has passed, the value is a boolean **True**.
        """

        self = object.__new__(Result)
        
        self.value = True if value is None else value
        self.errors = None
        
        return self
    
    @staticmethod
    def failure(error_message: str, 
                error_type: ErrorType = ErrorType.BAD_REQUEST) -> Result[T]:
        """
        Generate a Result fail with one error.
        
        Args:
            error_message (str): text with error informations.
            error_type (ErrorType): type of error. Default is BAD_REQUEST.

        Returns:
            Result[T]:
        """

        self = object.__new__(Result)
        
        self.value = None
        self.errors = [ResultError(error_message, error_type)]

        return self
    
    @staticmethod
    def failures(errors: list[ResultError]) -> Result[T]:
        """
        Generate a Result fail with a list of errors.
        
        Args:
            errors (list[ResultError]): list of errors.

        Returns:
            Result[T]:

        .. warning:: When a empty list or None value, the result has one basic error **UNSPECIFIED**.
        """

        if (errors is None or len(errors) == 0):
            return Result.failure(DEFAULT_UNKNOWN_ERROR_MESSAGE, ErrorType.UNSPECIFIED)
        
        self = object.__new__(Result)
        
        self.value = None
        self.errors = errors

        return self
    
    @staticmethod
    def maybe(value: T | None, 
              error_message: str = DEFAULT_NOT_FOUND_MESSAGE) -> Result[T]:
        """
        Generate a Result for a possible value.
        In case of value is None, return Result with Fail and error **NOT_FOUND**.

        Args:
            value (T nullable): a maybe value to verify in result construction.
            error_message(str): message in case of fail scenario.

        Returns:
            Result[T]:
        """

        if (value is None):
            return Result.failure(error_message, ErrorType.NOT_FOUND)
        
        return Result.successful(value)
    
    def map(self, func: Callable[[T], U]) -> Result[U]:
        """
        Apply a function with return **U** to a value **T**.

        Args:
            func: function(T) -> U

        Returns:
            Result[U]:
        """
                
        if (self.is_error):
            return Result.failures(self.errors)
        
        try:
            new_value = func(self.value)
            return Result.successful(new_value)
        
        except Exception as e:
            return Result.failure(str(e), ErrorType.BAD_REQUEST)
        
    def bind(self, func: Callable[[T], Result[U]]) -> Result[U]:
        """
        Apply a function with return **Result[U]** to a value **T**.

        Args:
            func: function(T) -> Result[U]

        Returns:
            Result[U]:
        """
        if (self.is_error):
            return Result.failures(self.errors)
        
        return func(self.value)
        