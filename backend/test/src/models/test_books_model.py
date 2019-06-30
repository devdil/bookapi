from backend.src.models.books_model import Books
import unittest

class test_abstract_response(unittest.TestCase):

    def test_abstract_resposne(self):
        B = Books()
        self.assertIsInstance(B, Books)


if __name__ =='__main__':
    unittest.main()