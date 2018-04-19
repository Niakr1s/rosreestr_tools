import sys

from PyQt5 import QtWidgets, QtGui, QtCore

from gui.central_widget import CentralWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        # initialize settings
        self.settings = QtCore.QSettings('settings.ini', QtCore.QSettings.IniFormat)

        # self.resize(1000, 600)
        self.resize(self.settings.value('main_window/size', QtCore.QSize(1000, 600)))
        self.move(self.settings.value('main_window/pos', QtCore.QPoint(0, 0)))
        self.setWindowTitle('Rosreestr Tools')
        self.setWindowIcon(QtGui.QIcon(r'static\rt.png'))

        self.setStatusBar(StatusBar(self))
        self.setMenuBar(MenuBar(self))
        self.setCentralWidget(CentralWidget(self))

        QtCore.QCoreApplication.setOrganizationName('by Niakr1s')
        QtCore.QCoreApplication.setApplicationName('Rosreest Tools')

    def closeEvent(self, e):
        # saving main window geometry
        self.settings.setValue('main_window/size', self.size())
        self.settings.setValue('main_window/pos', self.pos())
        e.accept()


class StatusBar(QtWidgets.QStatusBar):
    def __init__(self, parent=None):
        QtWidgets.QStatusBar.__init__(self, parent)

        self.progress_bar = QtWidgets.QProgressBar(self)

        # init progressbar for future use and hide it
        self.addWidget(self.progress_bar, 1)
        self.progress_bar.hide()

    def reset_progress_bar(self, maximum):
        # resets progress_bar with maximum value
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
        # simple about window
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
    # add toolbar here
    def __init__(self, parent=None):
        QtWidgets.QToolBar.__init__(self, parent)

        self.addAction('Очистить')
