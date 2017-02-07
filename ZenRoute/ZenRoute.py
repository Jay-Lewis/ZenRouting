__author__ = 'Justin'

import os
import networkx as nx
from datetime import datetime
from SetNetworkTime import set_network_time
from WeightFunction import weightfunction
from ZenScore import zenscore
from random import choice
from geopy.distance import vincenty as latlondist

# DESCRIPTION: This script will generate the ideal ZenRoute based on a user's desired factor weights
#
# INPUT: factor weights- [a,b,c] corresponding to [Zenness, time, distance]
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

# Generate Weighted Sum of Factors
weights = [1,1,1]
keys = ['Zenness','distance','currenttime']
for edge in G.edges():
    nodeA = edge[0]
    nodeB = edge[1]
    dict = G[nodeA][nodeB]
    G[nodeA][nodeB]['weight'] = weightfunction(weights,dict,keys)

# Save Network Graph
filename = "OSMNetworkReducedSet.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
nx.write_gexf(G,filepath)


# Djkistra's Shortest Path
distancelimit = 3

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


# Export Route