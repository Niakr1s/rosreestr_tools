import os
import platform

# This module only for console version, maybe except COLORS section, that affects GUI convert function too


COLORS = {'color_type': {'block': 7, 'parcel': 8, 'oks': 63}}  # colors for dxf files, converted from xml files

if platform.system() == 'Windows':
    DESKTOP_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\rosreestr_tools_files')
else:
    DESKTOP_PATH = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\\rosreestr_tools_files')


class Settings:
    def __init__(self, base_dir=DESKTOP_PATH):
        self.base_dir = DESKTOP_PATH
        paths = {
            'paths': {'xml_folder': os.path.join(base_dir, 'xml'), 'mydxf_folder': os.path.join(base_dir, 'mydxf')}}
        self.settings = paths

        self.formatted_txt = os.path.join(self.base_dir, 'formatted.txt')
        self.merged_dxf = os.path.join(self.base_dir, 'merged.dxf')

        self.check_paths()

    def check_paths(self):
        for i in self.settings['paths'].values():
            os.makedirs(i, exist_ok=True)

    def get_file_list(self, key, pattern):
        """ Key is from self.settings['paths'],
        for example 'xml_folder', 'mydxf_folder' etc
        pattern is '.dxf' string """
        res = []
        with os.scandir(self.settings['paths'][key]) as it:
            for entry in it:
                if entry.is_file() and pattern in entry.name:
                    res.append(entry.path)
        return res
