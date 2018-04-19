import logging

from PyQt5 import QtCore

from scripts import actions, my_dxf_file, xml_file
from scripts.log import log


class MyDxfCheckThread(QtCore.QThread):
    # checks selected myDxfs in all XMLs

    signal = QtCore.pyqtSignal(str)  # standard signal emitted when one task completed
    finished = QtCore.pyqtSignal(str)  # signal when everything finished

    def __init__(self, my_dxf_file_paths, xml_file_paths, callback, parent=None):
        super().__init__(parent)
        self.my_dxf_file_paths = my_dxf_file_paths
        self.xml_file_pathes = xml_file_paths
        self.finished.connect(callback)  # callback - function that changes something in app

    def run(self):
        checks_formatted = self.checks()
        self.finished.emit(checks_formatted)

    @log
    def checks(self):
        checks_list = []
        for my_dxf_file_path in self.my_dxf_file_paths:
            logging.info('checking %s' % my_dxf_file_path)
            self.signal.emit('Обрабатываю %s' % my_dxf_file_path)
            my_dxf = my_dxf_file.MyDxfFile(my_dxf_file_path)
            checks = my_dxf.checks(self.xml_file_pathes, save_to_file=False)
            checks_list.append(checks)
        logging.info('checks = %s' % str(checks_list))
        checks_formatted = my_dxf_file.checks_to_formatted_string(checks_list=checks_list)
        logging.info('formatted checks = %s' % str(checks_formatted))
        return checks_formatted


class XmlConvertThread(QtCore.QThread):
    # converting selected XMLs to DXFs to same folder and merging it in one file if user wants

    signal = QtCore.pyqtSignal(str)  # standard signal emitted when one task completed

    def __init__(self, file_paths, merge=False, merged_path=None, parent=None):
        super().__init__(parent)
        self.file_paths = file_paths
        self.merge = merge
        self.merged_path = merged_path

    def run(self):
        self.convert()

    @log
    def convert(self):
        dxf_file_paths = []  # dxf files for merging
        for file_path in self.file_paths:
            logging.info('converting %s' % file_path)
            self.signal.emit('Обрабатываю %s' % file_path)
            xml = xml_file.XmlFile(file_path)
            dxf_file_path = xml.convert_to_dxffile()

            if dxf_file_path is not None:
                dxf_file_paths.append(dxf_file_path)

        if len(dxf_file_paths) > 0:
            if self.merge:
                logging.info('merging %s to %s' % (dxf_file_paths, self.merged_path))
                self.signal.emit('Объединяю в один чертеж %s' % self.merged_path)
                actions.merge_dxfs(dxf_file_paths, self.merged_path)
        else:
            # TODO: add some alert to show that selected XML files have no coordinates and nothing was done
            pass
