import logging

from PyQt5 import QtWidgets, QtCore

from gui import my_threads
from scripts import xml_file, settings


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
    settings = settings.Settings(with_paths=False)

    def __init__(self, file_type, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.main_window = self.parent().parent()
        self.file_type = file_type
        self.progress_bar = self.main_window.statusBar().progress_bar

        # Creating list view
        self.list_model = QtCore.QStringListModel()
        self.list_view = QtWidgets.QListView(self)
        self.list_view.setModel(self.list_model)
        self.list_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

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

    def on_btn_add_click(self):
        # adding items to list_view and list_model

        # Making filter_string for QFileDialog
        if self.file_type == 'xml':
            filter_string = 'Выписки (*.%s)' % self.file_type
        else:
            filter_string = 'Чертеж (*.%s)' % self.file_type

        file_names = QtWidgets.QFileDialog(self).getOpenFileNames(self, 'Добавить файлы', '', filter_string)[0]
        for file in file_names:
            length = self.list_model.rowCount()
            self.list_model.insertRow(length)
            self.list_model.setData(self.list_model.index(length), file)

        logging.info('files added, current rowCount = %i' % self.list_model.rowCount())

    def on_btn_delete_click(self):
        # deleting items from list_view and list_model
        file_indexes = [i.row() for i in self.list_view.selectedIndexes()]
        file_indexes.sort(reverse=True)  # reversing to delete items from end
        logging.info('start deleting %i' % len(file_indexes))
        for f in file_indexes:
            self.list_model.removeRow(f)
        logging.info('items deleted')

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

    def on_btn_rename_click(self):
        # renaming all XMLs to pretty format
        logging.info('renaming xmls START')
        for i in range(self.list_model.rowCount()):
            index = self.list_model.index(i)
            file_path = self.list_model.data(index, QtCore.Qt.DisplayRole)
            xml = xml_file.XmlFile(file_path, self.settings)
            new_file_path = xml.pretty_rename()
            self.list_model.setData(index, new_file_path)
        logging.info('renaming xmls END')

    def on_btn_convert_clicked(self):
        # converting selected XMLs to DXFs to same folder and merging it in one file if user wants
        logging.info('converting xmls START')
        indexes = self.list_view.selectedIndexes()
        if len(indexes):
            # if user wants to merge all dxfs in one file
            merge = QtWidgets.QMessageBox().question(self, 'Вопрос', 'Объединять в один файл?',
                                                     buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox().Yes
            if merge:
                merged_path = QtWidgets.QFileDialog().getSaveFileName(self, filter='Чертеж (*.dxf)')[0]
            else:
                merged_path = None

            # preparing progressbar
            self.main_window.statusBar().reset_progress_bar(len(indexes))
            # getting xml file list from model
            file_paths = [self.list_model.data(i, QtCore.Qt.DisplayRole) for i in indexes]

            # starting thread
            t = my_threads.XmlConvertThread(file_paths, merge, merged_path, parent=self)
            t.signal.connect(self.on_thread_signal, QtCore.Qt.QueuedConnection)
            t.finished.connect(self.on_thread_finished)
            t.start()

            logging.info('converting xmls END')
        else:
            QtWidgets.QMessageBox.information(self.parent(), 'Ошибка', 'Выберите один или несколько xml из списка!')
            logging.info('converting xmls: file not selected')


class MyDxfListView(MyListView):
    # MyDxf list view
    def __init__(self, parent=None):
        MyListView.__init__(self, 'dxf', parent)

        self.btn_check = QtWidgets.QPushButton('Проверить вхождения')
        self.btn_check.clicked.connect(self.on_btn_check_click)

        self.bot_layout.addWidget(self.btn_check)

    def on_btn_check_click(self):
        # checks selected myDxfs in all XMLs
        logging.info('checking dxf in xmls START')
        indexes = self.list_view.selectedIndexes()
        if len(indexes):
            my_dxf_file_paths = [self.list_model.data(i, 0) for i in indexes]
            xml_file_pathes = self.parent().xml_view.list_model.stringList()

            # preparing progressbar
            self.main_window.statusBar().reset_progress_bar(len(indexes))

            # starting thread
            t = my_threads.MyDxfCheckThread(my_dxf_file_paths, xml_file_pathes, self.on_my_dxf_check_thread_finished,
                                            self)
            t.signal.connect(self.on_thread_signal, QtCore.Qt.QueuedConnection)
            t.start()

            logging.info('checking dxf in xmls END')
        else:
            QtWidgets.QMessageBox.information(self.parent(), 'Ошибка', 'Выберите один или несколько dxf из списка!')
            logging.info('checking dxf in xmls: file not selected')


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
