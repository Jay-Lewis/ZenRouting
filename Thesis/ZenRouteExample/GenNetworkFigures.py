

import networkx as nx
import math
import matplotlib.pyplot as plt
from numpy.random import rand

# Plot Simple Network Graph for Example

G1 = nx.DiGraph()

G1.add_edge('A','B',weight = 0,zenness= 5, time = 8, distance = 2)
G1.add_edge('B','C',weight = 0,zenness= 2, time = 6, distance = 2)
G1.add_edge('D','C',weight = 0,zenness= 4, time = 6, distance = 6)
G1.add_edge('D','B',weight = 0,zenness= 1, time = 5, distance = 2)
G1.add_edge('A','D',weight = 0,zenness= 2, time = 4, distance = 2)

positions = nx.spring_layout(G1)

# Print Network and Edge Lables (Block format)

nx.draw_networkx(G1,pos = positions,node_color = '#a6a6a6',edge_color = '#333333',node_size = 500,font_size = 14,)

edge_labels = {}
for edge in G1.edges():
    nodeA = edge[0]; nodeB = edge[1]
    edgedata = G1.get_edge_data(nodeA,nodeB)
    edgestring = ''
    for key in edgedata.keys():
        edgestring += str(key)+':'+str(edgedata[key])+'\n'
    edge_labels[(nodeA,nodeB)]=edgestring

nx.draw_networkx_edge_labels(G1,pos = positions,edge_labels = edge_labels,font_size = 14)
plt.show()

# Print Network and Edge Lables (Block format)

G1 = nx.DiGraph()

G1.add_edge('A','B',w = 0,z= 5, t = 8, d = 2)
G1.add_edge('B','C',w = 0,z= 2, t = 6, d = 2)
G1.add_edge('D','C',w = 0,z= 4, t = 6, d = 6)
G1.add_edge('D','B',w = 0,z= 1, t = 5, d = 2)
G1.add_edge('A','D',w = 0,z= 2, t = 4, d = 2)

nx.draw_networkx(G1,pos = positions,node_color = '#a6a6a6',edge_color = '#333333',node_size = 500,font_size = 14)

edge_labels = {}
for edge in G1.edges():
    nodeA = edge[0]; nodeB = edge[1]
    edgedata = G1.get_edge_data(nodeA,nodeB)
    edgestring = ''
    for key in edgedata.keys():
        edgestring += str(key)+':'+str(edgedata[key])+'  '
    edge_labels[(nodeA,nodeB)]=edgestring

nx.draw_networkx_edge_labels(G1,pos = positions,edge_labels = edge_labels,font_size = 14)
plt.show()


# Print Network and Edge Lables (Line format)

G1 = nx.DiGraph()

G1.add_edge('A','B',w = 0,z= 5, t = 8, d = 2)
G1.add_edge('B','C',w = 0,z= 2, t = 6, d = 2)
G1.add_edge('D','C',w = 0,z= 4, t = 6, d = 6)
G1.add_edge('D','B',w = 0,z= 1, t = 5, d = 2)
G1.add_edge('A','D',w = 0,z= 2, t = 4, d = 2)

nx.draw_networkx(G1,pos = positions,node_color = '#a6a6a6',edge_color = '#333333',node_size = 500,font_size = 14,)

edge_labels = {}
for edge in G1.edges():
    nodeA = edge[0]; nodeB = edge[1]
    edgedata = G1.get_edge_data(nodeA,nodeB)
    edge_labels[(nodeA,nodeB)] = str(edgedata)

nx.draw_networkx_edge_labels(G1,pos = positions,edge_labels = edge_labels,font_size = 14)
plt.show()
