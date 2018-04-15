Rosreestr Tools предназначена для кадастровых инженеров.

Данная программа может следующее:
1) Проверять вхождения dxf файлов (контуров объектов капитального строительства) в кадастровые участки (содержащиеся в xml выписках из Росреестра).
2) Переименовывать xml выписки из "абракадабры" в читаемые названия.
3) Конвертировать xml выписки из Росреестра в dxf формат.
4) Объединять получившиеся dxf файлы в один.

По умолчанию пути к входным и выходным файлам на рабочем столе в папке 'rosreestr_tools_files'.

Установщики для системы Windows - https://github.com/Niakr1s/rosreestr_tools/releases

Ручная установка и запуск:
1) установить python 3.6 или выше: https://www.python.org/downloads/
2) установить git: https://git-scm.com/downloads
3) в командной строке (клонируем репозиторий, в конце указать любой удобный путь): git clone https://github.com/Niakr1s/rosreestr_tools.git c:\rosreestr_tools
далее переходим в c:\rosreestr_tools
4) в командной строке (устанавливаем зависимости): pip install -r requirements.txt
5) запуск через rosreestr_tools.py или rosreestr_tools_GUI.py