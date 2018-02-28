from os import path
from pprint import pformat

from lxml import etree

from dxf_file import DxfFile


class XmlFile():
    """ Class for a single rosreestr xml file """

    def __init__(self, file_path, settings):
        self.settings = settings
        self.file_path = file_path
        self.basename_file_path = path.basename(file_path)
        self.tree = etree.parse(file_path)
        self.root = self.tree.getroot()
        self.parcels = self.get_parcels()
        self.parcels.update(self.get_blocks())  # parcels now contains blocks!!!

    def __str__(self):
        p = pformat(self.parcels)
        return p

    def get_parcels(self):
        """ Here we are getting dict of parcels with coordinates """
        result = {}
        for parcel in self.root.iter('{*}Parcel'):
            cadastral_number = parcel.attrib['CadastralNumber']
            conturs = self.get_parcel_conturs(parcel)
            result[cadastral_number] = conturs
        return result

    def get_parcel_conturs(self, parcel):
        """ Subfunction for get_parcels function,
        returns list of conturs with tuple of coords """
        result = []
        for contur in parcel.iter('{*}SpatialElement'):
            result.append([])
            for point in contur.iter('{*}Ordinate'):
                x = float(point.attrib['X'])
                y = float(point.attrib['Y'])
                result[-1].append((x, y))
        return result

    def get_blocks(self):
        """ Here we are getting dict of blocks with coordinates """
        result = {}
        for block in self.root.iter('{*}CadastralBlock'):
            cadastral_number = block.attrib['CadastralNumber']
            conturs = self.get_block_conturs(block)
            result[cadastral_number] = conturs
        return result

    def get_block_conturs(self, parcel):
        """ Subfunction for get_blocks function
        returns list of conturs with tuple of coords """
        for contur in parcel.iterchildren('{*}SpatialData'):
            result = self.get_parcel_conturs(contur)
        return result

    def convert_to_dxffile(self):
        dxffile = DxfFile(self)
        dxffile.draw_conturs_and_save()


def get_list_of_xmlfiles(settings):
    """ Returns list of XmlFile class objects """
    res = []
    for file in settings.get_xml_list():
        xml_file = XmlFile(file, settings)
        res.append(xml_file)
    return res
