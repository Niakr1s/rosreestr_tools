import logging
import os

from lxml import etree

from scripts import actions
from scripts.dxf_file import DxfFile
from scripts.exceptions import NoCoordinates
from scripts.log import log
from scripts.settings import Settings


class XmlFile:
    """ Class for a single rosreestr xml file """

    def __init__(self, file_path):
        self.file_path = os.path.abspath(file_path)
        self.basename_file_path = os.path.basename(file_path)
        self.tree = etree.parse(file_path)
        self.root = self.tree.getroot()
        # can be KPT, KVZU, KVOKS (Flat), KPOKS (Building, Construction, Uncompleted)
        self.xml_type = remove_namespace(self.root.tag)
        self.cadastral_number = self.root.find(
            './/*//*[@CadastralNumber]').attrib['CadastralNumber']
        self.parcels = self.get_parcels()
        self.xml_subtype = remove_namespace(
            self.root.find('.//*[@CadastralNumber]').tag)
        self.check = set()  # if myxml file checked and intersect parcel

    def get_parcels(self):
        result = {}
        for item in self.root.iterfind('.//*[@CadastralNumber]'):
            cadastral_number = item.attrib['CadastralNumber']
            try:
                if len(cadastral_number.split(':')) == 3:  # if it is a block
                    conturs = self.get_block_conturs(item)
                    actions.update(result, {cadastral_number: {'coordinates': conturs,
                                                               'type': remove_namespace(item.tag),
                                                               'rect': self.get_rect(conturs)
                                                               }})
                else:
                    conturs = self.get_parcel_conturs(item)
                    actions.update(result, {cadastral_number: {'coordinates': conturs,
                                                               'type': remove_namespace(item.tag),
                                                               'rect': self.get_rect(conturs)
                                                               }})
            except NoCoordinates:
                pass
                # result[cadastral_number]['coordinates'] = self.get_parcel_conturs(item)
        # Removing blank keys
        return result

    @staticmethod
    def get_rect(conturs):
        # gets rectangle conturs as dict {'xmin', 'ymin', 'xmax', 'ymax'}
        xs = []
        ys = []
        for contur in conturs:
            for point in contur:
                print(point)
                xs.append(point[0])
                ys.append(point[1])
        result = {
            'xmin': min(xs),
            'xmax': max(xs),
            'ymin': min(ys),
            'ymax': max(ys),
        }
        print('get_rect function, result: ', result)
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
        result = []
        for contur in parcel.iterchildren('{*}SpatialData'):
            result = self.get_parcel_conturs(contur)
        return result

    @log
    def convert_to_dxffile(self):
        if not self.parcels:
            return None
        dxffile = DxfFile(self)
        logging.info('converting %s to %s' %
                     (self.file_path, dxffile.output_file_path))
        dxffile.draw_conturs_and_save()
        return dxffile.output_file_path

    @log
    def pretty_rename(self):
        dirpath = os.path.dirname(self.file_path)
        cadastral_number_spaced = self.cadastral_number.replace(
            ':', ' ') + '.xml'
        pretty_basename = ' '.join(
            (self.xml_type, self.xml_subtype, cadastral_number_spaced))
        pretty_fullname = os.path.join(dirpath, pretty_basename)
        logging.info('renaming from %s to %s' %
                     (self.file_path, pretty_fullname))
        try:
            os.rename(self.file_path, pretty_fullname)
        except FileExistsError:
            os.remove(os.path.join(dirpath, pretty_basename))
            os.rename(self.file_path, pretty_fullname)
        return pretty_fullname


@log
def get_list_of_XmlFiles(xml_paths=None):
    """ Returns list of XmlFile class objects from xml_paths """

    # getting paths from settings (for console version mainly)
    if xml_paths is None:
        xml_paths = Settings().get_file_list('xml_folder', '.xml')
    logging.info('getting list of XmlFiles from %s' % xml_paths)

    res = []
    for file in xml_paths:
        xml_file = XmlFile(file)
        res.append(xml_file)
    return res


def remove_namespace(not_pretty_tag):
    return not_pretty_tag.split('}')[-1]
