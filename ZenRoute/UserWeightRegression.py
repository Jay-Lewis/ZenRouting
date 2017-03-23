__author__ = 'Justin'

import os
import sys
import json
import networkx as nx
from WeightFunction import weightfunction
from PathSimilarity import pathSimilarity as PS
from numpy import std,linspace
from DisplayNetwork import networkdisplay
from GetRouteInfo import routeinfo
from GenRandomNodes import randomnodes
import webbrowser
import matplotlib.pyplot as plt


# DESCRIPTION: This script is used to experimentally infer a user's characteristic weights based on route decisions and
# user feedback

# Initialize User Weights
zenWeight = 0.5
timeWeight = 1-zenWeight
# print('Enter your first name: ')
# person = sys.stdin.readline()[0:-1]
person = 'Justin'

# Load Network
cwd = os.getcwd()
filename = "OSMNetworkReducedSet.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
fh=open(filepath,'rb')
G = nx.read_gexf(fh)

userweight_history = []
pathinfo_history = []
choice_history = []

numiter = 25
weight_delta = 0.05

#-- User Weight Testing Loop-----------------------------------------------------
for itercount in linspace(1,numiter,numiter):
    zenRoute = []
    fastestRoute = []

    pathsimilarity = 1.0
    # Keep searching if routes are similar
    while(pathsimilarity > 0.5):

        # I) Generate Random Source and Destination
        lons = nx.get_node_attributes(G,'lon')
        lats = nx.get_node_attributes(G,'lat')
        origin,destination = randomnodes(G,distancelimit=1)       # distancelimit in miles

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
        zenRoute = nx.shortest_path(G,source = origin,target = destination,weight = 'weight')
        zenRouteInfo = routeinfo(G,zenRoute,['currenttime','Zenness'])

        # III) Generate Fastest Route

        # Djkistra's Shortest Path
        fastestRoute = nx.shortest_path(G,source = origin,target = destination,weight = 'currenttime')
        fastestRouteInfo = routeinfo(G,fastestRoute,['currenttime','Zenness'])

        # Check Path Similarity
        pathsimilarity= PS(zenRoute,fastestRoute)


    # IV) Plot Network and Routes
    routestyles = [{'color':' #ccffcc','width':20},{'color':' #ffff4d','width':10}]       # greenish then yellowish
    Zen_std = std(nx.get_edge_attributes(G,'Zenness').values())

    networkdisplay(G,routes=[zenRoute,fastestRoute],graphstyle='RdYlBu_r',routestyles = routestyles,
                   weightstring='Zenness',normValue=6.0*Zen_std, title='Example')

    # Plot Routes on GMaps
    fastestRoutestring = "https://www.google.com/maps/dir"
    Zenroutestring = "https://www.google.com/maps/dir"

    lons = nx.get_node_attributes(G,'lon')
    lats = nx.get_node_attributes(G,'lat')

    numpts = int(max([len(fastestRoute),len(zenRoute)])/3)
    fastmidnodes = [fastestRoute[int(i)] for i in linspace(1,len(fastestRoute)-2,numpts)]
    zenmidnodes =[zenRoute[int(i)] for i in linspace(1,len(zenRoute)-2,numpts)]

    for node in [origin]+fastmidnodes+[destination]:
        fastestRoutestring += '/'+str(lats[node])+','+str(lons[node])
    for node in [origin]+zenmidnodes+[destination]:
        Zenroutestring += '/'+str(lats[node])+','+str(lons[node])

    # webbrowser.open(fastestRoutestring,new=1)
    # webbrowser.open(Zenroutestring)


    # V) Print Route Information
    print('---------------------------------------')
    print('Source:',[lats[origin],lons[origin]])
    print('Destination',[lats[destination],lons[destination]])
    print('---------------------------------------')
    print('ZenRoute:')
    print('-time(min):',zenRouteInfo['currenttime']/60)
    print('-zenness:',zenRouteInfo['Zenness'])
    print('Gmaps Link:')
    print(fastestRoutestring)
    print('\n')
    print('FastestRoute:')
    print('-time(min):',fastestRouteInfo['currenttime']/60)
    print('-zenness:',fastestRouteInfo['Zenness'])
    print('Gmaps Link:')
    print(Zenroutestring)
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
        zenWeight += weight_delta
    elif(choice == '2'):
        zenWeight -= weight_delta
    timeWeight = 1-zenWeight

    # VIII) Store run info
    userweight_history.append(zenWeight)
    pathinfo = {'Zen':zenRoute,'Fast':fastestRoute}
    pathinfo_history.append(pathinfo)
    choice_history.append(choice)

    #-- END User Weight Testing Loop-----------------------------------------------------

    if(itercount>20):
        # IX) Plot User Weights
        plt.plot(linspace(1,itercount,itercount),userweight_history)
        plt.show()
        print(userweight_history)

    # Save info to folder
    folder = filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','UserWeights',person))

    filename = "UserWeights"
    filepath = os.path.abspath(os.path.join(folder,filename))
    with open(filepath, 'w') as outfile:
        json.dump(userweight_history, outfile)

    filename = "PathOptions"
    filepath = os.path.abspath(os.path.join(folder,filename))
    with open(filepath, 'w') as outfile:
        json.dump(pathinfo_history, outfile)

    filename = "Choices"
    filepath = os.path.abspath(os.path.join(folder,filename))
    with open(filepath, 'w') as outfile:
        json.dump(choice_history, outfile)

    filename = "Graph G.gexf"
    filepath = os.path.abspath(os.path.join(folder,filename))
    nx.write_gexf(G,filepath)