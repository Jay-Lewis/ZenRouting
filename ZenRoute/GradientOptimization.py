__author__ = 'Justin'

import os
import sys
import json
import networkx as nx
from WeightFunction import weightfunction
from PathSimilarity import pathSimilarity as PS
from numpy import std,linspace,argsort,array
from DisplayNetwork import networkdisplay
from GetRouteInfo import routeinfo
from GenRandomNodes import randomnodes
import matplotlib.pyplot as plt
from random import shuffle

# DESCRIPTION: Generate Estimate of Factor Weight Error Distribution
#


# Load Network
cwd = os.getcwd()
filename = "OSMNetworkReducedSet.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
fh=open(filepath,'rb')
G = nx.read_gexf(fh)

# Loop through weight values
numweights = 5
zenweights = linspace(0.1,0.4,numweights)
shuffle(zenweights)
iter_per_weight = 8

errorProbs = []

for zenweight in zenweights:
    #Generate Probability of Error
    choices = []

    #-- User Weight Testing Loop-----------------------------------------------------
    while(len(choices)<iter_per_weight):
        zenRoute = []
        fastestRoute = []

        pathsimilarity = 1.0
        maxsimilarity = 0.7
        # Keep searching if routes are similar
        while(pathsimilarity > maxsimilarity):

            # I) Generate Random Source and Destination
            lons = nx.get_node_attributes(G,'lon')
            lats = nx.get_node_attributes(G,'lat')
            origin,destination = randomnodes(G,distancelimit=1)       # distancelimit in miles

            # II) Generate Best User-Weighted Route

            # Update Total Edge Weights
            timeweight = 1-zenweight
            weights = [zenweight,timeweight]
            keys = ['Zenness','currenttime']
            for edge in G.edges():
                nodeA = edge[0]
                nodeB = edge[1]
                dict = G[nodeA][nodeB]
                G[nodeA][nodeB]['weight'] = weightfunction(weights,dict,keys)

            # Djkistra's Shortest Path
            zenRoute = nx.shortest_path(G,source = origin,target = destination,weight = 'weight')
            zenRouteInfo = routeinfo(G,zenRoute,['currenttime','Zenness'])

            # III) Generate Fastest Route

            # Djkistra's Shortest Path
            fastestRoute = nx.shortest_path(G,source = origin,target = destination,weight = 'currenttime')
            fastestRouteInfo = routeinfo(G,fastestRoute,['currenttime','Zenness'])

            # Check Path Similarity
            pathsimilarity= PS(zenRoute,fastestRoute)


        # IV) Plot Network and Routes
        routestyles = [{'color': '#ccffcc','width': 20,'name': 'Zen Route'},
                       {'color': '#ffff4d','width': 10,'name': 'Fastest Route'}]       # greenish then yellowish
        Zen_std = std(nx.get_edge_attributes(G,'Zenness').values())

        networkdisplay(G,routes=[zenRoute,fastestRoute],graphstyle='RdYlBu_r',routestyles = routestyles,
                       weightstring='Zenness',normValue=6.0*Zen_std, title='Example')


        # V) Print Route Information
        print('---------------------------------------')
        print('Source:',[lats[origin],lons[origin]])
        print('Destination',[lats[destination],lons[destination]])
        print('---------------------------------------')
        print('ZenRoute:')
        print('-time(min):',zenRouteInfo['currenttime']/60)
        print('-zenness:',zenRouteInfo['Zenness'])
        print('\n')
        print('FastestRoute:')
        print('-time(min):',fastestRouteInfo['currenttime']/60)
        print('-zenness:',fastestRouteInfo['Zenness'])
        print('---------------------------------------')
        print('ZenDiff:    '+str(fastestRouteInfo['Zenness']-zenRouteInfo['Zenness']))
        print('TimeDiff(min):    '+str(zenRouteInfo['currenttime']/60-fastestRouteInfo['currenttime']/60))
        print('---------------------------------------')


        # VI) Get User Feedback:
        print('Options:')
        print('1)Zen'); print('2)Fastest'); print('3)Skip')
        print('\nEnter you answer indicated by number 1-3:')
        choice = sys.stdin.readline()[0:-1]
        # VII) Update User Weight
        if(choice == '1'):
            choices.append(0)
        elif(choice == '2'):
            choices.append(1)

        #-- END User Weight Testing Loop-----------------------------------------------------
    print(choices)
    errorProb = float(sum(choices))/float(len(choices))
    errorProbs.append(errorProb)
    print(errorProb)

# Resort Data

indices = argsort(array(zenweights))
zenweights.sort()
errorProbs = [errorProbs[index] for index in indices]

# Print Estimate of Factor Weight Error Distribution

fig,ax = plt.subplots()
ax.bar(zenweights,errorProbs)
ax.set_xlim([0,1])
plt.title('Probability of Error vs. Zenweight')
plt.xlabel('Zenweight')
plt.ylabel('Prob. of Error')
plt.show()

# Save Information

folder = filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','GradientOptimization'))

filename = "ErrorDistribution2.json"
filepath = os.path.abspath(os.path.join(folder,filename))
with open(filepath, 'w') as outfile:
    json.dump(errorProbs, outfile)

filename = "zenweights2.json"
weights = zenweights.tolist()
filepath = os.path.abspath(os.path.join(folder,filename))
with open(filepath, 'w') as outfile:
    json.dump(weights, outfile)
