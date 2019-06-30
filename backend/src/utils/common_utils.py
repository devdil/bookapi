import logging
import datetime

logger = logging.getLogger('flask_app')

def is_valid_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    else:
        return True

