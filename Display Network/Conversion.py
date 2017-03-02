__author__ = 'Pablo'

import os
import networkx as nx

cwd = os.getcwd()
filename = "OSMNetworkReducedSet.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))

fh=open(filepath,'rb')
G = nx.read_gexf(fh)
fh.close

nx.write_graphml(G, "ReducedSet.graphml")