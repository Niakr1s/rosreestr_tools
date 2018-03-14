Rosreestr Tools предназначена для кадастровых инженеров.

 Данная программа может следующее:
1) Проверять вхождения dxf файлов (контуров объектов капитального строительства) в кадастровые участки (содержащиеся в xml выписках из Росреестра).
2) Переименовывать xml выписки из "абракадабры" в читаемые названия.
3) Конвертировать xml выписки из Росреестра в dxf формат.
4) Объединять получившиеся dxf файлы в один.

По умолчанию пути к входным и выходным файлам в подпапке files. Пути к файлам можно поменять в settings.json.
'dxf_folder_path': 'files\\dxf' - путь к директории с сконвертированными файлами
'xml_folder_path': 'files\\xml' - путь к директории с xml выписками
'my_dxf_file_path': 'files\\mydxf' -  путь к директории с проверяемыми dxf файлами
'check_txt_path': 'files\\txt' - путь к директории с результатами проверки вхождения dxf в xml
'formatted_txt_path': 'files\\txt\\formatted.txt' - путь к файлу с результами проверок, преобразованных в строку с разделителями ';'
'merged_dxf_path': 'files\\merged\\merged.dxf' - путь к объединенному dxf файлу
Чтоб вернуть настройки к исходным, просто удалите settings.json файл.


Установка и запуск:

1) установить python 3.6 или выше: https://www.python.org/downloads/

2) установить git: https://git-scm.com/downloads

3) в командной строке:
git clone https://github.com/Niakr1s/rosreestr_tools.git c:\rosreestr_tools

pip install ezdxf

pip install lxml

pip install progressbar

4) запуск через console.py