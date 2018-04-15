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

    def __init__(self, file_paths, merge=False, merged_path=None, parent=None):
        super().__init__(parent)
        self.file_paths = file_paths
        self.merge = merge
        self.merged_path = merged_path

    def run(self):
        self.convert()

    def convert(self):
        dxf_file_paths = []
        for file_path in self.file_paths:
            self.signal.emit('Обрабатываю %s' % file_path)
            xml = xml_file.XmlFile(file_path, self.parent().settings)
            dxf_file_path = xml.convert_to_dxffile()
            if dxf_file_path is not None:
                dxf_file_paths.append(dxf_file_path)
        if self.merge and len(dxf_file_paths) > 0:
            print('merging: ', dxf_file_paths, self.merged_path)
            self.signal.emit('Объединяю в один чертеж %s' % self.merged_path)
            actions.merge_dxfs(self.parent().settings, dxf_file_paths, self.merged_path)
