from backend.src.utils.common_utils import is_valid_date
import unittest

class test_common_utils(unittest.TestCase):

    def test_is_valid_date(self):
        self.assertEqual(is_valid_date('something'), False)
        self.assertEqual(is_valid_date('1992-09-07'), True)

if __name__ =='__main__':
    unittest.main()