import unittest
import json
from mock import patch, MagicMock
from backend.src.service.books_service import BookService
from backend.src.service import books_service
from backend.src.app import app
from backend.src.models.response import Response
from mongoengine import ValidationError, NotUniqueError, FieldDoesNotExist
import requests_mock

class test_book_service(unittest.TestCase):

    @patch('backend.src.service.books_service.Books.objects')
    @patch('backend.src.service.books_service.Books')
    def test_get_books_return_valid_response(self, book_p, obj):
        with app.test_request_context():
            with patch('backend.src.service.books_service.Q') as q_patch:
                mobject = MagicMock(spec=BookService)
                db_results = [{"id": 2, "name": "A Clash of Kings", "isbn": "978-0553108033",
                               "authors": ["George R. R. Martin"], "number_of_pages": 768, "publisher": "Bantam Books",
                               "country": "United States", "release_date": "1999-02-02"}]
                a = MagicMock()
                b = MagicMock()
                b.to_json = MagicMock(return_value=db_results)
                a.exclude = MagicMock(return_value=b)
                obj.return_value = a
                response = json.loads(BookService.get_books(mobject, {'name': 'something', 'country': 'something'}).get_data(as_text=True))
                self.assertEqual(response['status_code'], 200)
                self.assertEqual(response['data'], db_results)
                self.assertEqual(response['status'], "success")

    @patch('backend.src.service.books_service.Books.objects')
    @patch('backend.src.service.books_service.Books')
    def test_get_books_db_services_raises_exception(self, book_p, obj):
        with app.test_request_context():
            with patch('backend.src.service.books_service.Q') as q_patch:
                mobject = MagicMock(spec=BookService)
                obj.side_effect = MagicMock(return_value=Exception(''))
                error_resp = json.loads(BookService.get_books(mobject, {'name': 'something', 'country': 'something'}).get_data(as_text=True))
                self.assertEqual(error_resp['status_code'], 500)
                self.assertEqual(error_resp['data'], [])
                self.assertEqual(error_resp['status'], "failed")

    @patch('backend.src.service.books_service.Books.objects')
    @patch('backend.src.service.books_service.Books')
    def test_get_books_invalid_filter_return_error_response(self, book_p, obj):
        with app.test_request_context():
            with patch('backend.src.service.books_service.Q') as q_patch:
                mobject = MagicMock(spec=BookService)
                error_resp = json.loads(BookService.get_books(mobject, {'dummy': 'dummy'}).get_data(as_text=True))
                self.assertEqual(error_resp['status_code'], 400)
                self.assertEqual(error_resp['data'], [])
                self.assertEqual(error_resp['status'], "failed")



    @patch('backend.src.service.books_service.Books.objects.exclude')
    @patch('backend.src.service.books_service.Books.objects')
    @patch('backend.src.service.books_service.Books')
    def test_delete_fails_with_db_exception(self, book_p, obj, excl):
        with app.test_request_context():
            mobject = MagicMock(spec=BookService)
            a = MagicMock()
            b = [MagicMock()]
            b[0].name = MagicMock(return_value='mockbook')
            b[0].delete = MagicMock()
            a.first = b
            excl.return_value = a
            error_resp = json.loads(BookService.delete(mobject, 20).get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 200)
            self.assertEqual(error_resp['data'], [])
            self.assertEqual(error_resp['status'], 'success')
            a = MagicMock()
            b = MagicMock()
            b.name = MagicMock(return_value='mockbook')
            b.delete = MagicMock(side_effect=Exception)
            a.first = MagicMock(return_value=b)
            obj.return_value = a
            error_resp = json.loads(BookService.delete(mobject, 20).get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 500)
            self.assertEqual(error_resp['data'], [])
            self.assertEqual(error_resp['status'], 'failed')
            a.first = MagicMock(return_value='')
            error_resp = json.loads(BookService.delete(mobject, 20).get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 404)
            self.assertEqual(error_resp['data'], [])
            self.assertEqual(error_resp['status'], 'failed')

    @patch('backend.src.service.books_service.Books.objects')
    @patch('backend.src.service.books_service.Books')
    def test_delete_invalid_delete(self, book_p, obj):
        with app.test_request_context():
            mobject = MagicMock(spec=BookService)
            obj.side_effect = MagicMock(return_value=Exception(''))
            error_resp = json.loads(BookService.delete(mobject, 20).get_data(as_text=True))
            self.assertEqual(error_resp['status_code'],404)
            self.assertEqual(error_resp['data'], [])
            self.assertEqual(error_resp['status'], 'failed')

    def test_delete_with_fails_to_delete(self):
        with app.test_request_context():
            mobject = MagicMock(spec=BookService)
            error_resp = json.loads(BookService.delete(mobject, '').get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 400)

    @requests_mock.mock()
    def test_get_books_by_external_api(self, req_mock):
        with app.test_request_context():
            mobject = MagicMock(spec=BookService)
            req_mock.get('https://www.anapioficeandfire.com/api/books/?name=dummy', text='[{"dummy_json":"dummy_value"}]')
            resp = json.loads(BookService.get_books_by_external_api(mobject, {'name':'dummy'}).get_data(as_text=True))
            self.assertEqual(resp['status_code'], 200)

            # resp = json.loads(BookService.get_books_by_external_api(mobject, {'name': 'dummy'}).get_data(as_text=True))
            # self.assertEqual(resp['status_code'], 400)

            import requests
            adapter = requests_mock.Adapter()
            session = requests.Session()
            session.mount('mock', adapter)

            def custom_matcher(request):
                print (request.path_url)
                if request.path_url == 'https://www.anapioficeandfire.com/api/books/?name=test':
                    resp = requests.Response()
                    resp.status_code = 500
                    return resp
                return None

            adapter.add_matcher(custom_matcher)
            resp = json.loads(BookService.get_books_by_external_api(mobject, {'name': ':test'}).get_data(as_text=True))
            self.assertEqual(resp['status_code'], 500)

            resp = json.loads(BookService.get_books_by_external_api(mobject, '').get_data(as_text=True))
            self.assertEqual(resp['status_code'], 400)

    @patch('backend.src.service.books_service.Books.objects')
    @patch('backend.src.service.books_service.Books')
    def test_get_book_by_id(self, book_p, obj):
        with app.test_request_context():
            mobject = MagicMock(spec=BookService)
            db_results = [{"_id": 2, "name": "A Clash of Kings", "isbn": "978-0553108033",
                           "authors": ["George R. R. Martin"], "number_of_pages": 768, "publisher": "Bantam Books",
                           "country": "United States", "release_date": "1999-02-02"}]
            a = MagicMock()
            a.first = MagicMock(return_value=None)
            obj.return_value = a
            err_resp = json.loads(BookService.get_book_by_id(mobject, 20).get_data(as_text=True))
            self.assertEqual(err_resp['status_code'], 404)
            self.assertEqual(err_resp['data'], [])
            self.assertEqual(err_resp['status'], 'failed')

            a = MagicMock()
            b = MagicMock()
            b.to_json = MagicMock(return_value=json.dumps(db_results[0]))
            a.first = MagicMock(return_value=b)
            obj.return_value = a
            resp = json.loads(BookService.get_book_by_id(mobject, 20).get_data(as_text=True))
            self.assertEqual(resp['status_code'], 200)
            db_results[0].pop('_id')
            self.assertEqual(resp['data'], json.loads(json.dumps(db_results[0])))
            self.assertEqual(resp['status'], 'success')

            obj.side_effect = MagicMock(return_value=Exception(''))
            b.to_json = MagicMock(return_value='Dummy')
            err_resp = json.loads(BookService.get_book_by_id(mobject, 20).get_data(as_text=True))
            self.assertEqual(err_resp['status_code'], 500)
            self.assertEqual(err_resp['data'], [])
            self.assertEqual(err_resp['status'], 'failed')
            err_resp = json.loads(BookService.get_book_by_id(mobject, '').get_data(as_text=True))
            self.assertEqual(err_resp['status_code'], 400)
            self.assertEqual(err_resp['data'], [])
            self.assertEqual(err_resp['status'], 'failed')

    @patch('backend.src.service.books_service.Books')
    def test_create_book(self, book_p):
        with app.test_request_context():
            mobject = MagicMock(spec=BookService)
            request_body = {
                                "authors": [
                                    "George R. R. Martin"
                                ],
                                "country": "United States",
                                "isbn": "978-24123",
                                "name": "Diljit Books 8",
                                "number_of_pages": 768,
                                "publisher": "Bantam Books",
                                "release_date": "1999-02"
                            }
            error_resp = json.loads(BookService.create_book(mobject, request_body).get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 400)
            self.assertEqual(error_resp['data'], [])
            self.assertEqual(error_resp['status'], 'failed')

            request_body = {
                "_id" : "123",
                "authors": [
                    "George R. R. Martin"
                ],
                "country": "United States",
                "isbn": "978-24123",
                "name": "Diljit Books 8",
                "number_of_pages": 768,
                "publisher": "Bantam Books",
                "release_date": "1999-02-02"
            }
            a = MagicMock()
            a.save = MagicMock(side_effect=ValidationError)
            book_p.return_value = a
            error_resp = json.loads(BookService.create_book(mobject, request_body).get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 400)
            self.assertEqual(error_resp['data'], [])
            self.assertEqual(error_resp['status'], 'failed')
            a = MagicMock()
            a.save = MagicMock(side_effect=FieldDoesNotExist)
            book_p.return_value = a
            error_resp = json.loads(BookService.create_book(mobject, request_body).get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 400)
            self.assertEqual(error_resp['data'], [])
            self.assertEqual(error_resp['status'], 'failed')
            a.save = MagicMock(side_effect=NotUniqueError)
            error_resp = json.loads(BookService.create_book(mobject, request_body).get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 400)
            self.assertEqual(error_resp['data'], [])
            self.assertEqual(error_resp['status'], 'failed')
            a.save = MagicMock(side_effect=Exception)
            error_resp = json.loads(BookService.create_book(mobject, request_body).get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 400)
            self.assertEqual(error_resp['data'], [])
            self.assertEqual(error_resp['status'], 'failed')

            book = MagicMock()
            s_obj = MagicMock()
            s_obj.to_json = MagicMock(return_value=json.dumps(request_body))
            book.save = MagicMock(return_value=s_obj)
            book_p.return_value = book
            error_resp = json.loads(BookService.create_book(mobject, request_body).get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 201)
            request_body.pop('_id')
            assert error_resp['data'][0].keys()[0] == 'book'
            self.assertEqual(error_resp['status'], 'success')
            error_resp = json.loads(BookService.create_book(mobject, '').get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 400)
            self.assertEqual(error_resp['data'], [])
            self.assertEqual(error_resp['status'], 'failed')

    @patch('backend.src.service.books_service.Books.objects')
    @patch('backend.src.service.books_service.Books')
    def test_update_book(self, book_p, obj):
        with app.test_request_context():
            mobject = MagicMock(spec=BookService)
            request_body = {
                "_id": "123",
                "authors": [
                    "George R. R. Martin"
                ],
                "country": "United States",
                "isbn": "978-24123",
                "name": "Diljit Books 8",
                "number_of_pages": 768,
                "publisher": "Bantam Books",
                "release_date": "1999-02-02"
            }
            a = MagicMock()
            b = MagicMock()
            b.name = MagicMock(return_value='Diljit Books 8')
            b.to_json = MagicMock(return_value=json.dumps(request_body))
            c = MagicMock()
            c.to_json = MagicMock(return_value=json.dumps(request_body))
            b.save = MagicMock(return_value=c)
            a.first = MagicMock(return_value=b)
            obj.return_value = a
            error_resp = json.loads(BookService.update_book(mobject, request_body, "123").get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 200)
            self.assertEqual(error_resp['status'], 'success')
            a = MagicMock()
            b = MagicMock()
            b.name = MagicMock(return_value='Diljit Books 8')
            b.to_json = MagicMock(return_value=json.dumps(request_body))
            b.save = MagicMock(side_effect=ValidationError)
            a.first = MagicMock(return_value=b)
            obj.return_value = a
            error_resp = json.loads(BookService.update_book(mobject, request_body, "123").get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 400)
            self.assertEqual(error_resp['status'], 'failed')
            b.save = MagicMock(side_effect=FieldDoesNotExist)
            error_resp = json.loads(BookService.update_book(mobject, request_body, "123").get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 400)
            self.assertEqual(error_resp['status'], 'failed')
            b.save = MagicMock(side_effect=NotUniqueError)
            error_resp = json.loads(BookService.update_book(mobject, request_body, "123").get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 400)
            self.assertEqual(error_resp['status'], 'failed')
            b.save = MagicMock(side_effect=Exception)
            error_resp = json.loads(BookService.update_book(mobject, request_body, "123").get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 400)
            self.assertEqual(error_resp['status'], 'failed')
            error_resp = json.loads(BookService.update_book(mobject, '', "").get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 400)
            self.assertEqual(error_resp['status'], 'failed')
            a.first = MagicMock(return_value='')
            error_resp = json.loads(BookService.update_book(mobject, request_body, "123").get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 404)
            self.assertEqual(error_resp['status'], 'failed')
            a.first = MagicMock(side_effect=Exception)
            error_resp = json.loads(BookService.update_book(mobject, request_body, "123").get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 500)
            self.assertEqual(error_resp['status'], 'failed')
            a = MagicMock()
            b = MagicMock()
            b.name = MagicMock(return_value='Diljit Books 8')
            import copy
            resp_body = copy.deepcopy(request_body)
            resp_body.pop('name')
            b.to_json = MagicMock(return_value=json.dumps(resp_body))
            c = MagicMock()
            c.to_json = MagicMock(return_value=json.dumps(resp_body))
            b.save = MagicMock(return_value=c)
            a.first = MagicMock(return_value=b)
            obj.return_value = a
            error_resp = json.loads(BookService.update_book(mobject, request_body, "123").get_data(as_text=True))
            self.assertEqual(error_resp['status_code'], 400)
            self.assertEqual(error_resp['status'], 'failed')


    @patch('backend.src.service.books_service.Books.objects')
    @patch('backend.src.service.books_service.Books')
    def test_get_book_by_id_fails_if_id_not_present(self, book_p, obj):
        with app.test_request_context():
            mobject = MagicMock(spec=BookService)
            db_results = [{"_id": 2, "name": "A Clash of Kings", "isbn": "978-0553108033",
                           "authors": ["George R. R. Martin"], "number_of_pages": 768, "publisher": "Bantam Books",
                           "country": "United States", "release_date": "1999-02-02"}]
            a = MagicMock()
            a.first = MagicMock(return_value=None)
            obj.return_value = a
            err_resp = json.loads(BookService.get_book_by_id(mobject, None).get_data(as_text=True))
            self.assertEqual(err_resp['status_code'], 400)
            self.assertEqual(err_resp['status'], 'failed')

if __name__ == '__main__':
    unittest.main()
