import logging

from PyQt5 import QtWidgets


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

        self.list_view = QtWidgets.QListView(self)

        self.btn_add = QtWidgets.QPushButton('add')
        self.btn_add.clicked.connect(self.on_btn_add_click)

        self.btn_delete = QtWidgets.QPushButton('delete')

        # Top layout with buttons
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.addWidget(self.btn_add)
        top_layout.addWidget(self.btn_delete)

        # Middle layout with view
        mid_layout = QtWidgets.QHBoxLayout()
        mid_layout.addWidget(self.list_view)

        # Bottom layout with buttons
        bot_layout = QtWidgets.QHBoxLayout()

        # Main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(mid_layout)
        main_layout.addLayout(bot_layout)

        self.setLayout(main_layout)

    def on_btn_add_click(self):
        # Making filter_string for QFileDialog
        if self.file_type == 'xml':
            filter_string = 'Выписки (*.%s)' % self.file_type
        else:
            filter_string = 'Чертеж (*.%s)' % self.file_type

        file_names = QtWidgets.QFileDialog(self).getOpenFileNames(self, 'Добавить файлы', '', filter_string)
        
        logging.info('selected files: %s' % str(file_names[0]))


class XmlListView(MyListView):
    def __init__(self, parent=None):
        MyListView.__init__(self, 'xml', parent)


class DxfListView(MyListView):
    def __init__(self, parent=None):
        MyListView.__init__(self, 'dxf', parent)


class OutputView(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        QtWidgets.QTextEdit.__init__(self, parent)
