import os
import re

from data_parser import top_data

vuln_data = {} # словарь с данными об уязвимостях
top_vulnab = {} # словарь с данными об уязвимостях на узлах, где значение
# 4 - есть хоть одна уязвимость с уровнем root, 3 - с уровнем user
# 2 - c уровнем dos, 1 - с уровнем other, 0 - уязвимостей нет

def vuln_parser():
    print("Введите путь до файла с уязвимостями в полном виде") 
    _vulnab_path = input() # ввод с клавиатуры путя до файла
    _top_data = top_data
    with open(os.path.abspath(_vulnab_path), 'r', encoding='cp1252') as file: 
        # парсим данные с txt в словарик
        for line in file:
            vuln_data[line.split(":")[0].rstrip()] = line.split(":")[1].rstrip()

    for top_key, top_value in _top_data.items():
        top_value = top_value.split(",")

        for item in top_value:
            for vuln, access in vuln_data.items():
                if item.replace(" ", "") == vuln:
                    if access == 'root':
                        top_vulnab[top_key] = 4
                    elif access == "user" and top_vulnab.get(top_key, 0) < 4:
                        top_vulnab.update({top_key : 3})
                    elif access == "dos" and top_vulnab.get(top_key, 0) < 3:
                        top_vulnab.update({top_key : 2})
                    elif access == "other" and top_vulnab.get(top_key, 0) < 2:
                        top_vulnab.update({top_key : 1})
                elif item == "":
                    top_vulnab.update({top_key : 0})


    return(top_vulnab)

