from os import path, mkdir, scandir
import json


class Settings():
    def __init__(self):
        """ settings.json should be in app path """
        self.json_settings_path = path.abspath('settings.json')
        if not self.load_settings():
            self.init_constants()
            self.dump_settings()

    def init_constants(self):
        """ color_iter, colors: colors in dxf file
        dxf_folder_path - for dxf output files
        xml_folder_path - for xml input files
        my_dxf_file_path - for user file to check in xmls
        my_dxf_check_path - result of my file check """
        self.settings = {
            'color_iter': 0,
            'colors': [1, 2, 4, 5, 6, 34, 84, 234],
            'dxf_folder_path': path.abspath('xml\\dwg'),
            'xml_folder_path': path.abspath('xml'),
            'my_dxf_file_path': path.abspath(
                'xml\\my_dxf_file\\my_dxf_file.dxf'),
            'my_dxf_check_path': path.abspath(
                'xml\\my_dxf_file\\my_dxf_check.txt')}
        # # Some input / output pathes
        # self.settings['xml_folder_path'] = path.abspath('xml')
        # self.settings['dxf_folder_path'] = path.abspath('xml\\dwg')
        # self.check_pathes()
        # # Colors
        # self.settings['colors'] = (1, 2, 4, 5, 6, 34, 84, 234)
        # self.settings['color_iter'] = 0
        # self.settings['my_dxf_file_path'] = path.abspath(
        #     'xml\\my_dxf_file\\my_dxf_file.dxf')
        # self.settings['my_dxf_check_path'] = path.abspath(
        #     'xml\\my_dxf_file\\my_dxf_check.txt')

    def get_next_color(self):
        self.settings['color_iter'] += 1
        if self.settings['color_iter'] >= len(self.settings['colors']):
            self.settings['color_iter'] = 0
        return self.settings['colors'][self.settings['color_iter']]

    def check_pathes(self):
        if not path.exists(self.settings['xml_folder_path']):
            mkdir(self.settings['xml_folder_path'])
        if not path.exists(self.settings['dxf_folder_path']):
            mkdir(self.settings['dxf_folder_path'])

    def get_file_list(self, path, pattern):
        """ Pattern should be '.xml' or '.dxf' """
        res = []
        with scandir(path) as it:
            for entry in it:
                if entry.is_file() and pattern in entry.name:
                    res.append(entry.path)
        return res

    def get_xml_list(self):
        return self.get_file_list(self.settings['xml_folder_path'],
                                  '.xml')

    def get_dxf_list(self):
        return self.get_file_list(self.settings['dxf_folder_path'],
                                  '.dxf')

    def dump_settings(self):
        """ Dumps to json_file settings,
        recommended to call this when adding new setting"""
        attrs = self.get_all_attrs()
        with open(self.json_settings_path, 'w') as file:
            json.dump(attrs, file, indent='    ')

    def load_settings(self):
        """ Load settings from json_file and initialize with them """
        try:
            with open(self.json_settings_path) as file:
                settings = json.load(file)
        except FileNotFoundError:
            return False
        except Exception:
            return False
        self.settings = settings

    def get_all_attrs(self):
        result = {attr: getattr(self, attr)
                  for attr in dir(self)
                  if not callable(getattr(self, attr)) and
                  not attr.startswith('__') and
                  'json_settings_path' not in attr}
        return result


if __name__ == '__main__':
    settings = Settings()
    print(settings.settings)
    print(settings.settings['color_iter'])
    settings.get_next_color()
    print(settings.settings['color_iter'])
