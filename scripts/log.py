import datetime
import logging
import os
from functools import wraps


def log(func):
    msg = ' "%s" function' % func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug('START' + msg)
        return func(*args, **kwargs)
    return wrapper


def log_init(typ):
    # typ = 'console', 'gui'
    os.makedirs('logs\\%s' % typ, exist_ok=True)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s/%(lineno)d: %(levelname)s: %(message)s',
                        filename='logs\\%s\\%s.log' % (typ, datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')),
                        filemode='w')
