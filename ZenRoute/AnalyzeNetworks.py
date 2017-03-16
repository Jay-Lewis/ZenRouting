__author__ = 'Justin'

import os
from os.path import isfile, join
cwd = os.getcwd()
import networkx as nx
from datetime import datetime
import numpy as np
from random import choice
from geopy.distance import vincenty as latlondist
from GetRouteInfo import routeinfo
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
maxiter = 800

for G in Graphs:
    zenscores = nx.get_edge_attributes(G,'Zenness').values()
    averageCongestion.append(np.mean(zenscores))

    Zenratio = []
    for index in range(1,maxiter,1):
        # Generate Source and Destination
        distancelimit = 3   # distance in miles
        lons = nx.get_node_attributes(G,'lon')
        lats = nx.get_node_attributes(G,'lat')

        nodesdist = 0
        connected = False
        while(nodesdist < distancelimit or not(connected)):
            randomnodes = [choice(G.nodes()),choice(G.nodes())]
            origin = randomnodes[0]
            destination = randomnodes[1]
            nodesdist = latlondist([lats[origin],lons[origin]],[lats[destination],lons[destination]]).miles
            if nx.has_path(G,origin,destination):
                connected = True
            else:
                connected = False

        # Zen Route
        Zenpath = nx.shortest_path(G,source = randomnodes[0],target = randomnodes[1],weight = 'weight')
        ZenpathInfo = routeinfo(G,Zenpath,['Zenness','currenttime'])
        # Fastest Route
        Fastpath = nx.shortest_path(G,source = randomnodes[0],target = randomnodes[1],weight = 'currenttime')
        FastpathInfo = routeinfo(G,Fastpath,['Zenness','currenttime'])

        ZenDiff = FastpathInfo['Zenness']-ZenpathInfo['Zenness']
        TimeDiff = ZenpathInfo['currenttime']-FastpathInfo['currenttime']
        if(TimeDiff != 0):
            Zenratio.append(ZenDiff/TimeDiff)

    averageZenRatio.append(np.mean(Zenratio))

# Plot Zen Relevance vs. Average Congestion

plt.scatter(averageCongestion,averageZenRatio,s=10)
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

