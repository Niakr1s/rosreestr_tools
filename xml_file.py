import os
from pprint import pformat

from lxml import etree

from dxf_file import DxfFile
from exceptions import NotABlock


class XmlFile():
    """ Class for a single rosreestr xml file """

    def __init__(self, file_path, settings):
        self.settings = settings
        self.file_path = file_path
        self.basename_file_path = os.path.basename(file_path)
        self.tree = etree.parse(file_path)
        self.root = self.tree.getroot()
        self.parcels = self.get_parcels()
        self.head_parcel = tuple(self.parcels.keys())[0]
        self.update_parcels_with_blocks()
        # self.parcels and self.head_name should be updated after this with
        # string like '21:01:000000' if it is a block

    def __str__(self):
        p = pformat(self.parcels)
        return p

    def update_parcels_with_blocks(self):
        """Updates self.parcels with blocks if any,
        also updates self.head_parcel if any block.
        If xml is not a block, returns only parcels
        Also sets self.head_parcel='21:01:000000' if block
                            or '21:01:000000:00' if parcel"""
        try:  # Updates self.parcels with blocks and updates self.suggested_name
            blocks = self.get_blocks()
            self.parcels.update(blocks)  # parcels now contains blocks!!!
            self.head_parcel = tuple(blocks.keys())[0]
        except NotABlock:
            print('%s is a parcel' % self.file_path)
        finally:
            print('%s is a block' % self.file_path)

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
        try:
            for block in self.root.iter('{*}CadastralBlock'):
                cadastral_number = block.attrib['CadastralNumber']
                conturs = self.get_block_conturs(block)
                result[cadastral_number] = conturs
            return result
        except KeyError:
            raise NotABlock

    def get_block_conturs(self, parcel):
        """ Subfunction for get_blocks function
        returns list of conturs with tuple of coords """
        for contur in parcel.iterchildren('{*}SpatialData'):
            result = self.get_parcel_conturs(contur)
        return result

    def convert_to_dxffile(self):
        dxffile = DxfFile(self)
        dxffile.draw_conturs_and_save()

        # def pretty_rename(self):
        #     if os.path.basename(self.file_path) !=



def get_list_of_xmlfiles(settings, source='settings'):
    """ Returns list of XmlFile class objects """
    # if source == 'settings':
    #
    #     # TODO get file_paths from qt window
    # else:
    #     raise WrongArguments
    xml_paths = settings.get_file_list('xml_folder_path')
    res = []
    for file in xml_paths:
        xml_file = XmlFile(file, settings)
        res.append(xml_file)
    return res
