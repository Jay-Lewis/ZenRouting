__author__ = 'Justin'

import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy

# Load Network
cwd = os.getcwd()
filename = "OSMNetworkReducedSet.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))

fh=open(filepath,'rb')
G = nx.read_gexf(fh)
fh.close



# Print Edge Basetime Value Histogram
values = []

for edge in G.edges():
    nodeA = edge[0]
    nodeB = edge[1]
    values.append(G[nodeA][nodeB]['Zenness'])

# hist = numpy.histogram(values)
plt.hist(values)
plt.show()


