import logging
import sys

from PyQt5 import QtWidgets

from gui.main_window import MainWindow

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.move(-1200, 200)
    main_window.show()
    sys.exit(app.exec())
