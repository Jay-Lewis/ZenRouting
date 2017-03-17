

import networkx as nx
from DisplayNetwork import networkdisplay
from numpy.random import rand

G1 = nx.DiGraph()

nodes = ['A','B','C','D']
for node in nodes:
    randomnums = rand(1,2)
    dict = {'lat':randomnums[0][0],'lon':randomnums[0][1]}
    G1.add_node(node,attr_dict=dict)

keys = ['zenness','time','distance']
G1.add_edge('A','B',weight = 0,zenness= 5, time = 8, distance = 2)
G1.add_edge('B','C',weight = 0,zenness= 2, time = 6, distance = 2)
G1.add_edge('D','C',weight = 0,zenness= 4, time = 6, distance = 6)
G1.add_edge('D','B',weight = 0,zenness= 1, time = 5, distance = 2)
G1.add_edge('A','D',weight = 0,zenness= 2, time = 4, distance = 2)

factorstring = 'zenness'
values = nx.get_edge_attributes(G1,factorstring).values()
MAX = float(max(values))
networkdisplay(G1,[],'Blues',[],factorstring,MAX,'Network Graph Example')
