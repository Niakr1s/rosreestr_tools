import logging
from functools import wraps


def log(func):
    msg = ' "%s" function' % func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug('START' + msg)
        return func(*args, **kwargs)
    return wrapper
