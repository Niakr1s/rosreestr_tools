from os import path, mkdir, scandir


class Settings():
    def __init__(self):
        # Some input / output pathes
        self.xml_folder_path = path.abspath('xml')
        self.dxf_folder_path = path.abspath('xml\\dwg')
        self.xml_list = self.get_xml_list()
        self.check_pathes()
        # Colors
        self.colors = (1, 2, 4, 5, 6, 34, 84, 234)
        self.color_iter = 0
        self.my_dxf_file_path = path.abspath(
            'xml\\my_dxf_file\\my_dxf_file.dxf')
        self.my_dxf_check_path = path.abspath(
            'xml\\my_dxf_file\\my_dxf_check.txt')

    def get_next_color(self):
        self.color_iter += 1
        if self.color_iter >= len(self.colors):
            self.color_iter = 0
        return self.colors[self.color_iter]

    def check_pathes(self):
        if not path.exists(self.xml_folder_path):
            mkdir(self.xml_folder_path)
        if not path.exists(self.dxf_folder_path):
            mkdir(self.dxf_folder_path)

    def get_file_list(self, path, pattern):
        """ Pattern should be '.xml' or '.dxf' """
        res = []
        with scandir(path) as it:
            for entry in it:
                if entry.is_file() and pattern in entry.name:
                    res.append(entry.path)
        return res

    def get_xml_list(self):
        return self.get_file_list(self.xml_folder_path,
                                  '.xml')

    def get_dxf_list(self):
        return self.get_file_list(self.dxf_folder_path,
                                  '.dxf')


if __name__ == '__main__':
    settings = Settings()
    print(settings.xml_folder_path, settings.dxf_folder_path)
    print(settings.colors)
    for _ in range(8):
        print(settings.next_color())
