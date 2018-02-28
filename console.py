"""
Simple usage:
settings = Settings() # creating settings instance
MyDxfFile(settings).check() # checking my file for intersects with parcels
convert_all_xml2dxf(settings) # converting all xmls
merge_dxfs(settings) # merging all dxfs
"""
from dxf_intersect import MyDxfFile
from settings import Settings
from xml2dxf import merge_dxfs
from xml_parser import convert_all_xml2dxf


def help_screen(settings):
    print("""
        Rosreestr tools created by Pavel Koshelev.
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
        """ % (settings.settings['my_dxf_file_path'],
               settings.settings['xml_folder_path'],
               settings.settings['xml_folder_path'],
               settings.settings['dxf_folder_path'],
               settings.settings['dxf_folder_path'],
               settings.settings['merged_dxf_path'],
               settings.json_settings_path))


def short_input():
    inp = input("""
        Введите 1, 2 или 3 для выбора, q для выхода,
        h - чтоб показать большое меню с подсказками.
        """)
    return inp


def menu():
    settings = Settings()
    help_screen(settings)
    while(True):
        inp = short_input()
        if inp == '1':
            MyDxfFile(settings).check()
        elif inp == '2':
            convert_all_xml2dxf(settings)
        elif inp == '3':
            merge_dxfs(settings)
        elif inp in ('q', 'Q'):
            break
        elif inp in ('h', 'H'):
            help_screen(settings)


if __name__ == '__main__':
    menu()
