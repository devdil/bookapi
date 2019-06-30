class BookExternalApiModel(object):

    mapping_to_internal_api = {
        "name": "name",
        "isbn": "isbn",
        "authors": "authors",
        "numberOfPages": "number_of_pages",
        "publisher" : "publisher",
        "country": "country",
        "released": "release_date"
    }

    def __init__(self, **kwargs):

        self.transformed_body = {}

        for key, value in kwargs.iteritems():
            if key in BookExternalApiModel.mapping_to_internal_api:
                if key == "released":
                    value = value.split("T")[0]
                self.transformed_body[BookExternalApiModel.mapping_to_internal_api[key]] = value

    def get_transformed_response(self):
        return self.transformed_body


