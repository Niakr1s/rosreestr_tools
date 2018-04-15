from PyQt5 import QtCore

from scripts.actions import merge_dxfs


class MergeDxfsThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, settings, source, merged_path, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.settings = settings
        self.source = source
        self.merged_path = merged_path

    def run(self):
        print('run')
        merge_dxfs(self.settings, self.source, self.merged_path)
