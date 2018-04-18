import configparser
import os
import platform

if platform.system() == 'Windows':
    DESKTOP_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\rosreestr_tools_files')
elif platform.system() == 'Linux':
    DESKTOP_PATH = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\\rosreestr_tools_files')

PATHS = {'paths': {'dxf_folder_path': os.path.join(DESKTOP_PATH, 'dxf'),
                   'xml_folder_path': os.path.join(DESKTOP_PATH, 'xml'),
                   'my_dxf_file_path': os.path.join(DESKTOP_PATH, 'mydxf'),
                   'check_txt_path': os.path.join(DESKTOP_PATH, 'txt'),
                   'formatted_txt_path': os.path.join(DESKTOP_PATH), 'merged_dxf_path': os.path.join(DESKTOP_PATH)}}

INI = 'settings.ini'
FORMATTED = 'formatted.txt'
MERGED = 'merged.dxf'


class Settings:
    def __init__(self):
        """ settings is ConfigParser object """
        self.settings = configparser.ConfigParser()
        try:
            self.settings.read_file(open(INI))
        except FileNotFoundError:
            self.settings = init_defaults()
        self.check_paths()

    def check_paths(self):
        for i in self.settings['paths'].values():
            os.makedirs(i, exist_ok=True)

    def get_file_list(self, key, pattern):
        """ Key is from self.settings['paths'],
        for example 'xml_folder_path', 'check_txt_path' etc
        pattern is '.dxf' string """
        res = []
        with os.scandir(self.settings['paths'][key]) as it:
            for entry in it:
                if entry.is_file() and pattern in entry.name:
                    res.append(entry.path)
        return res

    @staticmethod
    def init_defaults():
        defaults = PATHS
        settings = configparser.ConfigParser()
        settings.read_dict(defaults)
        settings.write(open(INI, 'w'))
        return settings


if __name__ == '__main__':
    s = Settings()
    print(str(s.settings['paths']))
    print(s.get_file_list('dxf_folder_path', 'dxf'))
