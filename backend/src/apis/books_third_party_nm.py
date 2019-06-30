from flask import Blueprint
from flask import request
from backend.src.service.books_service import BookService

books_third_party_blueprint = Blueprint('external_books', __name__, url_prefix='/api/external-books')


@books_third_party_blueprint.route('/', methods=['GET'])
def get_external_books():
    request_args = request.args
    book_service = BookService()
    return book_service.get_books_by_external_api(request_args)


