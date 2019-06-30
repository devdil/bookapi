from functools import wraps
from backend.src.models.error_response import ErrorResponse
from backend.src.models.response import ResponseMessages
from flask_api import status
from flask import make_response, jsonify
import logging
import traceback

logger = logging.getLogger('flask_app')

def response_handler(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # here we want to execute the function
        response = None
        try:
            response = f(*args, **kwargs)
        except Exception as error:
            logger.debug("unexpected failure caught {}".format(traceback.format_exc()))
            response = ErrorResponse(ResponseMessages.FAILED, status.HTTP_500_INTERNAL_SERVER_ERROR, message="Failed while processing the request. Retry the request, if issue persists Please contact the support representative.")

        logger.debug(response)

        response = response.to_dict()

        return make_response(jsonify(response), response['status_code'])

    return wrapper
