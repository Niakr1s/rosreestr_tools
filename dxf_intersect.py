from intersection import is_intersect
import ezdxf
from settings import Settings
from xml2dxf import reverse_coords
from xml_parser import get_list_of_rrxmls


class MyDxfFile():
    def __init__(self, settings):
        self.settings = settings
        self.my_dxf_file = ezdxf.readfile(self.settings.my_dxf_file_path)
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
        return res

    def check(self):
        """ Main function for checking """
        settings = self.settings
        rrxmls = get_list_of_rrxmls(settings)
        mydxffile = MyDxfFile(settings)
        print('Checking for intersection')
        check1 = self.check_intersect(mydxffile, rrxmls)
        print('Checking for inpolygon')
        check2 = self.check_inpolygon(mydxffile, rrxmls)
        checks = check1 | check2
        return sorted(checks)

    def check_intersect(self, mydxffile, rrxmls):
        res = set()
        for contur in mydxffile.coords:
            for i in range(len(contur) - 1):
                for rrxml in rrxmls:
                    for k, v in rrxml.blocks.items():
                        for contur_xml in v:
                            for j in range(len(contur_xml) - 1):
                                segment1 = (contur[i], contur[i + 1])
                                segment2 = (contur_xml[j], contur_xml[j + 1])
                                if is_intersect(segment1, segment2):
                                    print('Intersects, ', k)
                                    res.add(k)
                    for k, v in rrxml.parcels.items():
                        for contur_xml in v:
                            for j in range(len(contur_xml) - 1):
                                segment1 = (contur[i], contur[i + 1])
                                segment2 = (contur_xml[j], contur_xml[j + 1])
                                if is_intersect(segment1, segment2):
                                    print('Intersects, ', k)
                                    res.add(k)
        return res

    def check_inpolygon(self, mydxffile, rrxmls):
        res = set()
        for contur in mydxffile.coords:
            for point in contur:
                for rrxml in rrxmls:
                    for k, v in rrxml.blocks.items():
                        for contur_xml in v:
                            if inside_polygon(*point, contur_xml):
                                print('Intersects, ', k)
                                res.add(k)
                    for k, v in rrxml.parcels.items():
                        for contur_xml in v:
                            if inside_polygon(*point, contur_xml):
                                print('Intersects, ', k)
                                res.add(k)
        return res


def inside_polygon(x, y, points):
    """
    Return True if a coordinate (x, y) is inside a polygon defined by
    a list of verticies [(x1, y1), (x2, x2), ... , (xN, yN)].

    Reference: http://www.ariel.com.au/a/python-point-int-poly.html
    """
    n = len(points)
    inside = False
    p1x, p1y = points[0]
    for i in range(1, n + 1):
        p2x, p2y = points[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


if __name__ == '__main__':
    settings = Settings()
    my = MyDxfFile(settings)
    print(my.check())
