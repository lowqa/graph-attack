import ipaddress
import logging
import os
import networkx as nx
import matplotlib.pyplot as plt

from data_parser import top_parser, vuln_parser, transition_list, def_edges,\
attack_edges, def_edges_for_attack

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESULT_DIR = ROOT_DIR + '/results'

logger = logging.getLogger(__name__)
_start_top = "" # начальная вершина

top_data = top_parser() # хранит в себе топологию
level_vuln = vuln_parser() # хранит в себе уровень прав на узалх



start_top = input("Введите начальную вершину в виде IP-адреса \n")

try:
    # данный блок служит для валидности IP-адреса стартовой вершины
    ipaddress.ip_address(start_top)
    _num_of_occur = 0
    for node in top_data:
        if node == start_top:
            _num_of_occur += 1
    if _num_of_occur == 0:
        raise ValueError("Такого IP-адреса не существует в топологии")

except ValueError as error:
    logger.error(error)
    raise

def graph_bypass(start_top): # функция обхода графа, предоставляющая
# трассы аттак в виде словаря
    attack_routes = []
    vuln_nodes = []
    
    
    _start_top_access = level_vuln.get(start_top)
    
    if _start_top_access >= 3:
            
        for nodes in transition_list():
            for key, value in nodes.items():
                if key != start_top and value == "1" and level_vuln.get(key) >= 3:
                    vuln_nodes.append(key)
    else:
        print("Граф атаки пуст, так как на указанном узле нет уязвимости с нужным уровнем доступа")
    
    #print(vuln_nodes)

    result = Ilustrator(attack_edges= "", def_edges=def_edges(), figsize=len(top_data))
    result.create_default_graph()

    if len(vuln_nodes) > 0:
        for i in range(len(vuln_nodes)):
            temp_attack = attack_edges(vuln_nodes[i], start_top)
            
            #temp_def = def_edges_for_attack(temp_attack)
            temp_def = def_edges()
            temp_res = Ilustrator(def_edges=temp_def, attack_edges=temp_attack, figsize = len(top_data))
            temp_res.create_graph_attack_graph(i=i)
        print("Графы атак успешно построены, результаты в папке \"results\"")

    

class Ilustrator():
    def_edge_color = 'black'
    attack_edge_color = 'red'
    width = 1
    node_edge_color = 'black'
    node_color = 'grey'
    connectionstyle = 'arc3, rad = 0.03'
    node_size = 5000
    font_size = 8
    font_color = 'black'

    def __init__(self, attack_edges, def_edges, figsize):
        self.attack_edges = attack_edges
        self.def_edges = def_edges
        self.figsize = figsize * 2

    def create_default_graph(self):
        G = nx.Graph()
        G.add_edges_from(self.def_edges, color=self.def_edge_color, weight=self.width, edgecolor='black')
        edges = G.edges()
        colors = [G[u][v]['color'] for u, v in edges]
        weights = [G[u][v]['weight'] for u, v in edges]
        plt.figure(figsize=(self.figsize, self.figsize - 2))
        labeldict = {}
        for node in G.nodes():
            labeldict[node] = node
        pos = nx.planar_layout(G)
        g_nodes = nx.draw_networkx_nodes(G, pos=pos, node_size=self.node_size, node_color=self.node_color)
        nx.draw_networkx_edges(G, pos=pos, edgelist=edges, edge_color=colors, node_size=self.node_size, width=weights,
                               connectionstyle=self.connectionstyle)
        g_nodes.set_edgecolor(self.node_edge_color)
        nx.draw_networkx_labels(G, pos=pos, font_size=self.font_size, font_color=self.font_color, labels=labeldict)
        plt.axis("off")
        plt.savefig(f"{RESULT_DIR}/def_graph.png", format="PNG")

    def create_graph_attack_graph(self, i):
        G = nx.Graph()
        G.add_edges_from(self.def_edges, color=self.def_edge_color, weight=self.width)
        G.add_edges_from(self.attack_edges, color=self.attack_edge_color, weight=self.width)
        edges = G.edges()
        colors = [G[u][v]['color'] for u, v in edges]
        weights = [G[u][v]['weight'] for u, v in edges]
        plt.figure(figsize=(self.figsize, self.figsize - 2))
        labeldict = {}
        for node in G.nodes():
            labeldict[node] = node
        pos = nx.planar_layout(G)
        g_nodes = nx.draw_networkx_nodes(G, pos=pos, node_size=self.node_size, node_color=self.node_color)
        nx.draw_networkx_edges(G, pos=pos, edgelist=edges, edge_color=colors, node_size=self.node_size, width=weights,
                            connectionstyle=self.connectionstyle)
        g_nodes.set_edgecolor(self.node_edge_color)
        nx.draw_networkx_labels(G, pos=pos, font_size=self.font_size, font_color=self.font_color, labels=labeldict)
        plt.axis("off")
        plt.savefig(f"{RESULT_DIR}/Graph{i}.png", format="PNG")

    
    

graph_bypass(start_top)


    
