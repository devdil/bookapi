from backend.src.models.error_response import ErrorResponse
import unittest

class test_error_response(unittest.TestCase):

    def test_abstract_resposne(self):
        self.assertEqual(ErrorResponse('success', 200, 'SUCCESS REPORT').to_dict(),
                         {'status': 'success', 'status_code': 200, 'data':[], 'message':'SUCCESS REPORT'})


if __name__ =='__main__':
    unittest.main()