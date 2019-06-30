from mongoengine import *

class Books(Document):
    name = StringField(required=True)
    uid = StringField(required=True, unique=True)
    isbn = StringField(required=True, unique=True)
    authors = ListField(StringField(required=True))
    number_of_pages = IntField(required=True)
    authors = ListField(StringField())
    publisher = StringField(required=True)
    country = StringField(required=True)
    release_date = StringField(required=True)
