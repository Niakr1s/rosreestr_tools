import os

from lxml import etree

import actions
from dxf_file import DxfFile
from exceptions import NoCoordinates


class XmlFile:
    """ Class for a single rosreestr xml file """

    def __init__(self, file_path, settings):
        self.settings = settings
        self.file_path = os.path.abspath(file_path)
        self.basename_file_path = os.path.basename(file_path)
        self.tree = etree.parse(file_path)
        self.root = self.tree.getroot()
        # can be KPT, KVZU, KVOKS (Flat), KPOKS (Building, Construction, Uncompleted)
        self.xml_type = remove_namespace(self.root.tag)
        self.cadastral_number = self.root.find('.//*//*[@CadastralNumber]').attrib['CadastralNumber']
        self.parcels = self.get_parcels()  # sml_subtype should update after this
        self.xml_subtype = remove_namespace(self.root.find('.//*[@CadastralNumber]').tag)
        self.check = set()  # if myxml file checked and intersect parcel

    def get_parcels(self):
        result = {}
        for item in self.root.iterfind('.//*[@CadastralNumber]'):
            cadastral_number = item.attrib['CadastralNumber']
            try:
                if len(cadastral_number.split(':')) == 3:  # if it is a block
                    actions.update(result, {cadastral_number: {'coordinates': self.get_block_conturs(item),
                                                               'type': remove_namespace(item.tag)}})
                else:
                    actions.update(result, {cadastral_number: {'coordinates': self.get_parcel_conturs(item),
                                                               'type': remove_namespace(item.tag)}})
            except NoCoordinates:
                pass
                # result[cadastral_number]['coordinates'] = self.get_parcel_conturs(item)
        # Removing blank keys
        return result

    @staticmethod
    def get_parcel_conturs(parcel):
        """ Subfunction for get_parcels function,
        returns list of conturs with tuple of coords """
        result = []
        for contur in parcel.iter('{*}SpatialElement'):
            result.append([])
            for point in contur.iter('{*}Ordinate'):
                x = float(point.attrib['X'])
                y = float(point.attrib['Y'])
                result[-1].append((x, y))
        if not result:
            raise NoCoordinates
        return result

    def get_block_conturs(self, parcel):
        """ Subfunction for get_blocks function
        returns list of conturs with tuple of coords """
        for contur in parcel.iterchildren('{*}SpatialData'):
            result = self.get_parcel_conturs(contur)
        return result

    def convert_to_dxffile(self):
        if not self.parcels:
            return
        dxffile = DxfFile(self)
        dxffile.draw_conturs_and_save()

    def pretty_rename(self):
        dirpath = os.path.dirname(self.file_path)
        cadastral_number_spaced = self.cadastral_number.replace(':', ' ') + '.xml'
        pretty_basename = ' '.join((self.xml_type, self.xml_subtype, cadastral_number_spaced))
        try:
            os.rename(self.file_path, os.path.join(dirpath, pretty_basename))
        except FileExistsError as err:
            os.remove(os.path.join(dirpath, pretty_basename))
            os.rename(self.file_path, os.path.join(dirpath, pretty_basename))


def get_list_of_XmlFiles(settings, source='settings'):
    """ Returns list of XmlFile class objects
    if settings='gui' - get list from gui"""
    xml_paths = settings.get_file_list('xml_folder_path')
    res = []
    for file in xml_paths:
        xml_file = XmlFile(file, settings)
        res.append(xml_file)
    return res


def remove_namespace(not_pretty_tag):
    return not_pretty_tag.split('}')[-1]


if __name__ == '__main__':
    from settings import Settings
    settings = Settings()
    xml = XmlFile(r'd:\github\rosreestr_tools\files\xml\KPT CadastralBlock 21 02 010103.xml', settings)
    xml.convert_to_dxffile()
    xml = XmlFile(r'd:\Dropbox\xml\зд.xml', settings)
    xml.convert_to_dxffile()
