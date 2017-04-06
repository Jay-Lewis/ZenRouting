
import os
import matplotlib.pyplot as plt
import networkx as nx
import json
import numpy as np
from ParetoFrontier import rand_paretofront

# # Load Network
# cwd = os.getcwd()
# filename = "OSMNetworkReducedSet.gexf"
# filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
# fh=open(filepath,'rb')
# G = nx.read_gexf(fh)
#
# numweights = 20
# weights = np.linspace(0,1,numweights)
# numunique = 3
# rand_paretofront(G,weights,['Zenness','currenttime'],numunique,'Zenness')





# Print Bar Graph of Gradient Optimization

# Load Data
cwd = os.getcwd()
folder = filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','GradientOptimization'))

filename = "ErrorDistribution3.json"
filepath = os.path.abspath(os.path.join(folder,filename))
with open(filepath) as data:
    errorProbs = json.load(data)

filename = "zenweights3.json"
filepath = os.path.abspath(os.path.join(folder,filename))
with open(filepath) as data:
    zenweights = json.load(data)

# Resort Data

print(zenweights)
print(errorProbs)
indices = np.argsort(np.array(zenweights))
zenweights.sort()
errorProbs = [errorProbs[index] for index in indices]

# Plot Data

fig,ax = plt.subplots()
ax.plot(zenweights,errorProbs)
ax.set_xlim([0,1])
plt.title('Probability of Error vs. Zenweight')
plt.xlabel('Zenweight')
plt.ylabel('Prob. of Error')
plt.show()
#
#
#
#
# # Print Histogram of Zen Scores
#
# # Load Network
# cwd = os.getcwd()
# filename = "OSMNetworkReducedSet.gexf"
# filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
# fh=open(filepath,'rb')
# G = nx.read_gexf(fh)
#
#
# fig,ax = plt.subplots()
# zenscores = nx.get_edge_attributes(G,'Zenness').values()
# # hist = numpy.histogram(values)
# zenrange = [0,800]
# ax.hist(zenscores,range=zenrange,bins = 50)
# plt.title('Zenscore Histogram')
# plt.xlabel('Zenscore')
# plt.ylabel('Probability')
# plt.show()





