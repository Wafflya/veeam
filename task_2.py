import hashlib
import os
from sys import argv


def hash_file(filename, enc_type):
    if enc_type == 'md5':
        h = hashlib.md5()
    elif enc_type == 'sha1':
        h = hashlib.sha1()
    elif enc_type == 'sha256':
        h = hashlib.sha256()
    else:
        return 'Unsupported encrypt type'

    with open(filename, 'rb') as f:
        # Подумал, что можно было читать по кускам из скольки-то байт, чтоб экономить память, но синтаксически так красивее
        h.update(f.read())

    return h.hexdigest()


try:
    input_file = argv[1]
    path_to_files = argv[2]
except IndexError as e:
    print('Не заданы параметры запуска')

with open(input_file, 'r') as f:
    a = f.readlines()
    for line in a:
        params = str(line).split(' ')
        if len(params) != 3:
            continue
        else:
            try:
                el_hash = hash_file(os.path.join(path_to_files, params[0]), params[1])
            except FileNotFoundError:
                print(params[0], 'NOT FOUND')
                continue
            if el_hash == params[2].strip():
                print(params[0], 'OK')
            else:
                print(params[0], 'FAIL')
