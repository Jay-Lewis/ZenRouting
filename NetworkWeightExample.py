__author__ = 'Justin'

import networkx as nx
import math
from WeightFunction import zen_score

G1 = nx.DiGraph()

nodes = ['A','B','C','D']

G1.add_edge('A','B',weight = 0,traffic= 1, time = 5, distance = 1)
G1.add_edge('B','C',weight = 0,traffic= 1, time = 5, distance = 5)
G1.add_edge('D','C',weight = 0,traffic= 5, time = 1, distance = 1)
G1.add_edge('B','D',weight = 0,traffic= 5, time = 5, distance = 1)
G1.add_edge('A','D',weight = 0,traffic= 5, time = 1, distance = 5)

edges = G1.edges()

# Equal Weights

weights = [1,1,1]

for edge in edges:
    edge_dictionary = G1.get_edge_data(*edge)
    G1[edge[0]][edge[1]]['weight'] =  zen_score(weights,edge_dictionary)
    # print(edge)
    # print(G1[edge[0]][edge[1]]['weight'])

path = nx.shortest_path(G1,'A','C',weight = 'weight')

print(path)

# Weighted for traffic

weights = [1,100,100]

for edge in edges:
    edge_dictionary = G1.get_edge_data(*edge)
    G1[edge[0]][edge[1]]['weight'] =  zen_score(weights,edge_dictionary)
    # print(edge)
    # print(G1[edge[0]][edge[1]]['weight'])

path = nx.shortest_path(G1,'A','C',weight = 'weight')

print(path)

# Weighted for time

weights = [20,1,20]

for edge in edges:
    edge_dictionary = G1.get_edge_data(*edge)
    G1[edge[0]][edge[1]]['weight'] =  zen_score(weights,edge_dictionary)
    # print(G1[edge[0]][edge[1]]['weight'])

path = nx.shortest_path(G1,'A','C',weight = 'weight')

print(path)

# Weighted for distance

weights = [20,20,1]

for edge in edges:
    edge_dictionary = G1.get_edge_data(*edge)
    G1[edge[0]][edge[1]]['weight'] =  zen_score(weights,edge_dictionary)
    # print(G1[edge[0]][edge[1]]['weight'])

path = nx.shortest_path(G1,'A','C',weight = 'weight')

print(path)
