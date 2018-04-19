import datetime
import logging
import os

from scripts.console import menu

os.makedirs('logs\\console', exist_ok=True)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s/%(lineno)d: %(levelname)s: %(message)s',
                    filename='logs\\console\\%s.log' % datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'),
                    filemode='w')

if __name__ == '__main__':
    menu()
