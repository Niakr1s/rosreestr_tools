from os import path

import ezdxf

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
        self.coords = self.get_reversed_coords()

    def get_coords(self):
        """ It's a dict(tuples):
        'LWPOLYLINE' = ((0,0), (1,1), (3,3)), ((0,0), (1,1), (3,3)), ...
        'POLYLINE' = ((0,0), (1,1), (3,3)), ((0,0), (1,1), (3,3)), ...
        'LINE' = ((0,0), (1,1)), ((0,0), (1,1)),
        'POINT' = (0,0), (1,1), (3,3), ...
        'CIRCLE' = ((0,0),3), ((1,1),2), ((3,3),6), ... (3rd item is radius)"""
        # res = {'LWPOLYLINE': [], 'POLYLINE': [], 'LINE': [],
        #        'POINT': [[]], 'CIRCLE': [[]]}  # Due reuse of is_inpolygon method
        res = {}
        for e in self.msp:
            if e.dxftype() == 'LWPOLYLINE':
                coords = []
                for coord in e.get_rstrip_points():
                    coords.append(coord)
                # res['LWPOLYLINE'].append(coords)
                if 'LWPOLYLINE' not in res:
                    res['LWPOLYLINE'] = []
                res['LWPOLYLINE'].append(coords)
            elif e.dxftype() == 'POLYLINE':
                coords = []
                for x, y, _ in e.points():
                    coords.append((x, y))
                # res['POLYLINE'].append(coords)
                if 'POLYLINE' not in res:
                    res['LWPOLYLINE'] = []
                res['LWPOLYLINE'].append(coords)
            elif e.dxftype() == 'LINE':
                startx, starty = e.dxf.start[0:2]
                endx, endy = e.dxf.end[0:2]
                # res['LINE'].append(((startx, starty), (endx, endy)))
                if 'LINE' not in res:
                    res['LINE'] = []
                res['LINE'].append(((startx, starty), (endx, endy)))
            elif e.dxftype() == 'POINT':
                if 'POINT' not in res:
                    res['POINT'] = [[]]
                res['POINT'][0].append((e.dxf.location[0:2]))
                # res['POINT'][-1].append(e.dxf.location)
            elif e.dxftype() == 'CIRCLE':
                # res['CIRCLE'][-1].append(*e.dxf.center, e.dxf.radius)
                if 'CIRCLE' not in res:
                    res['CIRCLE'] = [[]]
                res['CIRCLE'][0].append((*e.dxf.center[0:2], e.dxf.radius))
        return res

    def get_reversed_coords(self):
        result = {}
        for name, conturs in self.reversed_coords.items():
            if name in ('LWPOLYLINE, POLYLINE, LINE'):
                result[name] = [[(y, x) for x, y in contur] for contur in conturs]
            elif name in ('CIRCLE'):
                result[name] = [[(y, x, z) for x, y, z in i] for i in conturs]
            elif name in ('POINT'):
                result[name] = [[(y, x) for x, y in i] for i in conturs]
        return result

    def checks(self, source='settings'):
        """ Main function for checking dxf file in xmls """
        settings = self.settings
        XmlFiles = get_list_of_XmlFiles(settings, source)
        # Checking for is_intersect and is_inpolygon
        self.geometry_checks(XmlFiles)  # This function updates XmlFiles.check
        self.save_checks_to_file(XmlFiles)

    def geometry_checks(self, XmlFiles):
        """Checks for multiple files both is_intersect and is_inpolygon checks."""
        for XmlFile in XmlFiles:
            # We don't want to waste time on Flats and blank Xmls
            if XmlFile.xml_type == 'KPOKS' or not XmlFile.parcels:
                continue
            # We don't want to waste time on full KPT check if not nessessary
            elif XmlFile.xml_type == 'KPT':
                test = self.geometry_check(XmlFile, XmlFile.cadastral_number)
                if not XmlFile.check:
                    continue
            # Checking in whole dictionary
            for parcel_name in XmlFile.parcels.keys():
                self.geometry_check(XmlFile, parcel_name)

    def geometry_check(self, XmlFile, parcel_name):
        """This functon checks self.coords based on keys in XmlFile class instance"""
        for mydxf_name, mydxf_conturs in self.coords.items():
            for mydxf_contur in mydxf_conturs:
                # If it is a line or polyline checking both is_intersect and is_inpolygon
                if mydxf_name in ('LWPOLYLINE', 'POLYLINE', 'LINE'):
                    # Breaking cycles if not nessessary
                    if parcel_name not in XmlFile.check:
                        self.is_intersect_check(XmlFile, parcel_name, mydxf_contur)
                    if parcel_name not in XmlFile.check:
                        self.is_inpolygon_check(XmlFile, parcel_name, mydxf_contur)
                        # TODO point, circle checks
                elif mydxf_name in ('POINT', 'CIRCLE'):
                    if parcel_name not in XmlFile.check:
                        self.is_inpolygon_check(XmlFile, parcel_name, mydxf_contur)

    def is_intersect_check(self, XmlFile, parcel_name, mydxf_contur):
        """First check, checking if line or polyline contur
                is intersecting XmlFile parcel"""
        parcel = XmlFile.parcels[parcel_name]
        mydxf_previous_point = mydxf_contur[0]
        for mydxf_point in mydxf_contur:
            for xml_contur in parcel:
                # first check is is_intersect,
                # details in module geometry_checks
                xml_previous_point = xml_contur[0]
                for xml_point in xml_contur:
                    if not (mydxf_point == mydxf_previous_point):
                        segment1 = (mydxf_point, mydxf_previous_point)
                        segment2 = (xml_point, xml_previous_point)
                        if is_intersect(segment1, segment2):
                            XmlFile.check.add(parcel_name)

    def is_inpolygon_check(self, XmlFile, parcel_name, mydxf_contur):
        """Second check, checking if points in contur
                (can be separate poings, or points of line or polyline
                is lying in XmlFile parcel"""
        parcel = XmlFile.parcels[parcel_name]
        flags = []
        for mydxf_point in mydxf_contur:
            flag = 0
            for xml_contur in parcel:
                # second check is_inpolygon
                # flag represents how many times each point
                # contains in mydxf_contur
                # if all of them == each other and % 2 == 0
                # don't add contur to result
                if inside_polygon(mydxf_point[0], mydxf_point[1], xml_contur):
                    flag += 1
            flags.append(flag)
        if is_equal(flags) & flags[0] == 0 & flags[0] % 2:
            pass
        else:
            XmlFile.check.add(parcel_name)

    def save_checks_to_file(self, XmlFiles):
        """ Saves SORTED check() result to file and prints in console """
        checks = self.get_checks(XmlFiles)
        basename = path.basename(self.file_path).replace('.dxf', '.txt')
        output_path = path.join(self.settings.settings['my_dxf_check_path'], basename)
        with open(output_path, 'w') as file:
            for k, v in checks.items():
                if v:
                    print(k, file=file)
                    for i in v:
                        print(i, file=file)
        print('Result saved to file %s' % (output_path))

    def get_checks(self, XmlFiles):
        """getting checks from XmlFiles"""
        parcels, okses = set(), set()
        for XmlFile in XmlFiles:
            if XmlFile.check:
                if XmlFile.xml_type in ('KPT', 'KVZU'):
                    parcels |= XmlFile.check
                elif XmlFile.xml_type == 'KVOKS':
                    okses |= XmlFile.check
        result = {}
        result['Parcels'] = sort_result(parcels)
        result['OKSes'] = sort_result(okses)
        return result


def sort_result(result):
    return sorted(result, key=lambda x: (int(x.split(':')[-2]), int(x.split(':')[-1])))


def is_equal(lst: list):
    """Checks if all items in list are same
    """
    c = lst[0]
    for i in lst:
        if i != c:
            return False
    return True


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


def append_if(lst, k, v):
    if k not in lst:
        lst[k] = []
    lst[k].append(v)
    return lst


if __name__ == '__main__':
    from settings import Settings

    settings = Settings()
    my = MyDxfFile('xml\\mydxfs\\my_dxf_file.dxf', settings)
    print(my.coords)
    print(my.reversed_coords)
    my = MyDxfFile('xml\\mydxfs\\my_dxf_file - копия.dxf', settings)
    print(my.coords)
    print(my.reversed_coords)
