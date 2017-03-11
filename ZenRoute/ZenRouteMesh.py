__author__ = 'Justin'

import os
import networkx as nx
from datetime import datetime
from SetNetworkTime import set_network_time
from WeightFunction import weightfunction
from ZenScore import zenscore
from random import choice
from geopy.distance import vincenty as latlondist
import geojson
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


# DESCRIPTION: This script will generate the ideal ZenRoute based on a user's desired factor weights
#
# INPUT: factor weights- [a,b,c] corresponding to [Zenness, time, distance] and updated network graph
#
# OUTPUT: ZenRoute (as a networkx object or geojson output)


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

# Generate Zenness metric
for edge in G.edges():
    nodeA = edge[0]
    nodeB = edge[1]

    G[nodeA][nodeB]['Zenness'] = zenscore(G[nodeA][nodeB])

# Generate Source and Destination Nodes
distancelimit = 3   # distance in miles

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

# Djkistra's Shortest Path
# Note: weights are varied over grid of values
paths = {}

distanceweight = 0
for Zenweight in range(0,100,5):
    for timeweight in range(0,100,5):

        weights = [Zenweight,distanceweight,timeweight]
        keys = ['Zenness','distance','currenttime']
        for edge in G.edges():
            nodeA = edge[0]
            nodeB = edge[1]
            dict = G[nodeA][nodeB]
            G[nodeA][nodeB]['weight'] = weightfunction(weights,dict,keys)

        # Save Network Graph
        # filename = "OSMNetworkReducedSet.gexf"
        # filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
        # nx.write_gexf(G,filepath)

        path = tuple(nx.shortest_path(G,source = randomnodes[0],target = randomnodes[1],weight = 'weight'))

        if path in paths.keys():
             paths[path].append((Zenweight,timeweight))
        else:
            paths[path] = [(Zenweight,timeweight)]


# Plot Decision Regions
colors = np.random.random((len(paths.keys()), 3))
patches = []
keyorder = []
fig, ax = plt.subplots()

for index,key in enumerate(paths.keys()):
    list = paths[key]
    x,y = zip(*list)
    color = colors[index]
    plt.scatter(x,y,s=100,facecolors=color)
    patch = mpatches.Patch(color=color, label='Path'+str(index)+'.txt')
    patches.append(patch)
    keyorder.append(key)

plt.legend(handles=patches,bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
ax.set_xlabel('Zenweights')
ax.set_ylabel('Timeweights')
plt.show()


# Export Routes (geoJSON format)
for index, path in enumerate(keyorder):
    Features = []
    print('Path'+str(index),path)
    for node in path:
        Features.append(geojson.Feature(geometry=geojson.Point((lons[node], lats[node]))))
    Collection = geojson.FeatureCollection(Features)
    dump = geojson.dumps(Collection)
    filename = 'Path'+str(index)+'.txt'
    filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Paths',filename))
    text_file = open(filepath, "w")
    text_file.write(dump)
    text_file.close()

# Export Source and Destination
    Features = []
    for node in randomnodes:
        Features.append(geojson.Feature(geometry=geojson.Point((lons[node], lats[node]))))
    filename = 'Origin_Dest.txt'
    filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Paths',filename))
    text_file = open(filepath, "w")
    Collection = geojson.FeatureCollection(Features)
    dump = geojson.dumps(Collection)
    text_file.write(dump)
    text_file.close()