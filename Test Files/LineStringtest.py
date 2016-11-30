__author__ = 'Justin'

__author__ = 'Justin'

import random
from random import choice
import geojson
import networkx as nx
from geopy.distance import vincenty as latlondist
import matplotlib.pyplot as plt



# Load geoJSON string from file

with open('road data.geojson', 'r') as myfile:
    geoJSONstring=myfile.read().replace('\n', '')


# Load string into geojson object
roaddata = geojson.loads(geoJSONstring)


# Extract nodes and edges
meterconv = 1609.344

Graph = nx.DiGraph()
Graph = nx.Graph()

for feature in roaddata.features:

    #Add feature nodes
    lonlat = feature.geometry.coordinates[0]
    Graph.add_node(str(lonlat),lon =lonlat[0] ,lat =lonlat[1])
    lonlat = feature.geometry.coordinates[-1]
    Graph.add_node(str(lonlat),lon =lonlat[0] ,lat =lonlat[1])

    #Calculate feature length
    distance = 0
    for counter in range(0,len(feature.geometry.coordinates)-1,1):
        #find distance between latlon pair
        distance += latlondist(feature.geometry.coordinates[counter],feature.geometry.coordinates[counter+1]).miles

    #check for oneway vs. twoway streets (twoway streets need two directed edges)
    if(feature.properties["oneway"]== 0):
        #add directede edge with distance weight
        Graph.add_edge(str(feature.geometry.coordinates[-1]),str(feature.geometry.coordinates[0]),weight=distance )
    #add directed edge with distance weight (opposite direction of edge within if statement)
    Graph.add_edge(str(feature.geometry.coordinates[0]),str(feature.geometry.coordinates[-1]),weight=distance )


# Find shortest paths

randomnodes = [choice(Graph.nodes()),choice(Graph.nodes())]
print(randomnodes[0],randomnodes[1])

print(len(Graph.nodes()))
num = nx.number_connected_components(Graph)
print("Num Connected:")
print(num)

# path = nx.shortest_path(Graph,source = randomnodes[0],target = randomnodes[1],weight = 'weight')
# print(len(path))
#
# #Find length of a path
# totaldistance = 0
#
# for counter in range(0,len(path)-1):
#     totaldistance += latlondist(path[counter], path[counter+1]).miles
#
# print(totaldistance)


#Export Nodes
# Features =[]
# lons = nx.get_node_attributes(Graph,'lon')
# lats = nx.get_node_attributes(Graph,'lat')
#
# for node in Graph.nodes():
#     # Features.append(geojson.Feature(lons[node],lats[node]))
#     Features.append(geojson.Feature(geometry=geojson.Point((lons[node], lats[node]))))
#
# Collection = geojson.FeatureCollection(Features)
# dump = geojson.dumps(Collection)
#
# text_file = open("Points.txt", "w")
# text_file.write(dump)
# text_file.close()

