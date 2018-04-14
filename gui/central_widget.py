from PyQt5 import QtWidgets


class CentralWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        # Left column
        self.xml_view = XmlListView(self)

        # Middle column
        self.dxf_view = DxfListView(self)

        # Right column
        self.output_view = QtWidgets.QTextEdit(self)

        # Creating main layout
        box = QtWidgets.QHBoxLayout(self)
        box.addWidget(self.xml_view)  # Left column
        box.addWidget(self.dxf_view)  # Middle column
        box.addWidget(self.output_view)  # Right column

        self.setLayout(box)


class MyListView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.list_view = QtWidgets.QListView(self)
        self.btn_add = QtWidgets.QPushButton('add')
        self.btn_delete = QtWidgets.QPushButton('delete')

        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.list_view)

        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(self.btn_add)
        hbox.addWidget(self.btn_delete)

        vbox.addLayout(hbox)


class XmlListView(MyListView):
    def __init__(self, parent=None):
        MyListView.__init__(self, parent)


class DxfListView(MyListView):
    def __init__(self, parent=None):
        MyListView.__init__(self, parent)
