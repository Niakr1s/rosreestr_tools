from lxml import etree

file_path = '21 02 010103.xml'

tree = etree.parse(file_path)
root = tree.getroot()


def get_block_conturs(parcel):
    for contur in parcel.iterchildren('{*}SpatialData'):
        print('new_contur')
        get_parcel_conturs(contur)


def get_parcel_conturs(parcel):
    for contur in parcel.iter('{*}SpatialElement'):
        print('new_contur')
        for point in contur.iter('{*}Ordinate'):
            print(point.attrib)


for block in root.iter('{*}CadastralBlock'):
    print('block %s' % (block.attrib['CadastralNumber']))
    print(block.attrib)
    get_block_conturs(block)


for parcel in root.iter('{*}Parcel'):
    print('parcel %s' % (parcel.attrib['CadastralNumber']))
    get_parcel_conturs(parcel)
