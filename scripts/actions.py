import collections
from queue import Queue

import ezdxf
from progressbar import ProgressBar

from scripts import thread_handling
from scripts.my_dxf_file import get_list_of_MyDxfFiles, txts_to_formatted_string
from scripts.xml_file import get_list_of_XmlFiles


def check_mydxfs(settings, source='settings'):
    """ Checks all mydxf files from:
    if source='settings' - from settings.settings['my_dxf_file_path']
    if source='qt' - from list of xml_paths from QT window (TODO)
    in settings.settings['xml_folder_path']
    or if source='qt' - from QT window (TODO)"""
    list_of_MyDxfFiles = get_list_of_MyDxfFiles(settings, source)
    list_of_tasks = [(i.checks, (source,)) for i in list_of_MyDxfFiles]
    execute_list_of_tasks(list_of_tasks, 5)
    txts_to_formatted_string(settings)


def convert_xmlfiles_to_dxffiles(settings, source='settings'):
    """ Converts all xml files from:
    if source='settings' - from settings.settings['xml_folder_path']
    if source='qt' - from list of xml_paths from QT window (TODO)
    to settings.settings['dxf_folder_path'] """
    list_of_XmlFiles = get_list_of_XmlFiles(settings, source)
    list_of_tasks = [i.convert_to_dxffile for i in list_of_XmlFiles]
    execute_list_of_tasks(list_of_tasks, 1)


def merge_dxfs(settings, source='settings'):
    """ Merging all dxfs
    if source='settings' - from settings.settings['dxf_folder_path']
    if source='qt' - from list of xml_paths from QT window (TODO)
    into merged.dxf"""

    def import_and_save(dxf, target_dxf):
        try:
            source_dwg = ezdxf.readfile(dxf)
        except ezdxf.DXFStructureError:
            print('ФАЙЛ %s НЕ БЫЛ ДОБАВЛЕН!' % dxf)
            print('УДАЛИТЕ ЕГО И ПЕРЕКОНВЕРТИРУЙТЕ ЗАНОВО!')
            return
        importer = ezdxf.Importer(source_dwg, target_dxf)
        importer.import_all()
        target_dxf.save()

    dxf_list = settings.get_file_list('dxf_folder_path')
    # Creating clear dxf file
    dwg = ezdxf.new('R2000')
    merged_path = settings.settings['merged_dxf_path']
    dwg.saveas(merged_path)
    target_dxf = ezdxf.readfile(merged_path)
    list_of_tasks = [(import_and_save, (dxf, target_dxf)) for dxf in dxf_list]
    execute_list_of_tasks(list_of_tasks, 1)


def pretty_rename_xmls(settings, source='settings'):
    """ Renames list of dxfs to a pretty format """
    list_of_XmlFiles = get_list_of_XmlFiles(settings, source)
    list_of_tasks = [i.pretty_rename for i in list_of_XmlFiles]
    execute_list_of_tasks(list_of_tasks, 10, with_bar=False)
    # bar = ProgressBar(max_value=len(list_of_XmlFiles), redirect_stdout=True)
    # for n, XmlFile in enumerate(list_of_XmlFiles):
    #     bar.update(n)
    #     XmlFile.pretty_rename()
    print('Файлы были успешно переименованы!')


def update(d, u):
    """Updates dictionary"""
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def execute_list_of_tasks(list_of_tasks, max_threads=1, with_bar=True):
    """list_of_tasks can be list of functions or list of tuples (function, *args)"""
    queue = Queue()
    length = len(list_of_tasks)
    if with_bar:
        bar = ProgressBar(max_value=length)
        bar.update(0)
    else:
        bar = None
    threads = thread_handling.Threads(queue, max_threads, bar)
    for task in list_of_tasks:
        queue.put(task)
    queue.join()
    # stop workers
    for i in range(max_threads):
        queue.put(None)

# if __name__ == '__main__':
#     from settings import Settings
#
#     settings = Settings()
#     convert_xmlfiles_to_dxffiles(settings)
