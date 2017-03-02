__author__ = 'Justin'

import os
import networkx as nx

# Load Network
cwd = os.getcwd()
filename = "OSMNetworkReduced.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
print(filepath)

fh=open(filepath,'rb')
G = nx.read_gexf(fh)
fh.close

cwd = os.getcwd()
filename = "OSMNetwork.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
print(filepath)

fh=open(filepath,'rb')
H = nx.read_gexf(fh)
fh.close


print(len(G.nodes()))

print(len(H.nodes()))