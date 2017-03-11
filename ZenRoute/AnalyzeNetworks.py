__author__ = 'Justin'

import os
from os.path import isfile, join
cwd = os.getcwd()
import networkx as nx
import datetime
from DisplayNetwork import networkdisplay

# Load Networks

Graphs = []
cwd = os.getcwd()
folderpath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks','CstatHistory'))
files = [f for f in os.listdir(folderpath) if isfile(join(folderpath, f))]
print(files)
for filename in files:
    filepath = os.path.abspath(os.path.join(cwd,folderpath,filename))
    fh=open(filepath,'rb')
    G = nx.read_gexf(fh)
    fh.close

    myDate = datetime.strptime(filename,"%H-%M(%d-%m-%Y).gexf")
    G.graph['datetime']=myDate
    Graphs.append(G)


# Normalize Networks
maxZenscore = 1
maxs = []
for G in Graphs:
    zenscores = nx.get_edge_attributes(G,'Zenness')
    maxZenscore = max(zenscores)
    maxs.append()

# Plot Networks

for G in Graphs:
    networkdisplay(H,[],'RdYlBu_r',[])

