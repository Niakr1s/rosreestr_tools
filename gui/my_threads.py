from PyQt5 import QtCore

from scripts import actions, my_dxf_file, xml_file


class MyDxfCheckThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal(str)

    def __init__(self, my_dxf_file_paths, xml_file_pathes, callback, parent=None):
        super().__init__(parent)
        self.my_dxf_file_paths = my_dxf_file_paths
        self.xml_file_pathes = xml_file_pathes
        self.finished.connect(callback)

    def run(self):
        checks_formatted = self.checks()
        self.finished.emit(checks_formatted)

    def checks(self):
        all_checks = {}
        for my_dxf_file_path in self.my_dxf_file_paths:
            self.signal.emit('Обрабатываю %s' % my_dxf_file_path)
            my_dxf = my_dxf_file.MyDxfFile(my_dxf_file_path, self.parent().settings)
            checks = my_dxf.checks(self.xml_file_pathes, save_to_file=False)
            actions.update(all_checks, checks)
        checks_formatted = my_dxf_file.checks_to_formatted_string(source=all_checks)
        return checks_formatted


class XmlConvertThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)

    def __init__(self, file_paths, parent=None):
        super().__init__(parent)

        self.file_paths = file_paths

    def run(self):
        self.convert()

    def convert(self):
        for file_path in self.file_paths:
            self.signal.emit('Обрабатываю %s' % file_path)
            xml = xml_file.XmlFile(file_path, self.parent().settings)
            xml.convert_to_dxffile()
