import os

top_data = {} # словарь с данными топологии
_topology_path = "" # переменная с путем до файла

def top_parser():
    print("Введите путь до файла с топологией в полном виде") 
    _topology_path = input() # ввод с клавиатуры путя до файла
    
    with open(os.path.abspath(_topology_path), 'r', encoding='cp1252') as file: # парсим данные с txt в словарик
        for line in file:
            top_data[line.split(":")[0].strip()] = line.split(":")[1].strip()

    return(top_data)