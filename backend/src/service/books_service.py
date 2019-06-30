from backend.src.models.error_response import ErrorResponse
from backend.src.models.response import Response
from backend.src.models.books_model import Books
from backend.src.models.book_external_api_model import BookExternalApiModel
from backend.src.utils.response_utils import response_handler
from backend.src.models.response import ResponseMessages
from mongoengine.queryset.visitor import Q
from mongoengine import ValidationError, NotUniqueError, FieldDoesNotExist
from flask_api import status
from backend.src.utils.common_utils import is_valid_date
import logging
import traceback
import uuid
import requests
import json
import datetime

logger = logging.getLogger('flask_app')


class BookService(object):
    ICE_AND_FIRE_API = "https://www.anapioficeandfire.com/api/books"

    @response_handler
    def get_books(self, request_args):
        logger.info("request args {}".format(request_args))
        allowable_filter_values = ["name", "country", "publisher","release_date"]
        query_map = {}

        for filter_key, filter_value in request_args.iteritems():
            if filter_key in allowable_filter_values:
                query_map[filter_key] = Q(**{filter_key: filter_value})
            else:
                return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                     message="Filter {} not supported".format(filter_key))

        logger.debug('q obj {}'.format(query_map.values()))
        final_query_obj = None

        for query_obj in query_map.values():
            if final_query_obj:
                final_query_obj &= query_obj
            else:
                final_query_obj = query_obj

        logger.debug(final_query_obj)

        try:
            books = Books.objects(final_query_obj).exclude('id')
        except Exception as error:
            logger.debug('failed due to {}'.format(traceback.format_exc()))
            return ErrorResponse(ResponseMessages.FAILED, status.HTTP_500_INTERNAL_SERVER_ERROR,
                                 message="Failed while processing the request. Retry the request, if issue persists Please contact the support representative.")
        else:
            logger.info("got a list of books {}".format(books.to_json()))
            return Response(ResponseMessages.SUCCESS, status.HTTP_200_OK, results=books.to_json())

    @response_handler
    def get_books_by_external_api(self, request_args):
        if request_args:
            name = request_args.get('name')
            logger.debug("request args {}".format(request_args))
            logger.debug("going to search by name {}".format(name))
            try:
                resp = requests.get(BookService.ICE_AND_FIRE_API + '/?name={}'.format(name))
            except Exception as error:
                return ErrorResponse(ResponseMessages.FAILED, status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     message="Could not complete the request with the third party api due to {}".format(
                                         str(error)))
            if resp.status_code == 200:
                response_content = json.loads(resp.content)
                results = []

                for book in response_content:
                    tranformed_book = BookExternalApiModel(**book)
                    results.append(tranformed_book.get_transformed_response())

                return Response(ResponseMessages.SUCCESS, status.HTTP_200_OK, results=results)

            else:
                logger.debug("response failed with status code {}".format(resp.status_code))
                return ErrorResponse(ResponseMessages.FAILED, status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     message="Could not complete the request because the third party responsed with {} and response {}".format(
                                         resp.status_code, resp.content))
        else:
            return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                 message="The url should contain request args in the form of name=:<name of the book>. Please retry the request with said format")


    @response_handler
    def get_book_by_id(self, id):
        if id:
            try:
                book = Books.objects(__raw__={'uid': id}).first()
            except Exception as error:
                logger.debug("failed due to {}".format(traceback.format_exc()))
                return ErrorResponse(ResponseMessages.FAILED, status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     message="Internal Server Error. Retry again")
            else:
                if book:
                    results = json.loads(book.to_json())
                    results.pop('_id')
                    # we have found the book we can delete it
                    return Response(ResponseMessages.SUCCESS, status.HTTP_200_OK,
                                    results=results)
                else:
                    return ErrorResponse(ResponseMessages.FAILED, status.HTTP_404_NOT_FOUND,
                                         message="The resource you requested is invalid/not found. "
                                                 "Retry the request with a valid book id")
        else:
            return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                 message="The api url should have an id to retriev"
                                         "Retry the request with a valid book id")


    @response_handler
    def delete(self, id):
        if id:
            logger.debug("delete call id requested to delete {}".format(id))
            try:
                book = Books.objects(__raw__={'uid': id}).first()
            except Exception as error:
                logger.debug("failed due to {}".format(traceback.format_exc()))
                return ErrorResponse(ResponseMessages.FAILED, status.HTTP_404_NOT_FOUND,
                                     message="The resource you requested to delete is invalid. "
                                             "Retry the request with a valid request")
            else:
                if book:
                    logger.debug("book found {}".format(book.name))
                    try:
                        book.delete()
                    except Exception as error:
                        logger.debug("could not delete due to {}".format(traceback.format_exc()))
                        return ErrorResponse(ResponseMessages.FAILED, status.HTTP_500_INTERNAL_SERVER_ERROR,
                                             message="Something went wrong while deleting the request. "
                                                     "Please try again")
                    # we have found the book we can delete it
                    return Response(ResponseMessages.SUCCESS, status.HTTP_200_OK,
                                    results=[], message="The book {} was deleted successfully".format(book.name))
                else:
                    return ErrorResponse(ResponseMessages.FAILED, status.HTTP_404_NOT_FOUND,
                                         message="The resource you requested to delete is invalid. "
                                                 "Retry the request with a valid request")
        else:
            return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                 message="The delete api should have a valid id"
                                         "Retry the request with a valid request")


    @response_handler
    def create_book(self, request_body):
        if request_body:
            # validate request body and keys in it
            unique_id = str(uuid.uuid1())
            request_body[u'uid'] = unique_id
            logger.info("request body {}".format(request_body))
            if 'release_date' in request_body and not is_valid_date(request_body['release_date']):
                return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                     message="Validation Error! Incorrect date format for field Released, should be YYYY-MM-DD")
            try:
                book = Books(**request_body).save()
            except ValidationError as validation_error:
                logger.debug("create book failed due to {}".format(traceback.format_exc()))
                return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                     message="Validation Error! Failed due to {}. Please check the request body and try again".format(
                                         validation_error))
            except FieldDoesNotExist as field_not_exist_error:
                logger.debug("create book failed due to {}".format(traceback.format_exc()))
                return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                     message="One ore more fields in the request body does not exist! Failed due to {}. Please check the request body and try again".format(
                                         field_not_exist_error))
            except NotUniqueError as not_unique_error:
                logger.debug("create book failed due to {}".format(traceback.format_exc()))
                return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                     message="Item that you are trying to add already exists. Failed due to {}. Please check the request body and try again".format(
                                         not_unique_error))
            except Exception as error:
                logger.debug("create book failed due to {}".format(traceback.format_exc()))
                return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                     message="Failed due to {}".format(str(error)))
            else:
                results = json.loads(book.to_json())
                results.pop('_id')
                return Response(ResponseMessages.SUCCESS, status.HTTP_201_CREATED, results=[{"book": results}])
        else:
            return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                 message="The request should contain a valid request body!")

    @response_handler
    def update_book(self, request_body, id):
        if request_body and id:
            # check if id exists in the database
            try:
                book = Books.objects(__raw__={'uid': id}).first()
            except Exception as error:
                logger.debug("Failed due to {}".format(traceback.format_exc()))
                return ErrorResponse(ResponseMessages.FAILED, status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                 message="Could not process request to internal server error. Please try again")
            else:
                if book:
                    logger.debug("book found {}".format(book.to_json()))
                    old_book_name = book.name
                    book_in_dict = json.loads(book.to_json())
                    for key, value in request_body.iteritems():
                        if key not in book_in_dict:
                            return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                                 message="The field {} does not exist".format(key))
                        else:
                            book[key] = value
                    try:
                        updated_book_document = book.save()
                    except ValidationError as validation_error:
                        logger.debug("create book failed due to {}".format(traceback.format_exc()))
                        return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                             message="Validation Error! Failed due to {}. Please check the request body and try again".format(
                                                 validation_error))
                    except FieldDoesNotExist as field_not_exist_error:
                        logger.debug("create book failed due to {}".format(traceback.format_exc()))
                        return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                             message="One ore more fields in the request body does not exist! Failed due to {}. Please check the request body and try again".format(
                                                 field_not_exist_error))
                    except NotUniqueError as not_unique_error:
                        logger.debug("create book failed due to {}".format(traceback.format_exc()))
                        return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                             message="Item that you are trying to add already exists. Failed due to {}. Please check the request body and try again".format(
                                                 not_unique_error))
                    except Exception as error:
                        logger.debug("failed to update the book due {}".format(traceback.format_exc()))
                        return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                             message="Failed due to {}".format(str(error)))
                    else:
                        updated_book_document = json.loads(updated_book_document.to_json())
                        updated_book_document.pop('_id')
                        logger.debug("successfully updated {}".format(updated_book_document))
                        return Response(ResponseMessages.SUCCESS, status.HTTP_200_OK,
                                        results=updated_book_document,
                                        message="The book {} was updated successfully".format(old_book_name))
                else:
                    logger.debug("book does not exist in the database ")
                    return ErrorResponse(ResponseMessages.FAILED, status.HTTP_404_NOT_FOUND,
                                         message="The resource you requested to delete is invalid/does not exist"
                                                 "Retry the request with a valid request")
        else:
            return ErrorResponse(ResponseMessages.FAILED, status.HTTP_400_BAD_REQUEST,
                                 message="The request should have a valid target id and a valid request body. Please check the request body and try again")
