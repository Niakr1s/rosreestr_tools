from settings import Settings
from xml2dxf import merge_dxfs
from dxf_intersect import MyDxfFile
from xml_parser import convert_all_xml2dxf

"""
Simple usage:
settings = Settings() # creating settings instance
MyDxfFile(settings).check() # checking my file for intersects with parcels
convert_all_xml2dxf(settings) # converting all xmls
merge_dxfs(settings) # merging all dxfs
"""


def get_answer(settings):
    inp = input("""
        Введите цифру:
        1 - Чтобы проверить вхождение dxf файла в КПТшки
        переместите его в
        %s,
        а нужные КПТ - в каталог
        %s.
        2 - Чтобы сконвертировать КПТшки
        поместите нужные КПТ в каталог
        %s,
        сконвертированные файлы появятся в каталоге
        %s.
        3 - Чтобы соединить несколько dxf,
        поместите их в каталог
        %s.
        Выходной dxf появится в каталоге
        %s.
        Внимание! Эта операция может занять длительное время.
        P.S. Пути можно поменять в конфиг файле
        %s.
        Если что-то пошло не так, удалите конфиг файл.
        Введите 1, 2 или 3 для выбора, или любой символ для выхода.
        """ % (settings.settings['my_dxf_file_path'],
               settings.settings['xml_folder_path'],
               settings.settings['xml_folder_path'],
               settings.settings['dxf_folder_path'],
               settings.settings['dxf_folder_path'],
               settings.settings['merged_dxf_path'],
               settings.json_settings_path))
    return inp


def menu():
    settings = Settings()
    inp = get_answer(settings)
    if inp == '1':
        MyDxfFile(settings).check()
    elif inp == '2':
        convert_all_xml2dxf(settings)
    elif inp == '3':
        merge_dxfs(settings)
    else:
        print('Ничего не было выбрано')
    input("""Created by Pavel Koshelev. Press any key to exit.
        """)


if __name__ == '__main__':
    menu()
