from PyQt5 import QtWidgets

from gui.central_widget import CentralWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.resize(1000, 600)

        self.setCentralWidget(CentralWidget())


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.move(-1200, 200)
    main_window.show()
    sys.exit(app.exec())
