import ezdxf

from exceptions import WrongArguments
from my_dxf_file import get_list_of_mydxffiles
from xml_file import get_list_of_xmlfiles


def check_mydxfs(settings, source='settings'):
    """ Checks all mydxf files from:
    if source='settings' - from settings.settings['my_dxf_file_path']
    if source='qt' - from list of xml_paths from QT window (TODO)
    in settings.settings['xml_folder_path']
    or if source='qt' - from QT window (TODO)"""
    for xml_file in get_list_of_mydxffiles(settings, source):
        xml_file.check(source)


def convert_xmlfiles_to_dxffiles(settings, source='settings'):
    """ Converts all xml files from:
    if source='settings' - from settings.settings['xml_folder_path']
    if source='qt' - from list of xml_paths from QT window (TODO)
    to settings.settings['dxf_folder_path'] """
    for xml_file in get_list_of_xmlfiles(settings, source):
        xml_file.convert_to_dxffile()


def merge_dxfs(settings, source='settings'):
    """ Merging all dxfs
    if source='settings' - from settings.settings['xml_folder_path']
    if source='qt' - from list of xml_paths from QT window (TODO)
    into merged.dxf"""
    if source == 'settings':
        dxf_list = settings.get_dxf_list()
        # TODO get file_paths from qt window
    else:
        raise WrongArguments
    # Creating clear dxf file
    dwg = ezdxf.new('R2000')
    merged_path = settings.settings['merged_dxf_path']
    dwg.saveas(merged_path)
    target_dxf = ezdxf.readfile(merged_path)
    # Merging
    for dxf in dxf_list:
        source_dwg = ezdxf.readfile(dxf)
        importer = ezdxf.Importer(source_dwg, target_dxf)
        importer.import_all()
        print('%s added' % (dxf))
    target_dxf.save()