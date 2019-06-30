from backend.src.models.messages import ResponseMessages
import unittest

class test_messages(unittest.TestCase):

    def test_response_messages(self):
        self.assertEqual(ResponseMessages().SUCCESS, 'success')
        self.assertEqual(ResponseMessages().FAILED, 'failed')

if __name__ =='__main__':
    unittest.main()