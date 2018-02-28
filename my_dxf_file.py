import ezdxf

from actions import get_list_of_xmlfiles
from dxf_file import reverse_coords
from geometry_checks import is_intersect, inside_polygon
from settings import Settings


class MyDxfFile():
    def __init__(self, settings):
        self.settings = settings
        self.my_dxf_file = ezdxf.readfile(
            self.settings.settings['my_dxf_file_path'])
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

    def check(self):
        """ Main function for checking dxf file in xmls,
        returns not sorted set """
        settings = self.settings
        list_of_xmlfiles = get_list_of_xmlfiles(settings)
        mydxffile = MyDxfFile(settings)
        print('Checking for geometry_checks')
        check1 = self.check_intersect(mydxffile, list_of_xmlfiles)
        print('Checking for inpolygon')
        check2 = self.check_inpolygon(mydxffile, list_of_xmlfiles)
        checks = check1 | check2
        self.check_to_file(checks)
        return checks

    def check_to_file(self, checks):
        """ Saves SORTED check() result to file and prints in console """
        sorted_checks = [*[i for i in sorted(checks) if
                           len(i.split(':')) == 3],
                         *[i for i in sorted(checks) if
                           len(i.split(':')) != 3]]
        output_path = self.settings.settings['my_dxf_check_path']
        print('\n\nВаш dxf файл проходит по следующим участкам:')
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
    settings = Settings()
    my = MyDxfFile(settings)
    print(my.check())
