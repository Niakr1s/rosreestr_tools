import logging

from scripts.console import menu

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s/%(lineno)d: %(levelname)s: %(message)s',
                    filename='log.log')

if __name__ == '__main__':
    menu()
