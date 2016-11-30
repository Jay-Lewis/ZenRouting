__author__ = 'Justin'

import random
import googlemaps
from math import ceil
from random import choice
import geojson
import networkx as nx
from geopy.distance import vincenty as latlondist
from k_shortest_paths import k_shortest_paths
from datetime import datetime



# Load geoJSON string from file

with open('road data.geojson', 'r') as myfile:
    geoJSONstring=myfile.read().replace('\n', '')


# Load string into geojson object
roaddata = geojson.loads(geoJSONstring)


# Extract nodes and edges
meterconv = 1609.344

FullGraph = nx.DiGraph()

for feature in roaddata.features:
    #check for oneway vs. twoway streets (twoway streets need two directed edges)
    if(feature.properties["oneway"]== 0):
        #add directed edges and associated nodes for feature element
        for latlon in feature.geometry.coordinates:
            FullGraph.add_node(str(latlon),lon =latlon[0] ,lat =latlon[1])
        for counter in range(len(feature.geometry.coordinates)-1,0,-1):
            #find distance between node pair
            distance = meterconv*latlondist(feature.geometry.coordinates[counter],feature.geometry.coordinates[counter-1]).miles
            #add edge with distance weight
            FullGraph.add_edge(str(feature.geometry.coordinates[counter]),str(feature.geometry.coordinates[counter-1]),weight=distance )

    #add directed edges and associated nodes for feature element (opposite direction of edges within if statement)
    for latlon in feature.geometry.coordinates:
        FullGraph.add_node(str(latlon),lon =latlon[0] ,lat =latlon[1])
    for counter in range(0,len(feature.geometry.coordinates)-1):
        #find distance between node pair
        distance = meterconv*latlondist(feature.geometry.coordinates[counter],feature.geometry.coordinates[counter+1]).miles
        #add edge with distance weight
        FullGraph.add_edge(str(feature.geometry.coordinates[counter]),str(feature.geometry.coordinates[counter+1]),weight=distance)


# Export Nodes (geoJSON format)
# Features =[]
# lons = nx.get_node_attributes(FullGraph,'lon')
# lats = nx.get_node_attributes(FullGraph,'lat')
#
# for point in FullGraph.nodes():
#     Features.append(geojson.Feature(geometry=geojson.Point((lons[point], lats[point]))))
#
# Collection = geojson.FeatureCollection(Features)
# dump = geojson.dumps(Collection)
#
# text_file = open("AllPoints.txt", "w")
# text_file.write(dump)
# text_file.close()



# Remove Unnecessary nodes (exactly two neighbors or one neighbor and two edges)

Intersections = FullGraph

count = 0
print('Number of Graph Nodes',len(FullGraph.nodes()))

for node in Intersections.nodes():
    neighbors = Intersections.neighbors(node)
    if(len(neighbors)==2):
        A = neighbors[0]
        B = neighbors[1]
        Aneighbors = Intersections.neighbors(A)
        Bneighbors = Intersections.neighbors(B)
        if((node in Aneighbors) and (node in Bneighbors)):
            weightA_node = Intersections[A][node]['weight']
            weightnode_A = Intersections[node][A]['weight']
            weightB_node = Intersections[B][node]['weight']
            weightnode_B = Intersections[node][B]['weight']
            Intersections.add_edge(A,B,weight = weightA_node+weightnode_B)
            Intersections.add_edge(B,A,weight = weightB_node+weightnode_A)
            Intersections.remove_node(node)
        else:
            count += 1

    elif(len(neighbors)== 1 and Intersections.degree(node)==2):
        end = neighbors[0]
        start = Intersections.in_edges(node)[0][0]
        if(len(Intersections.in_edges(node)) == 0):
            print("NOOOOO")
        weightstart = Intersections[start][node]['weight']
        weightend = Intersections[node][end]['weight']
        Intersections.add_edge(start,end,weight = weightstart+weightend)
        Intersections.remove_node(node)


# print('Undeleted Redundant Nodes',count)
# print('Final Number of Graph Nodes',len(FullGraph.nodes()))

# Export Nodes (geoJSON format)
# Features =[]
# lons = nx.get_node_attributes(Intersections,'lon')
# lats = nx.get_node_attributes(Intersections,'lat')
#
# for point in Intersections.nodes():
#     Features.append(geojson.Feature(geometry=geojson.Point((lons[point], lats[point]))))
#
# Collection = geojson.FeatureCollection(Features)
# dump = geojson.dumps(Collection)
#
# text_file = open("Points.txt", "w")
# text_file.write(dump)
# text_file.close()


# Find  k shortest paths

lons = nx.get_node_attributes(Intersections,'lon')
lats = nx.get_node_attributes(Intersections,'lat')

randomnodes = [choice(FullGraph.nodes()),choice(FullGraph.nodes())]

path = nx.shortest_path(FullGraph,source = randomnodes[0],target = randomnodes[1],weight = 'weight')

pathtuple = k_shortest_paths(Intersections,randomnodes[0],randomnodes[1],30)
paths = pathtuple[1]

print('Source:',[lats[randomnodes[0]],lons[randomnodes[0]]])
print('Destination',[lats[randomnodes[1]],lons[randomnodes[1]]])


# Remove Similar Paths
print('Length of Paths:',len(paths))

finalpaths = [] # Eliminate duplicate paths
for path in paths:
    if(not(path in finalpaths)):
        finalpaths.append(path)

paths = finalpaths

for path in paths:
    for j in range(0,paths.index(path)):
        samenodes = 0
        for element in path:
            if(element in paths[j]):
                samenodes +=1
        if(samenodes >= ceil(len(path)/2)):
            paths.remove(path)
            break

elementnum = 0
for element in paths[0]:
    if(element in paths[1]):
        elementnum+=1
        print(element)
print(elementnum)

print('Length of Paths After:',len(paths))


# Export Routes (geoJSON format)
for index, path in enumerate(paths):
    Features = []
    print('Path'+str(index),path)
    for node in path:
        Features.append(geojson.Feature(geometry=geojson.Point((lons[node], lats[node]))))
    Collection = geojson.FeatureCollection(Features)
    dump = geojson.dumps(Collection)
    string = 'Path'+str(index)+'.txt'
    text_file = open(string, "w")
    text_file.write(dump)
    text_file.close()


# Sample Waypoints (max 23 allowed)
# maxwaypoints = 23
#
# for path in paths:
#
#

# Analyze Paths

# Find Congestion and Distances for Each Path

# Pathtimes = []
# Pathtraffictimes = []
# Pathlengths = []
#
# gmaps = googlemaps.Client(key='AIzaSyAVf9cLmfR52ST0VZcFsf-L-HynMTCzZEM')
#
# now = datetime.now()
# later = datetime(now.year,now.month,now.day+1,17,0)
#
# for path in paths:
#     origin = path[0]
#     destination = path[end]
#     waypoints = path[1,end-1]
#     directions_result = gmaps.directions(origin,
#                                          destination,
#                                          mode="driving", waypoints = waypoints,
#                                          departure_time=now, traffic_model = 'best_guess')
#     traveltime = directions_result[0]['legs'][0]['duration']['value']
#     fulltime = directions_result[0]['legs'][0]['duration_in_traffic']['value']  #time in seconds
#     traffictime = fulltime-traveltime   #time in seconds
#     totaldistance = directions_result[0]['legs'][0]['distance']['value']    #distance in meters
#     Pathtimes.append(traveltime)
#     Pathtraffictimes.append(traffictime)
#     Pathlengths.append(totaldistance)
#
# print('Times:',Pathtimes)
# print('Times due to traffic:', Pathtraffictimes)
# print('Path Distance:',Pathlengths)

# Normalize and Weight Data

# Choose Desired Path


# Save Network







# Random Code

# Plot Network

# pos = nx.spring_layout(H)
# nx.draw_networkx(H,pos)
# plt.show()

# Number of Segments

# segments = 0
# for feature in roaddata.features:
#      if(feature.properties["oneway"]== 0):
#         segments += 2*(len(feature.geometry.coordinates)-1)
#      else:
#         segments += len(feature.geometry.coordinates)-1
# print(segments)
# print(len(FullGraph.nodes()))
# print(len(FullGraph.edges()))




