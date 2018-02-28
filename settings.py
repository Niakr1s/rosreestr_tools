import json
from os import path, mkdir, scandir


def init_constants():
    """ color_iter, colors: colors in dxf file
    dxf_folder_path - for dxf output files
    xml_folder_path - for xml input files
    my_dxf_file_path - for user file to check in xmls
    my_dxf_check_path - result of my file check """
    settings = {'color_iter': 0, 'colors': [1, 2, 4, 5, 6, 34, 84, 234], 'dxf_folder_path': path.abspath('xml\\dxf'),
                'xml_folder_path': path.abspath('xml'),
                'my_dxf_file_path': path.abspath('xml\\my_dxf_file\\my_dxf_file.dxf'),
                'my_dxf_check_path': path.abspath('xml\\my_dxf_file\\my_dxf_check.txt'),
                'merged_dxf_path': path.abspath('xml\\dxf\\merged\\merged.dxf')}
    return settings


class Settings():
    def __init__(self):
        """ settings.json should be in app path """
        self.json_settings_path = path.abspath('settings.json')
        if not self.load_settings():
            self.settings = init_constants()
            self.dump_settings()
            print('Settings file not found, created it.')
        self.check_paths()

    def get_next_color(self):
        self.settings['color_iter'] += 1
        if self.settings['color_iter'] >= len(self.settings['colors']):
            self.settings['color_iter'] = 0
        return self.settings['colors'][self.settings['color_iter']]

    def check_paths(self):
        if not path.exists(self.settings['xml_folder_path']):
            print('xml_folder_path created')
            mkdir(self.settings['xml_folder_path'])
        if not path.exists(self.settings['dxf_folder_path']):
            print('dxf_folder_path created')
            mkdir(self.settings['dxf_folder_path'])
        if not path.exists(path.dirname(self.settings['my_dxf_check_path'])):
            print('my_dxf_check_path created')
            mkdir(path.dirname(self.settings['my_dxf_check_path']))
        if not path.exists(path.dirname(self.settings['merged_dxf_path'])):
            print('merged_dxf_path created')
            mkdir(path.dirname(self.settings['merged_dxf_path']))

    def get_xml_list(self):
        return get_file_list(self.settings['xml_folder_path'], '.xml')

    def get_dxf_list(self):
        return get_file_list(self.settings['dxf_folder_path'], '.dxf')

    def dump_settings(self):
        """ Dumps to json_file settings,
        recommended to call this when adding new setting"""
        with open(self.json_settings_path, 'w') as file:
            # json.dump(attrs, file, indent='    ')
            json.dump(self.settings, file, indent='    ')

    def load_settings(self):
        """ Load settings from json_file and initialize with them """
        try:
            with open(self.json_settings_path) as file:
                settings = json.load(file)
        except FileNotFoundError:
            return False
        self.settings = settings
        print('Settings loaded fom file')
        return True


def get_file_list(input_path, pattern):
    """ Pattern should be '.xml' or '.dxf' """
    res = []
    with scandir(input_path) as it:
        for entry in it:
            if entry.is_file() and pattern in entry.name:
                res.append(entry.path)
    return res


if __name__ == '__main__':
    settings = Settings()
    print(settings.settings)
    print(settings.settings['color_iter'])
    settings.get_next_color()
    print(settings.settings['color_iter'])
