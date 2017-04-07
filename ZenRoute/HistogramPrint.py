__author__ = 'Justin'

import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

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


histinfo = np.histogram(values)
probs = histinfo[0]
scores = histinfo[1]

# Normalize
probs = np.multiply(probs,1.0/sum(probs))

fig,ax = plt.subplots()

print(probs)
print(scores)
plt.bar(scores[0:-1],probs,np.diff(scores))
plt.ylabel('Probability')
plt.xlabel('ZenScore')
plt.title('Histogram Plot of Edge Zenness')
plt.show()
