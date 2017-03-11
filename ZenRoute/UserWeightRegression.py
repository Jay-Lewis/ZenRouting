__author__ = 'Justin'

import os
import networkx as nx
from WeightFunction import weightfunction
from random import choice
from geopy.distance import vincenty as latlondist
from DisplayNetwork import networkdisplay
from GetRouteInfo import routeinfo


# DESCRIPTION: This script is used to experimentally infer a user's characteristic weights based on route decisions and
# user feedback

# Initialize User Weights
zenWeight = 0.5
timeWeight = 0.5

# Load Network
cwd = os.getcwd()
filename = "OSMNetworkReducedSet.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
fh=open(filepath,'rb')
G = nx.read_gexf(fh)

#-- User Weight Testing Loop-----------------------------------------------------
zenRoute = []
fastestRoute = []

while(zenRoute==fastestRoute):
    # I) Generate Random Source and Destination
    distancelimit = 1   # distance in miles
    lons = nx.get_node_attributes(G,'lon')
    lats = nx.get_node_attributes(G,'lat')

    nodesdist = 0
    while(nodesdist < distancelimit):
        randomnodes = [choice(G.nodes()),choice(G.nodes())]
        origin = randomnodes[0]
        destination = randomnodes[1]
        nodesdist = latlondist([lats[origin],lons[origin]],[lats[destination],lons[destination]]).miles

    print('Source:',[lats[randomnodes[0]],lons[randomnodes[0]]])
    print('Destination',[lats[randomnodes[1]],lons[randomnodes[1]]])


    # II) Generate Best User-Weighted Route

    # Update Total Edge Weights
    weights = [zenWeight,timeWeight]
    keys = ['Zenness','currenttime']
    for edge in G.edges():
        nodeA = edge[0]
        nodeB = edge[1]
        dict = G[nodeA][nodeB]
        G[nodeA][nodeB]['weight'] = weightfunction(weights,dict,keys)

    # Djkistra's Shortest Path
    zenRoute = nx.shortest_path(G,source = randomnodes[0],target = randomnodes[1],weight = 'weight')
    zenRouteInfo = routeinfo(G,zenRoute,['currenttime','Zenness'])

    # III) Generate Fastest Route

    # Update Total Edge Weights
    weights = [0,1]                     # only time is accounted for due to full weight given to 'currenttime' value
    keys = ['Zenness','currenttime']
    for edge in G.edges():
        nodeA = edge[0]
        nodeB = edge[1]
        dict = G[nodeA][nodeB]
        G[nodeA][nodeB]['weight'] = weightfunction(weights,dict,keys)

    # Djkistra's Shortest Path
    fastestRoute = nx.shortest_path(G,source = randomnodes[0],target = randomnodes[1],weight = 'weight')
    fastestRouteInfo = routeinfo(G,fastestRoute,['currenttime','Zenness'])

# IV) Print Route Information
print('\n\n')
print('---------------------------------------')
print('ZenRoute:')
print('-time(min):',zenRouteInfo['currenttime']/60)
print('-zenness:',zenRouteInfo['Zenness'])
print('\n')
print('FastestRoute:')
print('-time(min):',fastestRouteInfo['currenttime']/60)
print('-zenness:',fastestRouteInfo['Zenness'])
print('---------------------------------------')
# IV) Plot Network and Routes
routestyles = [{'color':' #ccffcc','width':12},{'color':' #99ccff','width':7}]       # greenish then blueish
networkdisplay(G,routes=[zenRoute,fastestRoute],graphstyle='RdYlBu_r',routestyles = routestyles,normalize = True, title='Example')
