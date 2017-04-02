__author__ = 'Justin'

__author__ = 'Justin'




import networkx as nx
import os
from DisplayNetwork import networkdisplay
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from numpy.random import rand

# Plot Simple Network Graph for Example

G1 = nx.Graph()

nodes = ['A','B','C','D','E','F']
for node in nodes:
    G1.add_node(node)

keys = ['zenness','time','distance']
G1.add_edge('A','B',weight = 1,zenness= 5, time = 8, distance = 2)
G1.add_edge('B','C',weight = 2,zenness= 2, time = 6, distance = 2)
G1.add_edge('D','C',weight = 3,zenness= 4, time = 6, distance = 6)
G1.add_edge('D','B',weight = 4,zenness= 1, time = 5, distance = 2)
G1.add_edge('A','D',weight = 5,zenness= 2, time = 4, distance = 2)
G1.add_edge('D','E',weight = 5,zenness= 2, time = 4, distance = 2)
G1.add_edge('E','F',weight = 5,zenness= 2, time = 4, distance = 2)
G1.add_edge('F','C',weight = 5,zenness= 2, time = 4, distance = 2)
G1.add_edge('E','A',weight = 5,zenness= 2, time = 4, distance = 2)

positions = nx.spring_layout(G1)
print(positions)
nx.draw_networkx(G1,pos = positions,node_color = '#a6a6a6',edge_color = '#333333',node_size = 500,font_size = 14)
# edge_labels = nx.get_edge_attributes(G1,'weight')
# nx.draw_networkx_edge_labels(G1,pos = positions,edge_labels = edge_labels,font_size = 14)


# Draw Shortest Path

shortestpath = nx.shortest_path(G1,'A','F','weight')

edgelist =[]
for nodeA, nodeB in zip(shortestpath,shortestpath[1:]):
    edgelist.append((nodeA,nodeB))

redcolor = '#ff4d4d'
greencolor = '#5cd65c'
nx.draw_networkx_edges(G1,pos = positions,edge_color = greencolor,edgelist=edgelist,width=8,alpha=0.5)
nx.draw_networkx_nodes(G1,pos = positions,node_color = greencolor,node_size = 500,font_size = 14,nodelist=shortestpath[1:-1])


# Draw Alternate Path

path = ['A','D','E','F']

edgelist =[]
for nodeA, nodeB in zip(path,path[1:]):
    edgelist.append((nodeA,nodeB))

nx.draw_networkx_edges(G1,pos = positions,edge_color = redcolor,edgelist=edgelist,width=8,alpha=0.5)
nx.draw_networkx_nodes(G1,pos = positions,node_color = redcolor,node_size = 500,font_size = 14,nodelist=path[1:-1])

# Draw Origin and Destination

graycolor = '#a6a6a6'
nodes = ['A','F']
nx.draw_networkx_nodes(G1,pos = positions,node_color = graycolor,node_size = 500,font_size = 14,nodelist=nodes)

# Draw Legend

red_patch = mpatches.Patch(color=redcolor, label='Fastest Route')
green_patch = mpatches.Patch(color=greencolor, label='Zen Route')
yellow_patch = mpatches.Patch(color=graycolor, label='Start & End')
plt.legend(handles = [red_patch,green_patch,yellow_patch])
plt.show()


