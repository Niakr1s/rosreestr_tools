import sys

from PyQt5 import QtWidgets, QtGui

from gui.central_widget import CentralWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.resize(1000, 600)
        self.setWindowTitle('Rosreestr Tools')
        self.setWindowIcon(QtGui.QIcon(r'static\rt.ico'))

        self.setStatusBar(StatusBar(self))
        self.setMenuBar(MenuBar(self))
        self.setCentralWidget(CentralWidget(self))


class StatusBar(QtWidgets.QStatusBar):
    def __init__(self, parent=None):
        QtWidgets.QStatusBar.__init__(self, parent)
        self.showMessage('Добро пожаловать.')
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.addWidget(self.progress_bar, 1)
        self.progress_bar.hide()

    def reset_progress_bar(self, maximum):
        self.progress_bar.reset()
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        return self.progress_bar


class MenuBar(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        QtWidgets.QMenuBar.__init__(self, parent)

        file_menu = QtWidgets.QMenu('&Файл', self)
        file_menu.addAction('&Выход').triggered.connect(sys.exit)
        self.addMenu(file_menu)

        help_menu = QtWidgets.QMenu('&Справка', self)
        help_menu.addAction('&О программе').triggered.connect(self.about)
        self.addMenu(help_menu)

    def about(self):
        about_text = """
Rosreestr Tools предназначена для кадастровых инженеров.

Данная программа может следующее:
Проверять вхождения dxf файлов (контуров объектов капитального строительства) в кадастровые участки (содержащиеся в xml выписках из Росреестра).
Переименовывать xml выписки из "абракадабры" в читаемые названия.
Конвертировать xml выписки из Росреестра в dxf формат.
Объединять получившиеся dxf файлы в один.

Домашняя страница: https://github.com/Niakr1s/rosreestr_tools/releases
        """
        QtWidgets.QMessageBox().about(self, 'О программе', about_text)


class ToolBar(QtWidgets.QToolBar):
    def __init__(self, parent=None):
        QtWidgets.QToolBar.__init__(self, parent)

        self.addAction('Очистить')
