from backend.src.models.abstract_response import AbstractResponse

class ErrorResponse(AbstractResponse):

    def __init__(self, status, status_code, message):
        super(ErrorResponse, self).__init__(status, status_code)
        self.message = message
        self.data=[]
