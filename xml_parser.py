from lxml import etree
from pprint import pprint, pformat
from os import path
from settings import Settings
from xml2dxf import RRxml2dxf


class RRxml():
    """ Class for a single rosreestr xml file """

    def __init__(self, file_path, settings):
        self.settings = settings
        self.file_path = file_path
        self.basename_file_path = path.basename(file_path)
        self.tree = etree.parse(file_path)
        self.root = self.tree.getroot()
        self.blocks = self.get_blocks()
        self.parcels = self.get_parcels()

    def __str__(self):
        b = pformat(self.blocks)
        p = pformat(self.parcels)
        return b + '\n\n' + p

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


def get_list_of_rrxmls(settings):
    result = []
    for file in settings.get_xml_list():
        print(file)
        result.append(RRxml(file, settings))
    return result


def convert_all_xml2dxf(settings):
    """ Converts all xml files from settings.settings['xml_folder_path']
    to settings.settings['dxf_folder_path'] """
    for file in settings.get_xml_list():
        print(file)
        xml_file = RRxml(file, settings)
        pprint(xml_file.blocks)
        pprint(xml_file.parcels)
        RRxml2dxf(xml_file, settings).save_dxf()
