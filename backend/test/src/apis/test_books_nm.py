import unittest
from mock import patch, MagicMock
from backend.src.app import app
from flask import make_response, jsonify
from flask_api import status

class test_book_service(unittest.TestCase):

    @patch('backend.src.apis.books_nm.BookService')
    def test_get_books(self, bk_patch):
        with app.test_request_context():
            expected = make_response(jsonify({}), status.HTTP_200_OK)
            b = MagicMock()
            b.get_books = MagicMock(return_value=expected)
            bk_patch.return_value = b
            c = app.test_client()
            self.assertEqual(c.get('/api/v1/books/').status_code, 200)

    @patch('backend.src.apis.books_nm.BookService')
    def test_get_book_by_id(self, bk_patch):
        with app.test_request_context():
            expected = make_response(jsonify({}), status.HTTP_200_OK)
            b = MagicMock()
            b.get_book_by_id = MagicMock(return_value=expected)
            bk_patch.return_value = b
            c = app.test_client()
            self.assertEqual(c.get('/api/v1/books/123').status_code, 200)

    @patch('backend.src.apis.books_nm.BookService')
    def test_post_book(self, bk_patch):
        with app.test_request_context():
            expected = make_response(jsonify({}), status.HTTP_200_OK)
            b = MagicMock()
            b.create_book = MagicMock(return_value=expected)
            bk_patch.return_value = b
            c = app.test_client()
            self.assertEqual(c.post('/api/v1/books').status_code, 200)

    @patch('backend.src.apis.books_nm.BookService')
    def test_update_book(self, bk_patch):
        with app.test_request_context():
            expected = make_response(jsonify({}), status.HTTP_200_OK)
            b = MagicMock()
            b.update_book = MagicMock(return_value=expected)
            bk_patch.return_value = b
            c = app.test_client()
            self.assertEqual(c.patch('/api/v1/books/123').status_code, 200)

    @patch('backend.src.apis.books_nm.BookService')
    def test_delete(self, bk_patch):
        with app.test_request_context():
            expected = make_response(jsonify({}), status.HTTP_200_OK)
            b = MagicMock()
            b.delete = MagicMock(return_value=expected)
            bk_patch.return_value = b
            c = app.test_client()
            self.assertEqual(c.delete('/api/v1/books/123').status_code, 200)


if __name__ == '__main__':
    unittest.main()
