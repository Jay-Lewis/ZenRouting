__author__ = 'Justin'


import random
import networkx as nx
from k_shortest_paths import k_shortest_paths

Graph = nx.DiGraph()

nodes = ['A','B','C','D','E','F','G']

Graph.add_nodes_from(nodes)

Graph.add_edge('A','B',weight = 1)
Graph.add_edge('A','E',weight = 1)
Graph.add_edge('A','F',weight = 5)
Graph.add_edge('B','C',weight = 1)
Graph.add_edge('B','E',weight = 2)
Graph.add_edge('C','D',weight = 1)
Graph.add_edge('F','G',weight = 6)
Graph.add_edge('G','D',weight = 7)
Graph.add_edge('E','D',weight = 3)


paths = k_shortest_paths(Graph,'A','D',2)
print('Path a Length',paths[0][0])
print('Path a',paths[1][0])
print('Path b Length',paths[0][1])
print('Path b',paths[1][1])
