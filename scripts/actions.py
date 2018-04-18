import collections
from queue import Queue

import ezdxf
from progressbar import ProgressBar

import scripts.xml_file
from scripts import thread_handling
from scripts.my_dxf_file import get_list_of_MyDxfFiles, checks_to_formatted_string
from settings import Settings


def check_mydxfs(mydxf_paths=None, xml_paths=None):
    """ Checks all mydxf files from:
    If source is None - takes list from settings and converts in settings.settings['xml_folder_path']
    else you should pass list of file paths
    """
    if mydxf_paths is None:
        mydxf_paths = Settings().get_file_list('my_dxf_file_path', '.dxf')
    if xml_paths is None:
        xml_paths = Settings().get_file_list('xml_folder_path', '.xml')
    list_of_MyDxfFiles = get_list_of_MyDxfFiles(mydxf_paths)
    list_of_tasks = [(i.checks, (xml_paths,)) for i in list_of_MyDxfFiles]
    execute_list_of_tasks(list_of_tasks, 5)
    checks_to_formatted_string(formatted_txt=Settings().get_formatted_txt())


def convert_xmlfiles_to_dxffiles(source=None):
    """ Converts all xml files from:
    If source is None - takes list from settings and converts to settings.settings['dxf_folder_path']
    else you should pass list of file paths
    """
    list_of_XmlFiles = scripts.xml_file.get_list_of_XmlFiles(source)
    list_of_tasks = [i.convert_to_dxffile for i in list_of_XmlFiles]
    execute_list_of_tasks(list_of_tasks, 1)


def merge_dxfs(dxf_list=None, merged_path=None):
    """ Merging all dxfs
    If source is None - takes list from settings and converts into merged.dxf
    else you should pass list of file paths
    """
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

    if dxf_list is None:
        dxf_list = Settings().get_file_list('xml_folder_path', '.dxf')
    # Creating clear dxf file
    dwg = ezdxf.new('R2000')
    if merged_path is None:
        merged_path = Settings().get_merged_dxf()
    dwg.saveas(merged_path)
    target_dxf = ezdxf.readfile(merged_path)
    list_of_tasks = [(import_and_save, (dxf, target_dxf)) for dxf in dxf_list]
    execute_list_of_tasks(list_of_tasks, 1)


def pretty_rename_xmls(xml_paths=None):
    """
    If source is None - takes list from settings
    else you should pass list of file paths
    """
    list_of_XmlFiles = scripts.xml_file.get_list_of_XmlFiles(xml_paths)
    list_of_tasks = [i.pretty_rename for i in list_of_XmlFiles]
    execute_list_of_tasks(list_of_tasks, 10, with_bar=False)
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
    with thread_handling.Threads(queue, max_threads, bar):
        for task in list_of_tasks:
            queue.put(task)
        queue.join()
