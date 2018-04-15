import json
import os
import platform

if platform.system() == 'Windows':
    DESKTOP_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\rosreestr_tools_files')
elif platform.system() == 'Linux':
    DESKTOP_PATH = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop\\rosreestr_tools_files')


def init_defaults(with_pathes):
    """ color_iter, colors: colors in dxf file
    dxf_folder_path - for dxf output files
    xml_folder_path - for xml input files
    my_dxf_file_path - for user file to check in xmls
    check_txt_path - result of my file check """
    defaults = {'color_type': {'block': 7, 'parcel': 8, 'oks': 63}}
    if with_pathes:
        pathes = {'dxf_folder_path': os.path.join(DESKTOP_PATH, 'dxf'),
                  'xml_folder_path': os.path.join(DESKTOP_PATH, 'xml'),
                  'my_dxf_file_path': os.path.join(DESKTOP_PATH, 'mydxf'),
                  'check_txt_path': os.path.join(DESKTOP_PATH, 'txt'),
                  'formatted_txt_path': os.path.join(DESKTOP_PATH, 'formatted.txt'),
                  'merged_dxf_path': os.path.join(DESKTOP_PATH, 'merged.dxf')}
        defaults.update(pathes)
    return defaults


class Settings:
    def __init__(self, with_pathes=True):
        """ settings.json should be in app path """
        # self.json_settings_path = os.path.abspath('settings.json')
        self.settings = init_defaults(with_pathes)
        # self.update_settings_from_json()
        if with_pathes:
            self.check_paths()

    def check_paths(self):
        os.makedirs(self.settings['xml_folder_path'], exist_ok=True)
        os.makedirs(self.settings['dxf_folder_path'], exist_ok=True)
        os.makedirs(self.settings['my_dxf_file_path'], exist_ok=True)
        os.makedirs(self.settings['check_txt_path'], exist_ok=True)
        os.makedirs(os.path.dirname(self.settings['merged_dxf_path']), exist_ok=True)

    def get_file_list(self, key, pattern):
        """ Key is from self.settings dict,
        for example 'xml_folder_path', 'check_txt_path' etc
        pattern is '.dxf' string """
        res = []
        with os.scandir(self.settings[key]) as it:
            for entry in it:
                if entry.is_file() and pattern in entry.name:
                    res.append(entry.path)
        return res

    def dump_settings(self):
        """ Dumps to json_file settings,
        recommended to call this when adding new setting"""
        with open(self.json_settings_path, 'w') as file:
            # json.dump(attrs, file, indent='    ')
            json.dump(self.settings, file, indent='    ')

    def update_settings_from_json(self):
        """ Load settings from json_file and initialize with them """
        try:
            with open(self.json_settings_path) as file:
                self.settings = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.dump_settings()


if __name__ == '__main__':
    pass
