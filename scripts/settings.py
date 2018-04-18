import os
import platform

COLORS = {'color_type': {'block': 7, 'parcel': 8, 'oks': 63}}

if platform.system() == 'Windows':
    DESKTOP_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\rosreestr_tools_files')
else:
    DESKTOP_PATH = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\\rosreestr_tools_files')

PATHS = {
    'paths': {'xml_folder': os.path.join(DESKTOP_PATH, 'xml'), 'mydxf_folder': os.path.join(DESKTOP_PATH, 'mydxf')}}
FORMATTED_TXT = 'formatted.txt'
MERGED_DXF = 'merged.dxf'


class Settings:
    def __init__(self):
        """ settings is ConfigParser object """

        self.settings = PATHS
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

    @staticmethod
    def get_formatted_txt():
        return os.path.join(DESKTOP_PATH, FORMATTED_TXT)

    @staticmethod
    def get_merged_dxf():
        return os.path.join(DESKTOP_PATH, MERGED_DXF)
