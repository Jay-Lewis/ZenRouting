

import networkx as nx
import os
from DisplayNetwork import networkdisplay
import matplotlib.pyplot as plt
from numpy.random import rand

# Plot Simple Network Graph for Example

G1 = nx.DiGraph()

nodes = ['A','B','C','D']
for node in nodes:
    G1.add_node(node)

keys = ['zenness','time','distance']
G1.add_edge('A','B',weight = 1,zenness= 5, time = 8, distance = 2)
G1.add_edge('B','C',weight = 2,zenness= 2, time = 6, distance = 2)
G1.add_edge('D','C',weight = 3,zenness= 4, time = 6, distance = 6)
G1.add_edge('D','B',weight = 4,zenness= 1, time = 5, distance = 2)
G1.add_edge('A','D',weight = 5,zenness= 2, time = 4, distance = 2)

positions = nx.spring_layout(G1)
print(positions)
nx.draw_networkx(G1,pos = positions,node_color = '#a6a6a6',edge_color = '#333333',node_size = 500,font_size = 14)
edge_labels = nx.get_edge_attributes(G1,'weight')
nx.draw_networkx_edge_labels(G1,pos = positions,edge_labels = edge_labels,font_size = 14)
plt.show()


# Draw Example of Node and Edge

G1 = nx.DiGraph()

nodes = ['A','B']
for node in nodes:
    G1.add_node(node)

G1.add_edge('A','B',weight = 1)

positions = {'A':[0,0],'B':[1,0]}
nx.draw_networkx(G1,pos = positions,node_color = '#a6a6a6',edge_color = '#333333',node_size = 500,font_size = 14)
edge_labels = nx.get_edge_attributes(G1,'weight')
nx.draw_networkx_edge_labels(G1,pos = positions,edge_labels = edge_labels,font_size = 14)
plt.show()

G1 = nx.DiGraph()

nodes = ['A']
for node in nodes:
    G1.add_node(node)

positions = nx.spring_layout(G1)
nx.draw_networkx(G1,pos = positions,node_color = '#a6a6a6',edge_color = '#333333',node_size = 500,font_size = 14)
edge_labels = nx.get_edge_attributes(G1,'weight')
nx.draw_networkx_edge_labels(G1,pos = positions,edge_labels = edge_labels,font_size = 14)
plt.show()


# # Load Network
# cwd = os.getcwd()
# filename = "OSMNetworkReducedSet.gexf"
# filepath = os.path.abspath(os.path.join(cwd, '..','..', 'Project Data','Networks',filename))
# fh=open(filepath,'rb')
# G = nx.read_gexf(fh)
# fh.close
#
# nx.draw_networkx(G)
# plt.show()