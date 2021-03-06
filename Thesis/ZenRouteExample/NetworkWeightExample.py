__author__ = 'Justin'

import networkx as nx
import matplotlib.pyplot as plt
from WeightFunction import weightfunction

G1 = nx.DiGraph()

nodes = ['A','B','C','D']
keys = ['zenness','time','distance']

G1.add_edge('A','B',weight = 0,zenness= 5, time = 8, distance = 2)
G1.add_edge('B','C',weight = 0,zenness= 2, time = 6, distance = 2)
G1.add_edge('D','C',weight = 0,zenness= 4, time = 6, distance = 6)
G1.add_edge('D','B',weight = 0,zenness= 1, time = 5, distance = 2)
G1.add_edge('A','D',weight = 0,zenness= 2, time = 4, distance = 2)

edges = G1.edges()

# GraphMl format to export the network to cytoscape
nx.write_graphml(G1, "TrafficTest.graphml")

# Draw network
nx.draw_networkx(G1)
plt.draw()
plt.show()

# Equal Weights

weights = [1,1,1]

for edge in edges:
    edge_dictionary = G1.get_edge_data(*edge)
    G1[edge[0]][edge[1]]['weight'] =  weightfunction(weights,edge_dictionary,keys)
    # print(edge)
    #print(G1[edge[0]][edge[1]]['weight'])

path = nx.shortest_path(G1,'A','C',weight = 'weight')

print('Equal Weights',path)

# Weighted for traffic

weights = [5,1,1]

for edge in edges:
    edge_dictionary = G1.get_edge_data(*edge)
    G1[edge[0]][edge[1]]['weight'] =  weightfunction(weights,edge_dictionary,keys)
    # print(edge)
    #print(G1[edge[0]][edge[1]]['weight'])

path = nx.shortest_path(G1,'A','C',weight = 'weight')

print('Weighted for Traffic',path)

# Weighted for time

weights = [1,5,1]

for edge in edges:
    edge_dictionary = G1.get_edge_data(*edge)
    G1[edge[0]][edge[1]]['weight'] =  weightfunction(weights,edge_dictionary,keys)
    #print(G1[edge[0]][edge[1]]['weight'])

path = nx.shortest_path(G1,'A','C',weight = 'weight')

print('Weighted for Time',path)

# Weighted for distance

weights = [1,1,5]

for edge in edges:
    edge_dictionary = G1.get_edge_data(*edge)
    G1[edge[0]][edge[1]]['weight'] =  weightfunction(weights,edge_dictionary,keys)
    #print(G1[edge[0]][edge[1]]['weight'])

path = nx.shortest_path(G1,'A','C',weight = 'weight')

print('Weighted for Distance',path)
