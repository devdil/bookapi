from backend.src.models.book_external_api_model import BookExternalApiModel
import unittest

class test_abstract_response(unittest.TestCase):

    def test_abstract_resposne(self):
        self.assertEqual(BookExternalApiModel(name='test',authors='test_author',released='dateTtest').get_transformed_response(),
                         {'authors': 'test_author', 'name': 'test', 'release_date': 'date'})


if __name__ =='__main__':
    unittest.main()