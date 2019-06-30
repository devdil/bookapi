from backend.src.models.abstract_response import AbstractResponse
from backend.src.models.messages import ResponseMessages
from flask_api import status
import json

class Response(AbstractResponse):

    def __init__(self, status, status_code, results, message=None):
        super(Response, self).__init__(status, status_code)
        if results or results == []:
            if type(results) == str:
                self.data = json.loads(results)
            else:
                self.data = results
        if message:
            self.message = message

