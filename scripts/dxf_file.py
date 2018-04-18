from os import path

import ezdxf

from scripts import actions

COLORS = {'color_type': {'block': 7, 'parcel': 8, 'oks': 63}}


class DxfFile:
    """This class represents """

    def __init__(self, XmlFile):
        self.dwg = ezdxf.new('R2000')  # create R2000 drawing
        self.msp = self.dwg.modelspace()  # modelspace for dwg
        self.XmlFile = XmlFile
        self.settings = XmlFile.settings
        self.parcels = self.XmlFile.parcels
        self.parcels_add_reversed_coordinates()  # parcels now contain ['reversed_coordinates'] key
        if 'dxf_folder_path' not in self.settings.settings:
            self.output_file_path = self.XmlFile.file_path.replace('.xml', '.dxf')
        else:
            self.output_file_path = path.join(self.settings.settings['dxf_folder_path'],
                                              self.XmlFile.basename_file_path.replace('.xml', '.dxf'))

    def draw_conturs_and_save(self):
        """ Draws iterables from dictionary to modelspace.
        CAUTION: Use with reversed coordinates"""
        for cadastral_number, cadastral_attributes in self.parcels.items():
            # Creating block with name ~ '21 02 000000'
            block_name = cadastral_number.replace(':', ' ')
            dxf_block = self.dwg.blocks.new(name=block_name)
            # Different color and width for parcels, blocks and other
            attribs = get_attributes(cadastral_attributes)
            for contur in cadastral_attributes['reversed_coordinates']:
                dxf_block.add_lwpolyline(contur, dxfattribs=attribs)
            # Adding text description
            text_attrib = get_text_attrib(cadastral_attributes)
            if text_attrib:
                text_coords, text_height = text_attrib
                dxf_block.add_text(' '.join((cadastral_number, cadastral_attributes['type'])),
                                   dxfattribs={'height': text_height, 'color': attribs['color']}).set_pos(text_coords,
                                                                                                          align='MIDDLE_CENTER')
            # Adding block to modelspace
            self.msp.add_blockref(block_name, insert=(0, 0))
            # saving
            while True:
                try:
                    self.dwg.saveas(self.output_file_path)
                except PermissionError:
                    input(
                        '\nФайл %s\nиспользуется!\nЗакройте файл и нажмите любую клавишу + Enter' % self.output_file_path)
                else:
                    break

    def parcels_add_reversed_coordinates(self):
        """ Getting reverse coords, need for dxf file """
        for cadastral_number, attributes in self.parcels.items():
            actions.update(self.parcels,
                           {cadastral_number: {'reversed_coordinates': reverse_coords(attributes['coordinates'])}})


def reverse_coords(conturs):
    reversed_result = []
    for contur in conturs:
        reversed_result.append([])
        for (x, y) in contur:
            reversed_result[-1].append((y, x))
    return reversed_result


def get_text_attrib(cadastral_attributes):
    """ Calculating some dxf text_attributes like coordinates and height,
    based on conturs coordinates """
    list_of_x = []
    list_of_y = []
    try:
        for contur in cadastral_attributes['reversed_coordinates']:
            for x, y in contur:
                list_of_x.append(x)
                list_of_y.append(y)
        max_x, max_y = max(list_of_x), max(list_of_y)
        min_x, min_y = min(list_of_x), min(list_of_y)
        mid_x = (max_x - min_x) / 2 + min_x
        mid_y = (max_y - min_y) / 2 + min_y
    except ValueError:
        return None
    average_diff = ((max_x - mid_x) + (max_y - mid_y)) / 2
    height = min(average_diff / 5, 25)
    return (int(mid_x), int(mid_y)), height


def get_attributes(attributes):
    if attributes['type'] == 'CadastralBlock':
        return {'color': COLORS['color_type']['block'], 'const_width': 2}
    elif attributes['type'] == 'Parcel':
        return {'color': COLORS['color_type']['parcel']}
    else:
        return {'color': COLORS['color_type']['oks']}
