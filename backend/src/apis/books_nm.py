from flask import Blueprint, jsonify
from flask import request
from backend.src.service.books_service import BookService
import datetime

books_blueprint = Blueprint('books', __name__, url_prefix='/api/v1/books')

@books_blueprint.route('/', methods=['GET'])
def get_books():
    request_args = request.args
    book_service = BookService()
    return book_service.get_books(request_args)

@books_blueprint.route('/<id>', methods=['GET'])
def get_book_by_id(id):
    book_service = BookService()
    return book_service.get_book_by_id(id)

@books_blueprint.route('', methods=['POST'])
def post_book():
    request_json = request.get_json()
    book_service = BookService()
    return book_service.create_book(request_json)

@books_blueprint.route('/<id>', methods=['PATCH'])
def update_book(id):
    request_json = request.get_json()
    book_service = BookService()
    return book_service.update_book(request_json, id)

@books_blueprint.route('/<id>', methods=['DELETE'])
def delete(id):
    #add schema validation for validating json_request
    book_service = BookService()
    return book_service.delete(id)
