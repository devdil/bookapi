from backend.src.models.abstract_response import AbstractResponse
import unittest

class test_abstract_response(unittest.TestCase):

    def test_abstract_resposne(self):
        self.assertEqual(AbstractResponse('success', 200).to_dict(),{'status': 'success', 'status_code': 200})


if __name__ =='__main__':
    unittest.main()