from backend.src.utils.response_utils import response_handler
from backend.src.app import app
import unittest
from mock import patch, MagicMock

class test_response_utils(unittest.TestCase):

    def test_response_handler(self):
        with app.test_request_context():
            @response_handler
            def sample(*args,**kwargs):
                a = MagicMock()
                a.to_dict = MagicMock(return_value={'username':'lover','status_code':'200'})
                return a
            self.assertEqual(sample().status_code, 200)

            @response_handler
            def sample(*args, **kwargs):
                raise Exception

            self.assertEqual(sample().status_code, 500)

if __name__ =='__main__':
    unittest.main()