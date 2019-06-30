python -m unittest discover -s $PWD/backend/test/ -p 'test_*py'
coverage run --source=$PWD/backend/src/ -m unittest discover -s $PWD/backend/test/ -p 'test_*py'
coverage html
