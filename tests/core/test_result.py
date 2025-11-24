import unittest
from core.result import Result, DEFAULT_UNKNOWN_ERROR_MESSAGE, DEFAULT_NOT_FOUND_MESSAGE
from core.error_type import ErrorType, ResultError

class ResultTests(unittest.TestCase):

    ANY_STRING_VALUE = "any string value"
    ANY_INT_VALUE = 2
    ANY_BOOL_VALUE = True

    ERROR_MESSAGE_FAIL = "Any message failure"
    ANY_MESSAGE_NOT_FOUND = "User not found"
    
    def test_create_result_success_type_1(self):
        result = Result.successful(ResultTests.ANY_STRING_VALUE)
        
        self.assertTrue(result.is_ok)
        self.assertFalse(result.is_error)

        self.assertEqual(ResultTests.ANY_STRING_VALUE, result.value)
        self.assertIsNone(result.errors)

    def test_create_result_success_type_2(self):
        result = Result.successful(ResultTests.ANY_INT_VALUE)
        
        self.assertTrue(result.is_ok)
        self.assertFalse(result.is_error)

        self.assertEqual(ResultTests.ANY_INT_VALUE, result.value)
        self.assertIsNone(result.errors)
    
    def test_create_result_success_type_3(self):
        result = Result.successful()
        
        self.assertTrue(result.is_ok)
        self.assertFalse(result.is_error)

        self.assertEqual(ResultTests.ANY_BOOL_VALUE, result.value)
        self.assertIsNone(result.errors)

    def test_create_result_fail_1(self):
        result = Result.failure(ResultTests.ERROR_MESSAGE_FAIL)

        self.assertTrue(result.is_error)
        self.assertFalse(result.is_ok)

        self.assertIsNone(result.value)

        self.assertEqual(ResultTests.ERROR_MESSAGE_FAIL, result.errors[0].error_message)
        self.assertEqual(ErrorType.BAD_REQUEST, result.errors[0].error_type)

    def test_create_result_fail_2(self):
        result = Result.failure(ResultTests.ERROR_MESSAGE_FAIL, ErrorType.CRITICAL_ERROR)

        self.assertTrue(result.is_error)
        self.assertFalse(result.is_ok)

        self.assertIsNone(result.value)

        self.assertEqual(ResultTests.ERROR_MESSAGE_FAIL, result.errors[0].error_message)
        self.assertEqual(ErrorType.CRITICAL_ERROR, result.errors[0].error_type)
    
    def test_create_result_fails_1(self):
        result = Result.failures([])

        self.assertTrue(result.is_error)
        self.assertFalse(result.is_ok)

        self.assertIsNone(result.value)

        self.assertEqual(DEFAULT_UNKNOWN_ERROR_MESSAGE, result.errors[0].error_message)
        self.assertEqual(ErrorType.UNSPECIFIED, result.errors[0].error_type)

    def test_create_result_fails_2(self):
        result = Result.failures(None)

        self.assertTrue(result.is_error)
        self.assertFalse(result.is_ok)

        self.assertIsNone(result.value)

        self.assertEqual(DEFAULT_UNKNOWN_ERROR_MESSAGE, result.errors[0].error_message)
        self.assertEqual(ErrorType.UNSPECIFIED, result.errors[0].error_type)
    
    def test_create_result_fails_3(self):
        result = Result.failures()

        self.assertTrue(result.is_error)
        self.assertFalse(result.is_ok)

        self.assertIsNone(result.value)

        self.assertEqual(DEFAULT_UNKNOWN_ERROR_MESSAGE, result.errors[0].error_message)
        self.assertEqual(ErrorType.UNSPECIFIED, result.errors[0].error_type)

    def test_create_result_fails_4(self):
        errors = [ResultError("message 1"), 
                  ResultError("message 2", ErrorType.FORBIDDEN)]
        result = Result.failures(errors)

        self.assertTrue(result.is_error)
        self.assertFalse(result.is_ok)

        self.assertIsNone(result.value)
        self.assertEqual(len(errors), len(result.errors))

        self.assertEqual("message 1", result.errors[0].error_message)
        self.assertEqual(ErrorType.BAD_REQUEST, result.errors[0].error_type)

        self.assertEqual("message 2", result.errors[1].error_message)
        self.assertEqual(ErrorType.FORBIDDEN, result.errors[1].error_type)

    def test_create_result_maybe_type_1(self):
        result = Result.maybe(ResultTests.ANY_STRING_VALUE)
        
        self.assertTrue(result.is_ok)
        self.assertFalse(result.is_error)

        self.assertEqual(ResultTests.ANY_STRING_VALUE, result.value)
        self.assertIsNone(result.errors)

    def test_create_result_maybe_type_2(self):
        result = Result.maybe()
        
        self.assertTrue(result.is_error)
        self.assertFalse(result.is_ok)

        self.assertIsNone(result.value)
        self.assertEqual(len([1]), len(result.errors))

        self.assertEqual(DEFAULT_NOT_FOUND_MESSAGE, result.errors[0].error_message)
        self.assertEqual(ErrorType.NOT_FOUND, result.errors[0].error_type)

    def test_create_result_maybe_type_3(self):
        result = Result.maybe(None)
        
        self.assertTrue(result.is_error)
        self.assertFalse(result.is_ok)

        self.assertIsNone(result.value)
        self.assertEqual(len([1]), len(result.errors))

        self.assertEqual(DEFAULT_NOT_FOUND_MESSAGE, result.errors[0].error_message)
        self.assertEqual(ErrorType.NOT_FOUND, result.errors[0].error_type)

    def test_create_result_maybe_type_4(self):
        result = Result.maybe(None, ResultTests.ANY_MESSAGE_NOT_FOUND)
        
        self.assertTrue(result.is_error)
        self.assertFalse(result.is_ok)

        self.assertIsNone(result.value)
        self.assertEqual(len([1]), len(result.errors))

        self.assertEqual(ResultTests.ANY_MESSAGE_NOT_FOUND, result.errors[0].error_message)
        self.assertEqual(ErrorType.NOT_FOUND, result.errors[0].error_type)
    
    @staticmethod
    def __self_power__(value: int) -> int:
        return value * value
    
    def __substract_two__(value: int) -> int:
        return value - 2

    def test_result_map_1(self):
        result = Result[int].successful(2)

        op_result = result.map(ResultTests.__self_power__)

        self.assertTrue(op_result.is_ok)
        self.assertFalse(op_result.is_error)

        self.assertEqual(4, op_result.value)
        self.assertIsNone(op_result.errors)

    def test_result_map_2(self):
        result = Result[int].successful(2)

        op_result = result.map(ResultTests.__self_power__)\
                          .map(ResultTests.__substract_two__)

        self.assertTrue(result.is_ok)
        self.assertFalse(result.is_error)

        self.assertEqual(2, op_result.value)
        self.assertIsNone(op_result.errors)

    def test_result_map_3(self):
        result = Result[int].successful("a")

        op_result = result.map(ResultTests.__substract_two__)

        self.assertTrue(op_result.is_error)
        self.assertFalse(op_result.is_ok)

        self.assertIsNone(op_result.value)
        self.assertEqual(len([1]), len(op_result.errors))

        self.assertEqual("unsupported operand type(s) for -: \'str\' and \'int\'", 
                         op_result.errors[0].error_message)
        self.assertEqual(ErrorType.BAD_REQUEST, op_result.errors[0].error_type)

    def test_result_map_4(self):
        result = Result[int].successful("a")

        op_result = result.map(ResultTests.__substract_two__)\
                          .map(ResultTests.__self_power__)

        self.assertTrue(op_result.is_error)
        self.assertFalse(op_result.is_ok)

        self.assertIsNone(op_result.value)
        self.assertEqual(len([1]), len(op_result.errors))

        self.assertEqual("unsupported operand type(s) for -: \'str\' and \'int\'", 
                         op_result.errors[0].error_message)
        self.assertEqual(ErrorType.BAD_REQUEST, op_result.errors[0].error_type)

    def test_result_map_5(self):
        result = Result[int].failures()

        op_result = result.map(ResultTests.__substract_two__)\
                          .map(ResultTests.__self_power__)

        self.assertTrue(op_result.is_error)
        self.assertFalse(op_result.is_ok)

        self.assertIsNone(op_result.value)
        self.assertEqual(len([1]), len(op_result.errors))

        self.assertEqual(DEFAULT_UNKNOWN_ERROR_MESSAGE, op_result.errors[0].error_message)
        self.assertEqual(ErrorType.UNSPECIFIED, op_result.errors[0].error_type)

    VALUE_CANNOT_BE_NULL = "Value cannot be null"
    VALUE_NEED_BE_INTEGER = "Value need to be integer"

    @staticmethod
    def __multiple_by__(value: int, factor: int = 1) -> Result[int]:
        if (value is None):
            return Result.failure(ResultTests.VALUE_CANNOT_BE_NULL)

        if (type(value) != int):
            return Result.failure(ResultTests.VALUE_NEED_BE_INTEGER)
        
        return Result.successful(value * factor)
    
    @staticmethod
    def __to_string__(value: int) -> Result[str]:
        return Result[str].successful(str(value))

    def test_result_bind_1(self):
        result = Result[int].successful(2)

        op_result = result.bind(ResultTests.__multiple_by__)

        self.assertTrue(op_result.is_ok)
        self.assertFalse(op_result.is_error)

        self.assertEqual(2, op_result.value)
        self.assertIsNone(op_result.errors)

        self.assertEqual(2, result.value)

    def test_result_bind_2(self):
        result = Result[int].successful(2)

        op_result = result.bind(lambda r: ResultTests.__multiple_by__(r, 5))

        self.assertTrue(op_result.is_ok)
        self.assertFalse(op_result.is_error)

        self.assertEqual(10, op_result.value)
        self.assertIsNone(op_result.errors)

        self.assertEqual(2, result.value)

    def test_result_bind_3(self):
        result = Result[int].failures()

        op_result = result.bind(ResultTests.__to_string__)

        self.assertTrue(op_result.is_error)
        self.assertFalse(op_result.is_ok)

        self.assertIsNone(op_result.value)
        self.assertEqual(len([1]), len(op_result.errors))

        self.assertEqual(DEFAULT_UNKNOWN_ERROR_MESSAGE, op_result.errors[0].error_message)
        self.assertEqual(ErrorType.UNSPECIFIED, op_result.errors[0].error_type)
    
    def test_result_bind_4(self):
        result = Result[str].successful("Joao")\
                            .map(lambda r: User.create(r))\
                            .bind(lambda user: user.set_name("Bruno"))
        
        self.assertTrue(result.is_ok)
        self.assertFalse(result.is_error)

        self.assertEqual(User, type(result.value))
        self.assertIsNone(result.errors)

        self.assertEqual("Bruno", result.value.name)
    
    def test_result_bind_5(self):
        result = Result.successful("Joao")\
                        .map(lambda r: User.create(r))\
                        .bind(lambda user: user.set_name("Bruno"))\
                        .map(lambda user: user.len_name())\
                        .map(ResultTests.__substract_two__)
        
        self.assertTrue(result.is_ok)
        self.assertFalse(result.is_error)

        self.assertEqual(int, type(result.value))
        self.assertIsNone(result.errors)

        self.assertEqual(3, result.value)

class User():

    NAME_CANNOT_BE_NULL = "Name cannot be null"
    
    def __init__(self, name: str):
        self.name = name
    
    @staticmethod
    def create(name: str) -> "User":
        return User(name)
    
    def set_name(self, name: str) -> Result["User"]:
        if (name is None):
            return Result.failure(NAME_CANNOT_BE_NULL)
        
        self.name = name

        return Result.successful(self)

    def len_name(self) -> int:
        return len(self.name)    

if __name__ == "__main__":
    unittest.main()