import logging
import sys
import traceback

from PyQt5 import QtWidgets, QtCore

from gui.main_window import MainWindow

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('windowsvista')
    main_window = MainWindow()
    # main_window.move(-1200, 200)
    main_window.show()

    if QtCore.QT_VERSION >= 0x50501:
        def excepthook(type_, value, traceback_):
            traceback.print_exception(type_, value, traceback_)
            QtCore.qFatal('')
    sys.excepthook = excepthook

    sys.exit(app.exec())
