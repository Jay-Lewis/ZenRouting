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


# Zen Relevance vs. Average Congestion
averageCongestion = []
averageZenRatio = []
averageZenDiff = []
numpairs = 1000

# Choose Random Source and Destination Pairs
randpairs = randompairs(G,numpairs,distancelimit=3)  # distancelimit in miles

# Calculate Average Zen Ratio for each network slice
for G in Graphs:
    zenscores = nx.get_edge_attributes(G,'Zenness').values()

    Zenratio = 0
    ZenDiffs = 0
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

        if(TimeDiff > 0 and ZenDiff > 0):
            Zenratio += ZenDiff/TimeDiff
            ZenDiffs += ZenDiff

    if(Zenratio != 0):
        averageZenRatio.append(Zenratio/numpairs)
        averageZenDiff.append(ZenDiffs/numpairs)
        averageCongestion.append(np.mean(zenscores))

# Plot Zen Relevance vs. Average Congestion

fig,ax = plt.subplots()
plt.scatter(averageCongestion,averageZenRatio,s=10)
plt.xlabel('Average Network Congestion')
plt.ylabel('Average Zen/Time Tradeoff')

fig,ax = plt.subplots()
plt.scatter(averageCongestion,averageZenDiff,s=10)
plt.xlabel('Average Network Congestion')
plt.ylabel('Average ZenDiff')
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

