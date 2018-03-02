from os import path

import ezdxf

from dxf_file import reverse_coords
from geometry_checks import is_intersect, inside_polygon
from xml_file import get_list_of_XmlFiles


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
        """ It's a tuple(tuples)"""
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
        XmlFiles = get_list_of_XmlFiles(settings, source)
        # Checking for is_intersect and is_inpolygon
        checks = self.geometry_checks(XmlFiles)
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

    def geometry_checks(self, XmlFiles):
        """Checks for both is_intersect and is_inpolygon checks."""
        res = set()
        for XmlFile in XmlFiles:
            # We don't want to waste time on flats or blank Xmls
            if XmlFile.xml_type == 'KPOKS' or not XmlFile.parcels:
                continue
            for name, parcel in XmlFile.parcels.items():
                for mydxf_contur in self.coords:
                    # This variable is for first (is_intersect check)
                    mydxf_previous_point = mydxf_contur[0]
                    flags = []
                    for mydxf_point in mydxf_contur:
                        flag = 0
                        for xml_contur in parcel:
                            # first check is is_intersect,
                            # details in module geometry_checks
                            xml_previous_point = xml_contur[0]
                            for xml_point in xml_contur:
                                if mydxf_point == mydxf_previous_point:
                                    pass
                                else:
                                    segment1 = (mydxf_point, mydxf_previous_point)
                                    segment2 = (xml_point, xml_previous_point)
                                    if is_intersect(segment1, segment2):
                                        res.add(name)
                            # second check is_inpolygon
                            # flag represents how many times each point
                            # contains in mydxf_contur
                            # if all of them == each other and % 2 == 0
                            # don't add contur to result
                            if inside_polygon(*mydxf_point, xml_contur):
                                flag += 1
                        flags.append(flag)
                    if is_equal(flags) & flags[0] == 0 & flags[0] % 2:
                        pass
                    else:
                        res.add(name)
                        # end of check is_inpolygon
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


def get_list_of_MyDxfFiles(settings, source='settings'):
    """ Returns list of XmlFile class objects """
    # if source == 'settings':
    #     file_paths = settings.get_mydxf_list()
    #     # TODO get file_paths from qt window
    # else:
    #     raise WrongArguments
    mydxf_list = settings.get_file_list('my_dxf_file_path')
    res = []
    for file in mydxf_list:
        mydxf_file = MyDxfFile(file, settings)
        res.append(mydxf_file)
    return res
