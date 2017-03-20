__author__ = 'Justin'

__author__ = 'Justin'

import os
import networkx as nx
from datetime import datetime
from SetNetworkTime import set_network_time
from WeightFunction import weightfunction
from random import choice
from geopy.distance import vincenty as latlondist
from GetRouteInfo import routeinfo
import matplotlib.pyplot as plt
import numpy as np

# DESCRIPTION: This script will generate the approx. Pareto Frontier for randomized source and destination


# Load Network
cwd = os.getcwd()
filename = "OSMNetworkReducedSet.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
print(filepath)

fh=open(filepath,'rb')
G = nx.read_gexf(fh)
fh.close

# Update Time Segments
set = 0

if set == 1:
    now = datetime.now()
    G = set_network_time(G,'currenttime',now,1800)


#Generate Number of Pareto Frontier Graphs

numiterations = 1
for i in range(0,numiterations,1):

    # Loop Until Enough Pareto Optimal Points Found

    numunique = 0
    numParetoOptimal = 6
    while(numunique < numParetoOptimal):

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

        print('Source:',[lats[randomnodes[0]],lons[randomnodes[0]]])
        print('Destination',[lats[randomnodes[1]],lons[randomnodes[1]]])


        # Obtain Pareto Frontier for Randomized Origin and Destination
        numpts = 20
        Zenscore_pts = []
        time_pts = []
        annotations = []

        for zenweight in np.linspace(0,1,numpts):

            # Update Total Edge Weights
            factorweights = [zenweight,1-zenweight]
            factors = ['Zenness','currenttime']
            for edge in G.edges():
                nodeA = edge[0]
                nodeB = edge[1]
                dict = G[nodeA][nodeB]
                G[nodeA][nodeB]['weight'] = weightfunction(factorweights,dict,factors)


            # Djkistra's Shortest Path
            path = nx.shortest_path(G,source = randomnodes[0],target = randomnodes[1],weight = 'weight')

            # Get Shortest Path Information
            path_dict = routeinfo(G,path,['Zenness','currenttime'])
            Zenscore = path_dict['Zenness']
            time = path_dict['currenttime']

            Zenscore_pts.append(Zenscore)
            time_pts.append(time)
            annotations.append('ZW:'+str("%.3f"%zenweight)+',V:'+str("%.1f"%np.dot(factorweights,[Zenscore,time])))

        numunique=np.unique(Zenscore_pts).size


    # Plot Pareto Frontier
    fig,ax = plt.subplots()
    ax.scatter(Zenscore_pts,time_pts,s=10)
    for Zen,t,annotation in zip(np.unique(Zenscore_pts),np.unique(time_pts)[::-1],np.unique(annotations)):
        ax.annotate(annotation,(Zen,t))

    plt.xlabel('Zenscores')
    plt.xlim([0,2500])
    plt.ylabel('Times (s)')
    plt.ylim([0,2500])

# Show All Graphs at Once
plt.show()

# IV) Plot Network and Routes
# routestyles = [{'color':' #ccffcc','width':12}]       # greenish
# zenMAX = max(nx.get_edge_attributes(G,'Zenness').values())
# networkdisplay(G,routes=[path],graphstyle='RdYlBu_r',routestyles = routestyles,
#                weightstring='Zenness',maxValue=zenMAX, title='Example')