import os

from settings import Settings

from scripts import actions


def help_screen(settings):
    print("""
Rosreestr tools created by Pavel Koshelev.

%s - исходные xml файлы, сконвертированные dxf файлы хранятся там же
%s - ваши dxf, которые нужно проверить на пересечения в xml, результаты проверок хранятся там же

%s - объединенный dxf
%s - общая строка проверок dxf с xml
""" % (settings.settings['paths']['xml_folder'], settings.settings['paths']['mydxf_folder'], settings.get_merged_dxf(),
       settings.get_formatted_txt()))


def short_input():
    # inp = input("""
    #     Введите 1, 2, 3 или 4 для выбора, q для выхода,
    #     h - чтоб показать большое меню с подсказками.
    #     """)
    print("""\n\n
    Введите цифру:
1 - Чтобы проверить вхождение dxf файла в xml
2 - Переименовать xml в приятные названия
3 - Чтобы сконвертировать xml
4 - Чтобы соединить несколько dxf (долго)
""")
    print('\n')
    print(''.center(79, '*'))
    print('Введите 1, 2, 3, 4 для выбора, q для выхода, h для помощи'.center(79, '*'))
    inp = input(''.center(78, '*'))
    return inp


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n' * 25)


def menu():
    cls()
    settings = Settings()

    help_screen(settings)

    while True:
        inp = short_input()
        settings.check_paths()
        if inp == '1':
            cls()
            actions.check_mydxfs()
        elif inp == '2':
            cls()
            actions.pretty_rename_xmls()
        elif inp == '3':
            cls()
            actions.convert_xmlfiles_to_dxffiles()
        elif inp == '4':
            cls()
            actions.merge_dxfs()
        elif inp in ('q', 'Q'):
            cls()
            break
        elif inp in ('h', 'H'):
            cls()
            help_screen(settings)


if __name__ == '__main__':
    menu()
