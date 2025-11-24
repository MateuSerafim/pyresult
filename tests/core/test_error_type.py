import unittest
from src.error_type import ResultError, ErrorType

class ResultErrorTests(unittest.TestCase):

    ANY_MESSAGE_ERROR = "any message"

    def test_create_result_error(self):
        result_error = ResultError(ResultErrorTests.ANY_MESSAGE_ERROR, 
                                   ErrorType.UNAUTHORIZED)
        
        self.assertEqual(result_error.error_message, ResultErrorTests.ANY_MESSAGE_ERROR)
        self.assertEqual(result_error.error_type, ErrorType.UNAUTHORIZED)

    def test_create_result_error_without_type(self):
        result_error = ResultError(ResultErrorTests.ANY_MESSAGE_ERROR)
        
        self.assertEqual(result_error.error_message, ResultErrorTests.ANY_MESSAGE_ERROR)
        self.assertEqual(result_error.error_type, ErrorType.BAD_REQUEST)

if __name__ == "__main__":
    unittest.main()