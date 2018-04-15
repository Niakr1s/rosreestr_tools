import logging

from PyQt5 import QtWidgets, QtCore

from scripts import xml_file, settings, my_dxf_file, actions


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
    settings = settings.Settings(with_pathes=False)

    def __init__(self, file_type, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.file_type = file_type

        # Creating list view
        self.list_model = QtCore.QStringListModel()
        self.list_view = QtWidgets.QListView(self)
        self.list_view.setModel(self.list_model)
        self.list_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # buttons section
        self.btn_add = QtWidgets.QPushButton('add')
        self.btn_add.clicked.connect(self.on_btn_add_click)

        self.btn_delete = QtWidgets.QPushButton('delete')
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
        logging.info('selected files: %s' % str(file_names))
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
        logging.info('renaming xmls START')
        for i in range(self.list_model.rowCount()):
            index = self.list_model.index(i)
            file_path = self.list_model.data(index, QtCore.Qt.DisplayRole)
            xml = xml_file.XmlFile(file_path, self.settings)
            new_file_path = xml.pretty_rename()
            self.list_model.setData(index, new_file_path)
        logging.info('renaming xmls END')

    def on_btn_convert_clicked(self):
        logging.info('converting xmls START')
        indexes = self.list_view.selectedIndexes()
        if len(indexes):
            for index in indexes:
                file_path = self.list_model.data(index, QtCore.Qt.DisplayRole)
                xml = xml_file.XmlFile(file_path, self.settings)
                xml.convert_to_dxffile()
            logging.info('converting xmls END')
            QtWidgets.QMessageBox.information(self.parent(), 'Информация', 'Операция выполнена')
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
        logging.info('checking dxf in xmls START')
        indexes = self.list_view.selectedIndexes()
        print(indexes)
        if len(indexes):
            my_dxf_file_paths = [self.list_model.data(i, 0) for i in indexes]
            print(my_dxf_file_paths)
            xml_file_pathes = self.parent().xml_view.list_model.stringList()
            all_checks = {}
            for my_dxf_file_path in my_dxf_file_paths:
                my_dxf = my_dxf_file.MyDxfFile(my_dxf_file_path, self.settings)
                checks = my_dxf.checks(xml_file_pathes, save_to_file=False)
                actions.update(all_checks, checks)
            self.parent().output_view.output.setPlainText(my_dxf_file.checks_to_formatted_string(source=all_checks))
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
        выберите нужный dxf и нажмите "Проверить вхождения"')
        self.output.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        box = QtWidgets.QVBoxLayout()
        box.addWidget(label)
        box.addWidget(self.output)

        self.setLayout(box)
