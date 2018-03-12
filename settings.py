import json
from os import path, makedirs, scandir


def init_defaults():
    """ color_iter, colors: colors in dxf file
    dxf_folder_path - for dxf output files
    xml_folder_path - for xml input files
    my_dxf_file_path - for user file to check in xmls
    check_txt_path - result of my file check """
    defaults = {'color_iter': 0, 'colors': [1, 2, 4, 5, 6, 34, 84, 234],
                'color_type': {'block': 7, 'parcel': 8, 'oks': 63}, 'dxf_folder_path': path.abspath('files\\dxf'),
                'xml_folder_path': path.abspath('files\\xml'), 'my_dxf_file_path': path.abspath('files\\mydxf'),
                'check_txt_path': path.abspath('files\\txt'),
                'formatted_txt_path': path.abspath('files\\txt\\formatted.txt'),
                'merged_dxf_path': path.abspath('files\\merged\\merged.dxf')}
    return defaults


class Settings:
    def __init__(self):
        """ settings.json should be in app path """
        self.json_settings_path = path.abspath('settings.json')
        self.settings = init_defaults()
        self.update_settings_from_json()
        self.check_paths()

    def get_next_color(self):
        self.settings['color_iter'] += 1
        if self.settings['color_iter'] >= len(self.settings['colors']):
            self.settings['color_iter'] = 0
        return self.settings['colors'][self.settings['color_iter']]

    def check_paths(self):
        makedirs(self.settings['xml_folder_path'], exist_ok=True)
        makedirs(self.settings['dxf_folder_path'], exist_ok=True)
        makedirs(self.settings['my_dxf_file_path'], exist_ok=True)
        makedirs(self.settings['check_txt_path'], exist_ok=True)
        makedirs(path.dirname(self.settings['merged_dxf_path']), exist_ok=True)

    def get_file_list(self, key):
        """ Key is from self.settings dict,
        for example 'xml_folder_path', 'check_txt_path' etc"""
        if 'dxf' in key:
            pattern = '.dxf'
        elif 'xml' in key:
            pattern = '.xml'
        elif 'txt' in key:
            pattern = '.txt'
        else:
            raise FileNotFoundError
        res = []
        with scandir(self.settings[key]) as it:
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
    settings = Settings()
    print(settings.settings)
    print(settings.settings['color_iter'])
    settings.get_next_color()
    print(settings.settings['color_iter'])
