from queue import Queue

import ezdxf
from progressbar import ProgressBar

import scripts.xml_file
from scripts import thread_handling
from scripts.my_dxf_file import get_list_of_MyDxfFiles, checks_to_formatted_string
from scripts.settings import Settings


def check_mydxfs(mydxf_paths=None, xml_paths=None):
    """ Checks all mydxf files from mydxf_paths in xml files from xml_paths """

    # getting paths from settings (for console version mainly)
    if mydxf_paths is None:
        mydxf_paths = Settings().get_file_list('mydxf_folder', '.dxf')
    if xml_paths is None:
        xml_paths = Settings().get_file_list('xml_folder', '.xml')

    list_of_MyDxfFiles = get_list_of_MyDxfFiles(mydxf_paths)
    list_of_tasks = [(i.checks, (xml_paths,)) for i in list_of_MyDxfFiles]
    execute_list_of_tasks(list_of_tasks, 5)
    checks_to_formatted_string(formatted_txt_path=Settings().formatted_txt)


def convert_xmlfiles_to_dxffiles(xml_paths=None):
    """ Converts all xml files from xml_paths to same folder """
    list_of_XmlFiles = scripts.xml_file.get_list_of_XmlFiles(xml_paths)
    list_of_tasks = [i.convert_to_dxffile for i in list_of_XmlFiles]
    execute_list_of_tasks(list_of_tasks, 1)


def merge_dxfs(dxf_paths=None, merged_path=None):
    """ Merging all dxfs from dxf_list to merged_path
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

    # getting paths from settings (for console version mainly)
    if dxf_paths is None:
        dxf_paths = Settings().get_file_list('xml_folder', '.dxf')
    if merged_path is None:
        merged_path = Settings().merged_dxf

    # Creating clear dxf file
    dwg = ezdxf.new('R2000')
    dwg.saveas(merged_path)

    target_dxf = ezdxf.readfile(merged_path)
    list_of_tasks = [(import_and_save, (dxf, target_dxf)) for dxf in dxf_paths]
    execute_list_of_tasks(list_of_tasks, 1)


def pretty_rename_xmls(xml_paths=None):
    list_of_XmlFiles = scripts.xml_file.get_list_of_XmlFiles(xml_paths)
    list_of_tasks = [i.pretty_rename for i in list_of_XmlFiles]
    execute_list_of_tasks(list_of_tasks, 10, with_bar=False)
    print('Файлы были успешно переименованы!')


# def update(d, u):
#     """Updates dictionary"""
#     for k, v in u.items():
#         if isinstance(v, collections.Mapping):
#             d[k] = update(d.get(k, {}), v)
#         else:
#             d[k] = v
#     return d


def update(d, u):
    """Updates dictionary"""
    for k, v in u.items():
        if isinstance(v, dict):
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
