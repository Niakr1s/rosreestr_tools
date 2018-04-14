import logging

from PyQt5 import QtWidgets

from gui.central_widget import CentralWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.resize(1000, 600)

        self.setCentralWidget(CentralWidget(self))
        self.setStatusBar(StatusBar(self))
        self.setMenuBar(MenuBar(self))
        self.addToolBar(ToolBar(self))


class StatusBar(QtWidgets.QStatusBar):
    def __init__(self, parent=None):
        QtWidgets.QStatusBar.__init__(self, parent)
        self.showMessage('Добро пожаловать.')


class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        QtWidgets.QMenuBar.__init__(self, parent)

        file_menu = QtWidgets.QMenu('&Файл', self)
        file_menu.addAction('&Выход')
        self.addMenu(file_menu)

        help_menu = QtWidgets.QMenu('&Справка', self)
        help_menu.addAction('&Помощь')
        help_menu.addAction('&О программе')
        self.addMenu(help_menu)


class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent=None):
        QtWidgets.QToolBar.__init__(self, parent)

        self.addAction('Очистить')

if __name__ == '__main__':
    import sys

    logging.basicConfig(level=logging.INFO)
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.move(-1200, 200)
    main_window.show()
    sys.exit(app.exec())
