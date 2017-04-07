__author__ = 'Justin'

import os
import sys
import json
import networkx as nx
from WeightFunction import weightfunction
from PathSimilarity import pathSimilarity as PS
from numpy import std,linspace,argsort,array,linspace,unique
from DisplayNetwork import networkdisplay
from GetRouteInfo import routeinfo
from GenRandomNodes import randomnodes
from ParetoFrontier import rand_paretofront
import matplotlib.pyplot as plt
from random import shuffle

# DESCRIPTION: Generate Estimate of Factor Weight Error Distribution
#

# Initialize data
numweights = 20
weights = linspace(0,1,numweights)
weightchosen = {weight:0 for weight in weights}
uniquerange = [3,5]
numiter = 30

# Load Network
cwd = os.getcwd()
filename = "OSMNetworkReducedSet.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
fh=open(filepath,'rb')
G = nx.read_gexf(fh)

for _ in range(0,numiter,1):

    # Generate Pareto Frontier

    cluster_weights, paths, pathsinfo = rand_paretofront(G,weights,['Zenness','currenttime'],
                                                         uniquerange[0],uniquerange[1],'Zenness')


    # Print Route Information
    print('------------------------------------------------------------------------------')
    print('/////////////////////////////////////////////////////////////////////////////')
    Zenscore_pts = []
    time_pts = []
    for index,path in enumerate(paths):
        print('---------------------------------------')
        print('Route '+str(index)+':')
        print('-time(min):',pathsinfo[index]['currenttime']/60)
        print('-zenness:',pathsinfo[index]['Zenness'])
        print('----------------')
        print('-zen diff:',pathsinfo[0]['Zenness']-pathsinfo[index]['Zenness'])
        print('-time diff:',(pathsinfo[index]['currenttime']-pathsinfo[0]['currenttime'])/60)
        print('---------------------------------------')
        Zenscore_pts.append(pathsinfo[index]['Zenness'])
        time_pts.append(pathsinfo[index]['currenttime']/60)


    # Plot All Route Options
    routestyles=[]
    # listcolors = ['#cc9999','#ccff99','#999933','#ffcc99','#996633','#767777']
    listcolors = ['#ffff4d','#66ff66','#00cd00','#008b00','#006400','#cc9999','#ccff99','#999933']

    for index in range(0,len(paths),1):
        dict = {'color': listcolors[index],'width': 10,'name': 'Route '+str(index)+':'}
        routestyles.append(dict)

    Zen_std = std(nx.get_edge_attributes(G,'Zenness').values())
    networkdisplay(G,routes=paths,graphstyle='RdYlBu_r',routestyles = routestyles,
                   weightstring='Zenness',normValue=6.0*Zen_std, title='Pareto Optimal Routes')

    # # Plot Pareto Frontier
    # fig,ax = plt.subplots()
    # MIN = min(time_pts)
    # time_pts[:]=[value/MIN for value in time_pts]   # Normalize time to minimum value
    # ax.scatter(Zenscore_pts,time_pts,s=10)
    # plt.title('Pareto Frontier Example')
    # plt.xlabel('Zenscores')
    # plt.ylabel('Time Normalized to Fastest Route')
    #
    # for index,weightgroup in enumerate(cluster_weights):
    #     if(len(weightgroup)==1):
    #         a = "%.2f" % weightgroup[0]
    #         ax.annotate('['+a+']',(Zenscore_pts[index],time_pts[index]))
    #     else:
    #         a = "%.2f" % weightgroup[0]
    #         b = "%.2f" % weightgroup[-1]
    #         ax.annotate('['+a+'-'+b+']',(Zenscore_pts[index],time_pts[index]))
    # plt.show()




    # Get User Feedback:
    print('Options:')
    print('Enter you answer indicated by number 0-'+str(len(paths)-1)+'')
    print('OR')
    print("'s' for skip  and  'r' for refine:")
    choice = sys.stdin.readline()[0:-1]

    if(choice == 'r'):
        # Prune Options:
        print('Options:')
        print('Enter list separated by commas of choices to view')
        print('Example => 1,2,3')
        string = sys.stdin.readline()
        chosenindices = [int(element) for index,element in enumerate(string) if(index % 2 == 0) ]
        print('Chosen:',chosenindices)


        # Plot All Chosen Options
        routestyles=[]
        for index in chosenindices:
            dict = {'color': listcolors[index],'width': 10,'name': 'Route '+str(index)+':'}
            routestyles.append(dict)

        chosenpaths = [paths[i] for i in chosenindices]
        chosenpathinfos = [paths[i] for i in chosenindices]

        Zen_std = std(nx.get_edge_attributes(G,'Zenness').values())
        networkdisplay(G,routes=chosenpaths,graphstyle='RdYlBu_r',routestyles = routestyles,
                       weightstring='Zenness',normValue=6.0*Zen_std, title='Pareto Optimal Routes')

        # Get Refined User Feedback:
        print('Options:')
        print('Enter you answer indicated by number 0-'+str(len(paths)-1)+'')
        print('OR')
        print("'s' for skip  and  'r' for refine:")
        choice = sys.stdin.readline()[0:-1]




    if(choice != 's'):
        # Save contribution to weight error distribution

        for weight in cluster_weights[int(choice)]:
            weightchosen[weight] += 1


# Print Estimate of Factor Weight Error Distribution

fig,ax = plt.subplots()
x = sorted(weightchosen.keys())
y = [1.0-float(weightchosen[key])/float(numiter) for key in x]
ax.bar(x,y)
ax.set_xlim([0,1])
plt.title('Probability of Error vs. Zenweight')
plt.xlabel('Zenweight')
plt.ylabel('Prob. of Error')
plt.show()

# Save Information

folder = filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','GradientOptimization'))

filename = "ErrorDistribution3.json"
filepath = os.path.abspath(os.path.join(folder,filename))
with open(filepath, 'w') as outfile:
    json.dump(y, outfile)

filename = "zenweights3.json"
filepath = os.path.abspath(os.path.join(folder,filename))
with open(filepath, 'w') as outfile:
    json.dump(x, outfile)










# # Loop through weight values
# numweights = 5
# zenweights = linspace(0.1,0.4,numweights)
# shuffle(zenweights)
# iter_per_weight = 8
#
# errorProbs = []
#
# for zenweight in zenweights:
#     #Generate Probability of Error
#     choices = []
#
#     #-- User Weight Testing Loop-----------------------------------------------------
#     while(len(choices)<iter_per_weight):
#         zenRoute = []
#         fastestRoute = []
#
#         pathsimilarity = 1.0
#         maxsimilarity = 0.7
#         # Keep searching if routes are similar
#         while(pathsimilarity > maxsimilarity):
#
#             # I) Generate Random Source and Destination
#             lons = nx.get_node_attributes(G,'lon')
#             lats = nx.get_node_attributes(G,'lat')
#             origin,destination = randomnodes(G,distancelimit=1)       # distancelimit in miles
#
#             # II) Generate Best User-Weighted Route
#
#             # Update Total Edge Weights
#             timeweight = 1-zenweight
#             weights = [zenweight,timeweight]
#             keys = ['Zenness','currenttime']
#             for edge in G.edges():
#                 nodeA = edge[0]
#                 nodeB = edge[1]
#                 dict = G[nodeA][nodeB]
#                 G[nodeA][nodeB]['weight'] = weightfunction(weights,dict,keys)
#
#             # Djkistra's Shortest Path
#             zenRoute = nx.shortest_path(G,source = origin,target = destination,weight = 'weight')
#             zenRouteInfo = routeinfo(G,zenRoute,['currenttime','Zenness'])
#
#             # III) Generate Fastest Route
#
#             # Djkistra's Shortest Path
#             fastestRoute = nx.shortest_path(G,source = origin,target = destination,weight = 'currenttime')
#             fastestRouteInfo = routeinfo(G,fastestRoute,['currenttime','Zenness'])
#
#             # Check Path Similarity
#             pathsimilarity= PS(zenRoute,fastestRoute)
#
#
#         # IV) Plot Network and Routes
#         routestyles = [{'color': '#ccffcc','width': 20,'name': 'Zen Route'},
#                        {'color': '#ffff4d','width': 10,'name': 'Fastest Route'}]       # greenish then yellowish
#         Zen_std = std(nx.get_edge_attributes(G,'Zenness').values())
#
#         networkdisplay(G,routes=[zenRoute,fastestRoute],graphstyle='RdYlBu_r',routestyles = routestyles,
#                        weightstring='Zenness',normValue=6.0*Zen_std, title='Example')
#
#
#         # V) Print Route Information
#         print('---------------------------------------')
#         print('Source:',[lats[origin],lons[origin]])
#         print('Destination',[lats[destination],lons[destination]])
#         print('---------------------------------------')
#         print('ZenRoute:')
#         print('-time(min):',zenRouteInfo['currenttime']/60)
#         print('-zenness:',zenRouteInfo['Zenness'])
#         print('\n')
#         print('FastestRoute:')
#         print('-time(min):',fastestRouteInfo['currenttime']/60)
#         print('-zenness:',fastestRouteInfo['Zenness'])
#         print('---------------------------------------')
#         print('ZenDiff:    '+str(fastestRouteInfo['Zenness']-zenRouteInfo['Zenness']))
#         print('TimeDiff(min):    '+str(zenRouteInfo['currenttime']/60-fastestRouteInfo['currenttime']/60))
#         print('---------------------------------------')
#
#
#         # VI) Get User Feedback:
#         print('Options:')
#         print('1)Zen'); print('2)Fastest'); print('3)Skip')
#         print('\nEnter you answer indicated by number 1-3:')
#         choice = sys.stdin.readline()[0:-1]
#         # VII) Update User Weight
#         if(choice == '1'):
#             choices.append(0)
#         elif(choice == '2'):
#             choices.append(1)
#
#         #-- END User Weight Testing Loop-----------------------------------------------------
#     print(choices)
#     errorProb = float(sum(choices))/float(len(choices))
#     errorProbs.append(errorProb)
#     print(errorProb)
#
# # Resort Data
#
# indices = argsort(array(zenweights))
# zenweights.sort()
# errorProbs = [errorProbs[index] for index in indices]
#
# # Print Estimate of Factor Weight Error Distribution
#
# fig,ax = plt.subplots()
# ax.bar(zenweights,errorProbs)
# ax.set_xlim([0,1])
# plt.title('Probability of Error vs. Zenweight')
# plt.xlabel('Zenweight')
# plt.ylabel('Prob. of Error')
# plt.show()
#
# # Save Information
#
# folder = filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','GradientOptimization'))
#
# filename = "ErrorDistribution2.json"
# filepath = os.path.abspath(os.path.join(folder,filename))
# with open(filepath, 'w') as outfile:
#     json.dump(errorProbs, outfile)
#
# filename = "zenweights2.json"
# weights = zenweights.tolist()
# filepath = os.path.abspath(os.path.join(folder,filename))
# with open(filepath, 'w') as outfile:
#     json.dump(weights, outfile)
