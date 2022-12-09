import os
import re


class Router(object): # класс для внесения информации о маршрутизаторах
    def __init__(self, _router_ip, _con_router_ip, _con_nodes):
        self.ip = _router_ip
        self.con_routers = _con_router_ip
        self.con_nodes = _con_nodes

    def ac_nodes(self):
        access = {} # словарь с значениями: 
                    #IP-адрес:внешний доступ(1-есть, 0 - нету)
        for _node in self.con_nodes:
            if _node[0] == "+":
                access.update({re.sub("\+", "", _node) : "1"})
            elif _node[0] == "-":
                access.update({re.sub("\-", "", _node) : "0"})
        return(access)

routers_list = [] # список для обьектов класса

def con_parser():
    print("Введите путь до файла со связями в полном виде")
    _con_path = input()

    
    _nodes = [] # список для внесения данных из файла
    
    with open(os.path.abspath(_con_path), 'r', encoding='cp1252') as file:
        
        for line in file:
            _nodes.append(re.sub("\n", "", line)) 
            # в эту переменную последовательно записываем строки, 
            # получая готовый обьект для работы

    for _node in _nodes: # этот блок нужен для создания объектов класса
        _router_ip = "" # т.е он парсит данные из кучи
        _con_router_ip = [] # и создает объекты класса
        _con_nodes = [] # которые в свою очередь составляют список
        
        if _node[0] != ">" and _node[0] != "+" and _node[0] != "-":
            _router_ip = re.sub(":", "", _node)
            i = 1
            while _nodes.index(_node) + i < len(
                _nodes) and _nodes[_nodes.index(_node) + i][-1] != ":":
                if _nodes[_nodes.index(_node) + i][0] == ">":
                    _con_router_ip.append(re.sub(">", "",
                    _nodes[_nodes.index(_node) + i]))
                    i += 1
                elif _nodes[_nodes.index(_node) + i][0] == "+" or "-":    
                    _con_nodes.append(_nodes[_nodes.index(_node) + i])
                    i += 1
                
                

            routers_list.append(Router(_router_ip, _con_router_ip, _con_nodes))

    return(routers_list)


#for i in range(len(routers)):
#    print (routers[i].ac_nodes())

def transition_list(): # некое подобие матрицы переходов, но словарь
    routers = con_parser()
    trans_list = []
    for i in range(len(routers)):
        trans_list.append(routers[i].ac_nodes())
    return(trans_list)

def def_edges():
    routers = routers_list
    def_edges = []
    for _router in routers:
        for _con_router in _router.con_routers:
            def_edges.append([_router.ip , _con_router])
        for _con_node in _router.con_nodes:
            def_edges.append([_router.ip , re.sub("\+|\-","",_con_node)])
            for _con_between_nodes in _router.con_nodes:
                if _con_node != _con_between_nodes:
                    def_edges.append([re.sub("\+|\-","",_con_node), 
                    re.sub("\+|\-","",_con_between_nodes)])
    
    return(def_edges)
    


def attack_edges(vuln_node, start_top):
    routers = routers_list
    temp_attack = []
    attack_route = []

    for _router in routers:
        for _con_node in _router.con_nodes:

            if vuln_node == re.sub("\+|\-","",_con_node):
                for _con_node in _router.con_nodes:
                    if start_top == re.sub("\+|\-","",_con_node):
                        temp_attack.append([start_top, vuln_node])
                        break

                    elif vuln_node == re.sub("\+|\-","",_con_node):
                        start_router_ip = ""

                        temp_attack.append([vuln_node, _router.ip])
                        
                        for _con_routers_to_vuln in _router.con_routers:
                            for _start_router in routers:
                                for _start_top in _start_router.con_nodes:
                                    if re.sub("\+|\-","",_start_top) == start_top:
                                        str_router = _start_router.ip
                                        if _con_routers_to_vuln == str_router:
                                            temp_attack.append([_router.ip, str_router])
                                            temp_attack.append([str_router, start_top])

                        
    return temp_attack 

def def_edges_for_attack(temp_attack):
    temp_def_edges = def_edges()
    for item in temp_def_edges:
        for trace in temp_attack:
            if item == trace:
                temp_def_edges.remove(item)

      




