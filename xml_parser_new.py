from lxml import etree
from pprint import pprint
""" Some functions for __init__() | Start """


def get_parcels(root):
    """ Here we are getting dict of parcels with coordinates """
    result = {}
    for parcel in root.iter('{*}Parcel'):
        cadastral_number = parcel.attrib['CadastralNumber']
        print('parcel %s' % (cadastral_number))
        conturs = get_parcel_conturs(parcel)
        result[cadastral_number] = conturs
    return result


def get_parcel_conturs(parcel):
    """ Subfunction for get_parcels function,
    returns list of conturs with tuple of coords """
    result = []
    for contur in parcel.iter('{*}SpatialElement'):
        print('new_contur')
        result.append([])
        for point in contur.iter('{*}Ordinate'):
            print(point.attrib)
            x = float(point.attrib['X'])
            y = float(point.attrib['Y'])
            result[-1].append((x, y))
    return result


def get_blocks(root):
    """ Here we are getting dict of blocks with coordinates """
    result = {}
    for block in root.iter('{*}CadastralBlock'):
        cadastral_number = block.attrib['CadastralNumber']
        print('block %s' % (cadastral_number))
        conturs = get_block_conturs(block)
        result[cadastral_number] = conturs
    return result


def get_block_conturs(parcel):
    """ Subfunction for get_blocks function
    returns list of conturs with tuple of coords """
    for contur in parcel.iterchildren('{*}SpatialData'):
        print('new_contur')
        result = get_parcel_conturs(contur)
    return result


""" Some functions for __init__() | End """


class RRxml():
    """ Class for a single rosreestr xml file """

    def __init__(self, file_path):
        self.file_path = file_path
        self.tree = etree.parse(file_path)
        self.root = self.tree.getroot()
        self.blocks = get_blocks(self.root)
        self.parcels = get_parcels(self.root)


if __name__ == '__main__':
    file_path = '21 02 010103.xml'
    xml = RRxml(file_path)
    pprint(xml.blocks)
    pprint(xml.parcels)
