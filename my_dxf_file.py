from os import path

import ezdxf

from dxf_file import reverse_coords
from geometry_checks import is_intersect, inside_polygon
from xml_file import get_list_of_xmlfiles


class MyDxfFile:
    def __init__(self, file_path, settings):
        self.settings = settings
        self.file_path = file_path
        self.my_dxf_file = ezdxf.readfile(self.file_path)
        self.msp = self.my_dxf_file.modelspace()
        # It's reversed coords from dxf!
        self.reversed_coords = self.get_coords()
        # It's normal coords like in xml.
        self.coords = reverse_coords(self.reversed_coords)

    def get_coords(self):
        res = []
        for e in self.msp:
            if e.dxftype() == 'LWPOLYLINE':
                coords = []
                for coord in e.get_rstrip_points():
                    coords.append(coord)
                res.append(tuple(coords))
            elif e.dxftype() == 'LINE':
                startx, starty = e.dxf.start[0:2]
                endx, endy = e.dxf.end[0:2]
                res.append(((startx, starty), (endx, endy)))
            elif e.dxftype() == 'POLYLINE':
                coords = []
                for x, y, _ in e.points():
                    coords.append((x, y))
                res.append(coords)
        print('coords of my_dxf_file:\n', res)
        return res

    def check(self, source='settings'):
        """ Main function for checking dxf file in xmls,
        returns not sorted set """
        settings = self.settings
        list_of_xmlfiles = get_list_of_xmlfiles(settings, source)
        print('Checking for geometry_checks')
        check1 = self.check_intersect(self, list_of_xmlfiles)
        print('Checking for inpolygon')
        check2 = self.check_inpolygon(self, list_of_xmlfiles)
        checks = check1 | check2
        self.save_check_to_file(checks)
        return checks

    def save_check_to_file(self, checks):
        """ Saves SORTED check() result to file and prints in console """
        sorted_checks = [*[i for i in sorted(checks) if
                           len(i.split(':')) == 3],
                         *[i for i in sorted(checks) if
                           len(i.split(':')) != 3]]
        basename = path.basename(self.file_path).replace('.dxf', '.txt')
        output_path = path.join(self.settings.settings['my_dxf_check_path'], basename)
        print('\n\nФайл %s проходит по следующим участкам:' % (self.file_path))
        with open(output_path, 'w') as file:
            for parcel in sorted_checks:
                print(parcel)
                print(parcel, file=file)
        print('Saved to file %s' % (output_path))

    def check_intersect(self, MyDxfFile, list_of_xmlfiles):
        """First check for object of class MyDxfFile in list of XmlFile objects"""
        res = set()
        for contur in MyDxfFile.coords:
            for i in range(len(contur) - 1):
                for rrxml in list_of_xmlfiles:
                    for k, v in rrxml.parcels.items():
                        for contur_xml in v:
                            for j in range(len(contur_xml) - 1):
                                segment1 = (contur[i], contur[i + 1])
                                segment2 = (contur_xml[j], contur_xml[j + 1])
                                if is_intersect(segment1, segment2):
                                    print('Intersects, ', k)
                                    res.add(k)
        return res

    def check_inpolygon(self, MyDxfFile, list_of_xmlfiles):  # new func
        """Second check for object of class MyDxfFile in list of XmlFile objects"""
        res = set()
        for rrxml in list_of_xmlfiles:
            for name, parcel in rrxml.parcels.items():
                for mydxf_contur in MyDxfFile.coords:
                    # how many times each point of mydxf_contur
                    # contains in parcel
                    # if all of them == each other and % 2 == 0
                    # don't add contur to result
                    flags = []
                    for mydxf_point in mydxf_contur:
                        flag = 0
                        for xml_contur in parcel:
                            if inside_polygon(*mydxf_point, xml_contur):
                                flag += 1
                        flags.append(flag)
                    if is_equal(flags) & flags[0] == 0 & flags[0] % 2:
                        pass
                    else:
                        print(name, flags)
                        res.add(name)
        return res


def is_equal(lst: list):
    """Checks if all items in list are same
    """
    c = lst[0]
    for i in lst:
        if i != c:
            return False
    return True

if __name__ == '__main__':
    pass


def get_list_of_mydxffiles(settings, source='settings'):
    """ Returns list of XmlFile class objects """
    # if source == 'settings':
    #     file_paths = settings.get_mydxf_list()
    #     # TODO get file_paths from qt window
    # else:
    #     raise WrongArguments
    file_paths = settings.get_mydxf_list()
    res = []
    for file in file_paths:
        mydxf_file = MyDxfFile(file, settings)
        res.append(mydxf_file)
    return res
