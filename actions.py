import collections

import ezdxf
from progressbar import ProgressBar, streams

from my_dxf_file import get_list_of_MyDxfFiles, txts_to_formatted_string
from xml_file import get_list_of_XmlFiles


def check_mydxfs(settings, source='settings'):
    """ Checks all mydxf files from:
    if source='settings' - from settings.settings['my_dxf_file_path']
    if source='qt' - from list of xml_paths from QT window (TODO)
    in settings.settings['xml_folder_path']
    or if source='qt' - from QT window (TODO)"""
    list_of_MyDxfFiles = get_list_of_MyDxfFiles(settings, source)
    bar = ProgressBar(max_value=len(list_of_MyDxfFiles), redirect_stdout=True)
    for n, MyDxfFile in enumerate(list_of_MyDxfFiles):
        bar.update(n)
        MyDxfFile.checks(source)
    txts_to_formatted_string(settings)


def convert_xmlfiles_to_dxffiles(settings, source='settings'):
    """ Converts all xml files from:
    if source='settings' - from settings.settings['xml_folder_path']
    if source='qt' - from list of xml_paths from QT window (TODO)
    to settings.settings['dxf_folder_path'] """
    list_of_XmlFiles = get_list_of_XmlFiles(settings, source)
    bar = ProgressBar(max_value=len(list_of_XmlFiles), redirect_stdout=True)
    for n, XmlFile in enumerate(list_of_XmlFiles):
        bar.update(n)
        XmlFile.convert_to_dxffile()


def merge_dxfs(settings, source='settings'):
    """ Merging all dxfs
    if source='settings' - from settings.settings['dxf_folder_path']
    if source='qt' - from list of xml_paths from QT window (TODO)
    into merged.dxf"""
    dxf_list = settings.get_file_list('dxf_folder_path')
    # Creating clear dxf file
    dwg = ezdxf.new('R2000')
    merged_path = settings.settings['merged_dxf_path']
    dwg.saveas(merged_path)
    target_dxf = ezdxf.readfile(merged_path)
    # Progress Bar
    streams.flush()
    bar = ProgressBar(max_value=len(dxf_list), redirect_stdout=True)
    # Merging
    for n, dxf in enumerate(dxf_list):
        bar.update(n)
        try:
            source_dwg = ezdxf.readfile(dxf)
        except ezdxf.DXFStructureError:
            print('ФАЙЛ %s НЕ БЫЛ ДОБАВЛЕН!' % dxf)
            print('УДАЛИТЕ ЕГО И ПЕРЕКОНВЕРТИРУЙТЕ ЗАНОВО!')
        importer = ezdxf.Importer(source_dwg, target_dxf)
        importer.import_all()
        target_dxf.save()


def pretty_rename_xmls(settings, source='settings'):
    """ Renames list of dxfs to a pretty format """
    list_of_XmlFiles = get_list_of_XmlFiles(settings, source)
    bar = ProgressBar(max_value=len(list_of_XmlFiles), redirect_stdout=True)
    for n, XmlFile in enumerate(list_of_XmlFiles):
        bar.update(n)
        XmlFile.pretty_rename()
    print('Файлы были успешно переименованы!')


if __name__ == '__main__':
    from settings import Settings
    settings = Settings()
    txts_to_formatted_string(settings)


def update(d, u):
    """Updates dictionary"""
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d
