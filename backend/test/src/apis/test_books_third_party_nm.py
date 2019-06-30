from backend.src.apis import books_third_party_nm
import unittest
from mock import patch, MagicMock
from backend.src.app import app
from flask import make_response, jsonify
from flask_api import status

class test_books_third_party_nm(unittest.TestCase):

    @patch('backend.src.apis.books_third_party_nm.BookService')
    def test_get_external_books(self, bk_patch):
        with app.test_request_context():
            expected = make_response(jsonify({}), status.HTTP_200_OK)
            b = MagicMock()
            b.get_books_by_external_api = MagicMock(return_value=expected)
            bk_patch.return_value = b
            c = app.test_client()
            self.assertEqual(c.get('/api/external-books/').status_code, 200)

if __name__ =='__main__':
    unittest.main()