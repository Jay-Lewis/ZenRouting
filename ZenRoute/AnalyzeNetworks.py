__author__ = 'Justin'

import os
from os.path import isfile, join
import networkx as nx
from datetime import datetime
import numpy as np
from GetRouteInfo import routeinfo
from GenRandomNodes import randompairs
from DisplayNetwork import networkdisplay
import matplotlib.pyplot as plt


# Load Networks

Graphs = []
cwd = os.getcwd()
folderpath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks','CstatHistory'))
files = [f for f in os.listdir(folderpath) if isfile(join(folderpath, f))]
for filename in files:
    filepath = os.path.abspath(os.path.join(cwd,folderpath,filename))
    fh=open(filepath,'rb')
    G = nx.read_gexf(fh)
    fh.close

    myDate = datetime.strptime(filename,"%H-%M(%d-%m-%Y).gexf")
    G.graph['datetime']=myDate
    Graphs.append(G)


# Find Normalization Factor
# maxZenscore = 1
# maxs = []
# for G in Graphs:
#     zenscores = nx.get_edge_attributes(G,'Zenness').values()
#     MAX = float(max(zenscores))
#     maxs.append(MAX)
# maxZenscore = max(maxs)

# Zen Relevance vs. Average Congestion
averageCongestion = []
averageZenRatio = []
numpairs = 2000


# Choose Random Source and Destination Pairs
randpairs = randompairs(G,numpairs,distancelimit=3)  # distancelimit in miles
for G in Graphs:
    zenscores = nx.get_edge_attributes(G,'Zenness').values()
    averageCongestion.append(np.mean(zenscores))

    Zenratio = []
    for pair in randpairs:
        # Set Origin and Destination
        origin = pair[0]; destination = pair[1]

        # Zen Route
        Zenpath = nx.shortest_path(G,source = origin,target = destination,weight = 'weight')
        ZenpathInfo = routeinfo(G,Zenpath,['Zenness','currenttime'])
        # Fastest Route
        Fastpath = nx.shortest_path(G,source = origin,target = destination,weight = 'currenttime')
        FastpathInfo = routeinfo(G,Fastpath,['Zenness','currenttime'])

        ZenDiff = FastpathInfo['Zenness']-ZenpathInfo['Zenness']
        TimeDiff = ZenpathInfo['currenttime']-FastpathInfo['currenttime']
        if(TimeDiff != 0):
            Zenratio.append(ZenDiff/TimeDiff)
    averageZenRatio.append(np.mean(Zenratio))

# Plot Zen Relevance vs. Average Congestion

plt.scatter(averageCongestion,averageZenRatio,s=10)
plt.xlabel('Average Congestion')
plt.ylabel('Zen Relevance')
plt.show()

# Plot Zenness Histograms
# for index,G in enumerate(Graphs):
#     fig,ax = plt.subplots()
#     zenscores = nx.get_edge_attributes(G,'Zenness').values()
#     # hist = numpy.histogram(values)
#     zenrange = [0,800]
#     ax.hist(zenscores,range=zenrange,bins = 50)
#     plt.title(str(G.graph['datetime']))
# plt.show()


# # Plot Networks
# for G in Graphs:
#     networkdisplay(G,[],'RdYlBu_r',[],maxZenscore,str(G.graph['datetime']))

