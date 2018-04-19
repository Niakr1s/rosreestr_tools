import logging

from PyQt5 import QtWidgets

from gui import central_widget


class FileListView(QtWidgets.QListView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            model = self.model()
            for url in e.mimeData().urls():
                path = url.toLocalFile()
                if path.endswith(self.parent().file_type):
                    logging.info('adding %s via drag and drop' % path)
                    central_widget.append_data(model, url.toLocalFile())
            e.accept()
