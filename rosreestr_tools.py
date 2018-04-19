from scripts.console import menu
from scripts.log import log_init


if __name__ == '__main__':
    # initializing log output to file
    log_init('console')

    menu()
