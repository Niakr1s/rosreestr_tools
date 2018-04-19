import logging
from functools import wraps


def log(func):
    msg = ' "%s" function in %s' % (func.__name__, __name__)

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug('START' + msg)
        res = func(*args, **kwargs)
        logging.debug('END' + msg)
        return res

    return wrapper
