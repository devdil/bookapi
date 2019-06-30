# Welcome to BookAPI  V1.0

BookAPI is a sample python api development project to learn about flask development framework, rest apis and unit testing your apis


# Software requirements
* Centos 6.5/7/Mac OS/Any linux machine
* Python 2.7
* git - a version controlling tool
* pip - python package manager tool
* virtualenv - isolated environment for python apps to run



## Installation Procedure

    $ git clone https://github.com/devdil/bookapi.git
    $ virtualenv bookapi
    $ source bookapi/bin/activate
    $ cd bookapi
    $ pip install -r ./backend/src/requirements.txt
    $ source ./setup.sh
    $ python ./backend/src/app.py
    
    
If everything goes well you would see:

```

* Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
2019-06-29 15:07:26,840 - werkzeug - INFO -  * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

    

## Settings Files

```
FYI:

For testing/development 

the file under bookapi/setup.sh does update environment variables.

export MONGO_HOST=diljitpr.net
export MONGO_PORT=27017
export MONGO_DB=books
export PYTHONPATH=$PWD

In production, you would have a file from a keystore and deploy it.

```


## Database

```bash

You wouldn't require to setup any database since I have a test database running on
an aws server. But if you wish to setup your own follow below:


For test purpose, the test database is a mongodb instance running on aws
If you want to run your instance, make sure your mongo instance
you have a db named "books" and update host, password and db credentials in 
`bookapi/setup.sh` [refer to settings section]


```

## Project Coverage
```
The coverage has been taken from coverage utility from python,
to see a more detailed version of coverage see [Unit Testing] section.

Module	statements	missing	excluded	coverage
Total	286	4	0	99%
backend/src/__init__.py	0	0	0	100%
backend/src/apis/__init__.py	0	0	0	100%
backend/src/apis/books_nm.py	23	0	0	100%
backend/src/apis/books_third_party_nm.py	8	0	0	100%
backend/src/apiv1.py	3	0	0	100%
backend/src/app.py	20	2	0	90%
backend/src/logging_config.py	1	0	0	100%
backend/src/models/__init__.py	0	0	0	100%
backend/src/models/abstract_response.py	6	0	0	100%
backend/src/models/book_external_api_model.py	11	0	0	100%
backend/src/models/books_model.py	11	0	0	100%
backend/src/models/error_response.py	6	0	0	100%
backend/src/models/messages.py	3	0	0	100%
backend/src/models/response.py	13	0	0	100%
backend/src/service/__init__.py	0	0	0	100%
backend/src/service/books_service.py	152	2	0	99%
backend/src/settings.py	0	0	0	100%
backend/src/utils/__init__.py	0	0	0	100%
backend/src/utils/common_utils.py	9	0	0	100%
backend/src/utils/response_utils.py	20	0	0	100%
```

## Unit Testing/Development

Before development, ensure that the unit tests are passing. To run them
```
$ cd bookapi
$ ./run_tests.sh

```


Coverage report can be viewed under:
```bash
$ bookapi/htmlcov/index.html

```



## API Supported

The development web server runs on localhost and port 5000. The examples assumes they are hosted at http://127.0.0.1:5000/ and would not use it further in the examples and would only use endpoints

You may use a client like POSTMAN to test these apis.

```
HTTP METHOD: GET
API : /api/external-books

url_params: name
	value: :<value>
	mandatory: yes
	
Description: Gets a list of books from an external given the name of the book as a query parameter in the url. For.e.g, if you want to query all the books whose name is "A Game of Thrones", you would have to form a url like :
**http://127.0.0.1:5000/api/external-books?name=:A Game of Thrones**

Sample Usage: 

URL : http://127.0.0.1:5000/api/external-books?name=:A Game of Thrones

Response :

{
    "data": [
        {
            "authors": [
                "George R. R. Martin"
            ],
            "country": "United States",
            "isbn": "978-0553103540",
            "name": "A Game of Thrones",
            "number_of_pages": 694,
            "publisher": "Bantam Books",
            "release_date": "1996-08-01"
        }
    ],
    "status": "success",
    "status_code": 200
}

On cases where the book name is invalid, the api would return

{
    "data" : []
    "status" : "success",
    "status_code" : 200
}

```


```
HTTP METHOD: GET
API : /api/v1/books/:uid

url_params: :uid
	value: :<value>
	description: unique id of the book
	mandatory: yes
	
Description: Gets a specific book given the unique identifier/id.

Sample Usage: 

URL : http://127.0.0.1:5000/api/v1/books/58ddb7e3-9b1f-11e9-ad2d-8c859094a654

Response :

{
    "data": {
        "authors": [
            "George R. R. Martin"
        ],
        "country": "United States",
        "isbn": "978-8888",
        "name": "Diljit Books 1000",
        "number_of_pages": 768,
        "publisher": "Bantam Books",
        "release_date": "1999-02-02",
        "uid": "58ddb7e3-9b1f-11e9-ad2d-8c859094a654"
    },
    "status": "success",
    "status_code": 200
}

* On cases where the user tries to request a book whose id is invalid or not in our records,
we usually send a response with status code 404 and message to help the user to take corrective action.

for e.g.

{
    "data": [],
    "message": "The resource you requested is invalid/not found. Retry the request with a valid book id",
    "status": "failed",
    "status_code": 404
}

```

```
HTTP METHOD: GET
API : /api/v1/books

The api support filtering by passing url params in the url in the  form of
filter_key=<filter_value>. The supported filters are 
name (string), country (string), publisher (string) and release date(string).

For e.g. 

http://127.0.0.1:5000/api/v1/books?publisher=Bantam Books&name=Diljit Books

Description: Gets all the books in the database

Sample Usage: 

URL : http://127.0.0.1:5000/api/v1/books

Response :

{
    "data": [
        {
            "authors": [
                "George R. R. Martin"
            ],
            "country": "United States",
            "isbn": "978-8888",
            "name": "Diljit Books 1000",
            "number_of_pages": 768,
            "publisher": "Bantam Books",
            "release_date": "1999-02-02",
            "uid": "58ddb7e3-9b1f-11e9-ad2d-8c859094a654"
        },
        {
            "authors": [
                "George R. R. Martin"
            ],
            "country": "United States",
            "isbn": "978-8888222",
            "name": "Diljit Books 3",
            "number_of_pages": 768,
            "publisher": "Bantam Books",
            "release_date": "1999-02-02",
            "uid": "df0336ab-9b1f-11e9-9fd7-8c859094a654"
        }
    ],
    "status": "success",
    "status_code": 200
}


In cases where are no books, found the api would have the following response:

{
    "data": [],
    "status": "success",
    "status_code": 200
}


Other HTTP Return codes:
500 - In case of server faiures
400 - In case of filters which are not supported

```

```
HTTP METHOD: POST
API : /api/v1/books

Description: Creates a new book
Request headers:
    Content-Type: application/json
Request Body : 
    type: json
    body:  {
            "name" : "<string>",
            "isbn" : "<string>",
            "authors" : [ 
                        "<string">
            ],
            "number_of_pages" : <integer>,
            "publisher" : "<string>",
            "country" : "<string>",
            "release_date" : "<string>"
           }
    
Required fields:
    name, isbn, authors, number_of_pages, publisher, country, release_date
Unique Fields:
    isbn

Sample Usage: 

URL : http://127.0.0.1:5000/api/v1/books

Request_body:

        {
            "authors": [
                "George R. R. Martin"
            ],
            "country": "United States",
            "isbn": "978-24123",
            "name": "Diljit Books 8",
            "number_of_pages": 768,
            "publisher": "Bantam Books",
            "release_date": "1999-02-02"
        }

Response :

On Success:

{
    "data": [
        {
            "book": {
                "authors": [
                    "George R. R. Martin"
                ],
                "country": "United States",
                "isbn": "978-24123",
                "name": "Diljit Books 8",
                "number_of_pages": 768,
                "publisher": "Bantam Books",
                "release_date": "1999-02-02",
                "uid": "20bd1d23-9b32-11e9-b374-8c859094a654"
            }
        }
    ],
    "status": "success",
    "status_code": 201
}

The response contains the "uid" which is the unique identifer for the book.
You can use this later to fetch the book by this specific identifier or
update the book with this identifier

In cases where are there are vaidation errors, the response would be :

{
    "data": [],
    "message": "Validation Error! Failed due to ValidationError (Books:None) (sdsadsadasd could not be converted to int: ['number_of_pages']). Please check the request body and try again",
    "status": "failed",
    "status_code": 400
}

In cases where are the isbn are same, the api would respond with a 400 error. for e.g.

{
    "data": [],
    "message": "Item that you are trying to add already exists. Failed due to Tried to save duplicate unique keys (E11000 duplicate key error collection: books.books index: isbn_1 dup key: { : \"978-24123\" }). Please check the request body and try again",
    "status": "failed",
    "status_code": 400
}


Other HTTP Return codes:
500 - In case of server faiures

```


```
HTTP METHOD: PATCH
API : api/v1/books/:uid

Description: Updates a book by the unique identifier and the new request body

url_params: :uid
	value: :<value>
	description: unique id of the book
	mandatory: yes

Request headers:
    Content-Type: application/json
    
Request Body : 
    type: json
    body:  {
            "name" : "<string>",
            "isbn" : "<string>",
            "authors" : [ 
                        "<string">
            ],
            "number_of_pages" : <integer>,
            "publisher" : "<string>",
            "country" : "<string>",
            "release_date" : "<string>"
           }
    
Required fields:
    name, isbn, authors, number_of_pages, publisher, country, release_date
    
Unique Fields:
    isbn

Sample Usage: 

URL : http://127.0.0.1:5000/api/v1/books/58ddb7e3-9b1f-11e9-ad2d-8c859094a654

Request Body:

    {
        "authors": [
            "George R. R. Martin"
        ],
        "country": "United States",
        "isbn": "978-8888",
        "name": "Diljit Books 1001",
        "number_of_pages": 768,
        "publisher": "Bantam Books",
        "release_date": "1999-02-02"
    }

Response :

On Success:

{
    "data": {
        "authors": [
            "George R. R. Martin"
        ],
        "country": "United States",
        "isbn": "978-8888",
        "name": "Diljit Books 1001",
        "number_of_pages": 768,
        "publisher": "Bantam Books",
        "release_date": "1999-02-02",
        "uid": "58ddb7e3-9b1f-11e9-ad2d-8c859094a654"
    },
    "message": "The book Diljit Books 1000 was updated successfully",
    "status": "success",
    "status_code": 200
}

The response contains the updated document


In cases where are there are vaidation errors, the response would be :

{
    "data": [],
    "message": "Validation Error! Failed due to ValidationError (Books:None) (sdsadsadasd could not be converted to int: ['number_of_pages']). Please check the request body and try again",
    "status": "failed",
    "status_code": 400
}

In cases where are the isbn are same, the api would respond with a 400 error. for e.g.

{
    "data": [],
    "message": "Item that you are trying to add already exists. Failed due to Tried to save duplicate unique keys (E11000 duplicate key error collection: books.books index: isbn_1 dup key: { : \"978-24123\" }). Please check the request body and try again",
    "status": "failed",
    "status_code": 400
}


Other HTTP Return codes:
500 - In case of server faiures

```

## Code Architecture/Structure

The source and test files for the entire application is under `bookapi/backend`. The source files
are `bookapi/backend/src` and test files are `bookapi/backend/test`.

For the http rest apis, the flask development framework is being used everywhere and
mongodb for database

The source folder is divided into sub folders again depending upon the responsiblity

```
    bookapi
        backend
            src
              apis\ - contains api endpoints
              models\ - contains model objects for database interaction
              service\ - handles business logic
              utils - reusable common utilties, decorators, etc.  


```

If you are addding any new libraries in the framework, please add your required
library to `bookapi/backend/src/requirements.txt`

The test folder hierarchy is maintained to promote easier lookups and maintainability

```
    bookapi
        backend
            test
              src
                apis\ - contains testcases for api endpoints
                models\ - contains testcases for model objects for database interaction
                service\ - contains testcases for business logic
                utils - contains testcases for  reusable common utilties, decorators, etc.



```


## Logging

To debug failures, errors, etc the flask app is configured to log
to a file called `bookapi/log.txt`. This would help to resolve issues
if any.