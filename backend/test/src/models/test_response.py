from backend.src.models.response import Response
import unittest

class test_response(unittest.TestCase):

    def test_abstract_response(self):
        A= Response('success', 200, [], 'message')
        self.assertEqual(A.data,[])
        self.assertEqual(A.message, 'message')

        A = Response('success', 200, '', 'message')
        self.assertEqual(A.message, 'message')

        A = Response('success', 200, '{}', 'message')
        self.assertEqual(A.message, 'message')

if __name__ =='__main__':
    unittest.main()