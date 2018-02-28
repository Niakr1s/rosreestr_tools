import ezdxf

from xml_file import XmlFile


def convert_xmlfiles_to_dxffiles(settings):
    """ Converts all xml files from settings.settings['xml_folder_path']
    to settings.settings['dxf_folder_path'] """
    for xml_file in get_list_of_xmlfiles(settings):
        xml_file.convert_to_dxffile()


def merge_dxfs(settings):
    """ Merging all dxfs from settings.settings['dxf_folder_path']
    into merged.dxf"""
    dxf_list = settings.get_dxf_list()
    # Creating clear dxf file
    dwg = ezdxf.new('R2000')
    merged_path = settings.settings['merged_dxf_path']
    dwg.saveas(merged_path)
    target_dwg = ezdxf.readfile(merged_path)
    # Merging
    for dxf in dxf_list:
        source_dwg = ezdxf.readfile(dxf)
        importer = ezdxf.Importer(source_dwg, target_dwg)
        importer.import_all()
        print('%s added' % (dxf))
    target_dwg.save()


def get_list_of_xmlfiles(settings):
    """ Returns list of XmlFile class objects """
    res = []
    for file in settings.get_xml_list():
        xml_file = XmlFile(file, settings)
        res.append(xml_file)
    return res
