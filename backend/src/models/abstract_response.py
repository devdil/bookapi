
class AbstractResponse(object):

    def __init__(self, status, status_code):
        self.status_code = status_code
        self.status = status

    def to_dict (self):
        return self.__dict__

