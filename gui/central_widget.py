import logging
import os

from PyQt5 import QtWidgets, QtCore

from gui import my_threads
from gui.file_list_view import FileListView
from scripts import xml_file
from scripts.log import log


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Left column
        self.xml_view = XmlListView(self)

        # Middle column
        self.dxf_view = MyDxfListView(self)

        # Right column
        self.output_view = OutputView(self)

        # Creating main layout
        main_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addWidget(self.xml_view)  # Left column
        main_layout.addWidget(self.dxf_view)  # Middle column
        main_layout.addWidget(self.output_view)  # Right column

        self.setLayout(main_layout)


class MyListView(QtWidgets.QWidget):
    def __init__(self, file_type, parent=None):
        """file_type = string 'xml' or 'dxf'"""
        QtWidgets.QWidget.__init__(self, parent)
        self.main_window = self.parent().parent()
        self.file_type = file_type
        self.progress_bar = self.main_window.statusBar().progress_bar

        # Creating list view
        self.list_model = QtCore.QStringListModel()
        self.list_view = FileListView(self)
        self.list_view.setModel(self.list_model)

        # buttons section
        self.btn_add = QtWidgets.QPushButton('Добавить')
        self.btn_add.clicked.connect(self.on_btn_add_click)

        self.btn_delete = QtWidgets.QPushButton('Удалить')
        self.btn_delete.clicked.connect(self.on_btn_delete_click)

        # Top layout with buttons
        self.top_layout = QtWidgets.QHBoxLayout()
        self.top_layout.addWidget(self.btn_add)
        self.top_layout.addWidget(self.btn_delete)

        # Middle layout with view
        self.mid_layout = QtWidgets.QHBoxLayout()
        self.mid_layout.addWidget(self.list_view)

        # Bottom layout with buttons
        self.bot_layout = QtWidgets.QHBoxLayout()

        # Main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(self.top_layout)
        main_layout.addLayout(self.mid_layout)
        main_layout.addLayout(self.bot_layout)

        self.setLayout(main_layout)

    @log
    def on_btn_add_click(self, checked):
        # adding items to list_view and list_model

        # Making filter_string for QFileDialog
        if self.file_type == 'xml':
            filter_string = 'Выписки (*.%s)' % self.file_type
        else:
            filter_string = 'Чертеж (*.%s)' % self.file_type

        # get last_path from settings
        last_path = self.main_window.settings.value('last_paths/%s' % self.file_type)
        file_names = QtWidgets.QFileDialog(self).getOpenFileNames(self, 'Добавить файлы', last_path, filter_string)[0]
        if file_names:
            # updating last_path
            self.main_window.settings.setValue('last_paths/%s' % self.file_type, os.path.dirname(file_names[0]))
            for file in file_names:
                logging.info('adding %s' % str(file))
                append_data(self.list_model, file)

    @log
    def on_btn_delete_click(self, checked):
        # deleting items from list_view and list_model
        file_indexes = [i.row() for i in self.list_view.selectedIndexes()]
        file_indexes.sort(reverse=True)  # reversing to delete items from end
        for f in file_indexes:
            logging.info('deleting %i row' % f)
            self.list_model.removeRow(f)

    def on_thread_signal(self, msg):
        # common signal handler, adding +1 to value and prints msg to statusbar
        self.progress_bar.setFormat(msg)
        self.progress_bar.setValue(self.progress_bar.value() + 1)

    def on_thread_finished(self):
        self.progress_bar.hide()
        self.main_window.statusBar().showMessage('Операция завершена')


class XmlListView(MyListView):
    # Xml list view
    def __init__(self, parent=None):
        MyListView.__init__(self, 'xml', parent)

        self.btn_rename = QtWidgets.QPushButton('Переименовать все')
        self.btn_rename.clicked.connect(self.on_btn_rename_click)

        self.btn_convert_selected = QtWidgets.QPushButton('Выделенное в dxf')
        self.btn_convert_selected.clicked.connect(self.on_btn_convert_clicked)

        self.bot_layout.addWidget(self.btn_rename)
        self.bot_layout.addWidget(self.btn_convert_selected)

    @log
    def on_btn_rename_click(self, checked):
        # renaming all XMLs to pretty format
        for i in range(self.list_model.rowCount()):
            index = self.list_model.index(i)
            file_path = self.list_model.data(index, QtCore.Qt.DisplayRole)
            logging.info('renaming %s' % file_path)
            xml = xml_file.XmlFile(file_path)
            new_file_path = xml.pretty_rename()
            self.list_model.setData(index, new_file_path)

    @log
    def on_btn_convert_clicked(self, checked):
        # converting selected XMLs to DXFs to same folder and merging it in one file if user wants
        indexes = self.list_view.selectedIndexes()
        if len(indexes):
            # if user wants to merge all dxfs in one file
            merge = QtWidgets.QMessageBox().question(self, 'Вопрос', 'Объединять в один файл?',
                                                     buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox().Yes

            if merge:
                # get last_merged_path from settings
                last_merged_path = self.main_window.settings.value('last_paths/merged')
                merged_path = \
                    QtWidgets.QFileDialog().getSaveFileName(self, directory=last_merged_path, filter='Чертеж (*.dxf)')[
                        0]
                if merged_path:
                    # if merged_path changed - update last_merged_path in settings
                    self.main_window.settings.setValue('last_paths/merged', merged_path)
            else:
                # '' means user doesn't want to merge dxfs
                merged_path = ''

            # preparing progressbar
            self.main_window.statusBar().reset_progress_bar(len(indexes))
            # getting xml file list from model
            file_paths = [self.list_model.data(i, QtCore.Qt.DisplayRole) for i in indexes]

            # starting thread
            t = my_threads.XmlConvertThread(file_paths, merged_path, parent=self)
            t.signal.connect(self.on_thread_signal, QtCore.Qt.QueuedConnection)
            t.finished.connect(self.on_thread_finished)
            t.start()
        else:
            QtWidgets.QMessageBox.information(self.parent(), 'Ошибка', 'Выберите один или несколько xml из списка!')


class MyDxfListView(MyListView):
    # MyDxf list view
    def __init__(self, parent=None):
        MyListView.__init__(self, 'dxf', parent)

        self.btn_check = QtWidgets.QPushButton('Проверить вхождения')
        self.btn_check.clicked.connect(self.on_btn_check_click)

        self.bot_layout.addWidget(self.btn_check)

    @log
    def on_btn_check_click(self, checked):
        # checks selected myDxfs in all XMLs
        indexes = self.list_view.selectedIndexes()
        if len(indexes):
            my_dxf_file_paths = [self.list_model.data(i, 0) for i in indexes]
            xml_file_pathes = self.parent().xml_view.list_model.stringList()

            # preparing progressbar
            self.main_window.statusBar().reset_progress_bar(len(indexes))

            # starting thread
            t = my_threads.MyDxfCheckThread(my_dxf_file_paths, xml_file_pathes, self.on_thread_finished, self)
            t.signal.connect(self.on_thread_signal, QtCore.Qt.QueuedConnection)
            t.start()

        else:
            QtWidgets.QMessageBox.information(self.parent(), 'Ошибка', 'Выберите один или несколько dxf из списка!')

    def on_thread_finished(self, str):
        super().on_thread_finished()
        self.parent().output_view.output.setPlainText(str)


class OutputView(QtWidgets.QWidget):
    # Results view
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        label = QtWidgets.QLabel('Результаты проверки вхождения')

        # json output
        self.output = QtWidgets.QPlainTextEdit(self)
        self.output.setPlainText('Откройте несколько xml и dxf в панелях слева, \
        выберите один или несколько dxf и нажмите "Проверить вхождения"')
        self.output.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        box = QtWidgets.QVBoxLayout()
        box.addWidget(label)
        box.addWidget(self.output)

        self.setLayout(box)


def append_data(model, data):
    # appends data at end of model
    length = model.rowCount()
    model.insertRow(length)
    model.setData(model.index(length), data)
