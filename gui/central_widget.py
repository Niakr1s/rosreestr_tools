import logging

from PyQt5 import QtWidgets, QtCore


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Left column
        self.xml_view = XmlListView(self)

        # Middle column
        self.dxf_view = DxfListView(self)

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
        QtWidgets.QWidget.__init__(self, parent)
        self.file_type = file_type

        # Creating list view
        self.list_model = QtCore.QStringListModel()
        self.list_view = QtWidgets.QListView(self)
        self.list_view.setModel(self.list_model)

        # buttons section
        self.btn_add = QtWidgets.QPushButton('add')
        self.btn_add.clicked.connect(self.on_btn_add_click)

        self.btn_delete = QtWidgets.QPushButton('delete')

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

        logging.info('selected files: %s' % str(file_names))


class XmlListView(MyListView):
    def __init__(self, parent=None):
        MyListView.__init__(self, 'xml', parent)

        self.btn_rename = QtWidgets.QPushButton('Переименовать')
        self.btn_convert = QtWidgets.QPushButton('Выделенное 2dxf')
        self.btn_convert_all = QtWidgets.QPushButton('Все 2dxf')

        self.bot_layout.addWidget(self.btn_rename)
        self.bot_layout.addWidget(self.btn_convert)
        self.bot_layout.addWidget(self.btn_convert_all)


class DxfListView(MyListView):
    def __init__(self, parent=None):
        MyListView.__init__(self, 'dxf', parent)

        self.btn_check = QtWidgets.QPushButton('Проверить вхождения')
        self.bot_layout.addWidget(self.btn_check)


class OutputView(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        QtWidgets.QTextEdit.__init__(self, parent)
