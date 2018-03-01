import actions
from settings import Settings


def help_screen(settings):
    print("""
Rosreestr tools created by Pavel Koshelev.
%s - для исходных xml файлов
%s - для сконвертированных dxf
%s - для ваших dxf, которые нужно проверить
%s - для соединенного dxf
%s - конфиг файл
Введите цифру:
1 - Чтобы проверить вхождение dxf файла в xml
2 - Чтобы сконвертировать xml
3 - Чтобы соединить несколько dxf (долго)
4 - Переименовать xml в приятные названия
Если что-то пошло не так, удалите конфиг файл.
""" % (
    settings.settings['xml_folder_path'], settings.settings['dxf_folder_path'], settings.settings['my_dxf_file_path'],
    settings.settings['merged_dxf_path'], settings.json_settings_path))


def short_input():
    inp = input("""
        Введите 1, 2, 3 или 4 для выбора, q для выхода,
        h - чтоб показать большое меню с подсказками.
        """)
    return inp


def menu():
    settings = Settings()
    help_screen(settings)
    while True:
        inp = short_input()
        if inp == '1':
            actions.check_mydxfs(settings)
        elif inp == '2':
            actions.convert_xmlfiles_to_dxffiles(settings)
        elif inp == '3':
            actions.merge_dxfs(settings)
        elif inp == '4':
            actions.pretty_rename_dxfs(settings)
        elif inp in ('q', 'Q'):
            break
        elif inp in ('h', 'H'):
            help_screen(settings)


if __name__ == '__main__':
    menu()
