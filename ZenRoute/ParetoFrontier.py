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
from GenRandomNodes import randomnodes
import matplotlib.pyplot as plt
import numpy as np

# DESCRIPTION: This script will generate the approx. Pareto Frontier for randomized source and destination


def rand_paretofront(G,weights,factorkeys,min,max,unique_key):

        numunique = 0

        # Search until enough points found for random source and destination
        while(numunique not in range(min,max+1,1)):

            # Generate Random Nodes
            origin,destination = randomnodes(G,distancelimit=1)       # distancelimit in miles

            pathsinfo = []
            paths = []

            for weight in weights:

                # Update Total Edge Weights
                factorweights = [weight,1-weight]
                for edge in G.edges():
                    nodeA = edge[0]
                    nodeB = edge[1]
                    dict = G[nodeA][nodeB]
                    G[nodeA][nodeB]['weight'] = weightfunction(factorweights,dict,factorkeys)

                # Djkistra's Shortest Path
                path = nx.shortest_path(G,source = origin,target = destination,weight = 'weight')

                # Get Path Information
                path_dict = routeinfo(G,path,factorkeys)

                paths.append(path)
                pathsinfo.append(path_dict)

            values = [dict[unique_key] for dict in pathsinfo]
            numunique=np.unique(values).size

        # Get clustered weights based on uniqueness
        weight_cluster = cluster_weights(weights,pathsinfo,unique_key)

        # Save only unique paths and associated information
        _,indices = np.unique(pathsinfo,return_index=True)
        pathsinfo = [pathsinfo[index] for index in np.sort(indices)]

        _,indices = np.unique(paths,return_index=True)
        paths = [paths[index] for index in np.sort(indices)]

        return weight_cluster, paths, pathsinfo


def cluster_weights(weights,pathsinfo,unique_key):

    values = [dict[unique_key] for dict in pathsinfo]
    uniquevalues = np.unique(values)
    weight_cluster = []

    for value in uniquevalues:
        indices = [i for i,dictionary in enumerate(pathsinfo) if dictionary[unique_key]==value]
        subcluster = [weights[index] for index in indices]
        weight_cluster.append(subcluster)

    return list(reversed(weight_cluster))












# Example Code

if(False):

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

    ratios = []
    numiterations = 3
    for i in range(0,numiterations,1):

        # Loop Until Enough Pareto Optimal Points Found

        numunique = 0
        numParetoOptimal = 2
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
            zenweights = np.linspace(0,1,numpts)
            for zenweight in zenweights:

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
        print(min(time_pts))
        MIN = min(time_pts)
        time_pts[:]=[value/MIN for value in time_pts]   # Normalize time to minimum value
        ax.scatter(Zenscore_pts,time_pts,s=10)
        arr,unique_indices = np.unique(Zenscore_pts,return_index=True)

        for index in unique_indices:
            ax.annotate(annotations[index],(Zenscore_pts[index],time_pts[index]))

        # Plot weight point of interest
        index2 = int(1*len(Zenscore_pts)/4)
        print(zenweights[index2])
        ax.scatter(Zenscore_pts[index2],time_pts[index2],s=100,color = 'r',alpha=0.2)
        ratios.append(Zenscore_pts[index2]/time_pts[index2])

        plt.xlabel('Zenscores')
        plt.ylabel('Times (Normalized to Fastest Path)')
        plt.ylim([0,3])
        plt.xlim([0,2200])

    # Show All Graphs at Once
    plt.show()
    plt.close("all")

    # Plot Histogram of Zen/Time Ratio for a specific value of Wzen
    fig,ax = plt.subplots()
    ax.hist(ratios)
    plt.xlabel('Ratio')
    plt.ylabel('Frequency')
    plt.title('Histogram of Zen/Time Ratio for Wzen = '+str(zenweights[index2]))
    plt.show()

    # IV) Plot Network and Routes
    # routestyles = [{'color':' #ccffcc','width':12}]       # greenish
    # zenMAX = max(nx.get_edge_attributes(G,'Zenness').values())
    # networkdisplay(G,routes=[path],graphstyle='RdYlBu_r',routestyles = routestyles,
    #                weightstring='Zenness',maxValue=zenMAX, title='Example')