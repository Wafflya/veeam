import os

# Рекомендуется там, где это уместно, использовать стандартные библиотеки, а не выполнять реализацию общеизвестных
# алгоритмов с нуля. (c)
import xmltodict  # Пакет для парсинга хмл https://pypi.org/project/xmltodict/ , возможно, не совсем стандартный
import shutil  # Пакет для копирования файла

# Название файла, лежит в одной директории со скриптом
f = "cfg.xml"
with open('cfg.xml') as fd:
    doc = xmltodict.parse(fd.read())

for i in doc['config']['file']:
    # Кстати, стоит понимать, что скрипт не обработает название файла кириллицей
    try:
        shutil.copyfile(os.path.join(i['@source_path'], i['@file_name']),
                        os.path.join(i['@destination_path'], i['@file_name']))
    except PermissionError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
