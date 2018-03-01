from os import path

import ezdxf


class DxfFile():
    """This class represents """

    def __init__(self, xmlfile):
        self.dwg = ezdxf.new('R2000')  # create R2000 drawing
        self.msp = self.dwg.modelspace()  # modelspace for dwg
        self.xmlfile = xmlfile
        self.settings = xmlfile.settings
        self.parcels = self.xmlfile.parcels
        self.reversed_parcels = reverse_dict_coords(self.parcels)
        self.output_file_path = path.join(
            self.settings.settings['dxf_folder_path'], self.xmlfile.basename_file_path.replace('.xml', '.dxf'))

    def draw_conturs_and_save(self):
        """ Draws iterables from dictionary to modelspace.
        CAUTION: Use with reversed coordinates"""
        for parcel_name, conturs in self.reversed_parcels.items():
            # Creating block with name ~ '21 02 000000'
            block_name = parcel_name.replace(':', ' ')
            dxf_block = self.dwg.blocks.new(name=block_name)
            # Getting random color for every block
            color = self.settings.get_next_color()
            # Adding parcels polylines
            for contur in conturs:
                dxf_block.add_lwpolyline(contur, dxfattribs={'color': color})
            # Adding text description
            text_attrib = get_text_attrib(conturs)
            if text_attrib:
                text_coords, text_height = text_attrib
                # print('Adding text at: %s with height %s ' %
                #       (text_coords, text_height))
                dxf_block.add_text(parcel_name,
                                   dxfattribs={'height': text_height,
                                               'color': color}).\
                    set_pos((text_coords), align='MIDDLE_CENTER')
            # Adding block to modelspace
            self.msp.add_blockref(block_name, insert=(
                0, 0), dxfattribs={'color': 2})
            # print name of cadastral block
            # saving
            self.dwg.saveas(self.output_file_path)
        print('%s drawed and saved' % (self.xmlfile.file_path))


def reverse_dict_coords(dic):
    """ Getting reverse coords, need for dxf file """
    reversed_result = {}
    for k, v in dic.items():
        reversed_result[k] = reverse_coords(v)
    return reversed_result


def reverse_coords(conturs):
    reversed_result = []
    for contur in conturs:
        reversed_result.append([])
        for (x, y) in contur:
            reversed_result[-1].append((y, x))
    return reversed_result


def get_text_attrib(conturs):
    """ Calculating some dxf text_attributes like coordinates and height,
    based on conturs coordinates """
    list_of_x = []
    list_of_y = []
    try:
        for contur in conturs:
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
