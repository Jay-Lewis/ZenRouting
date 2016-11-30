__author__ = 'Justin'

import googlemaps
from random import choice
import geojson
import networkx as nx
import math
from datetime import datetime
import gmapsKeys
from geopy.distance import vincenty as latlondist

# Load API Keys

APIkeys = gmapsKeys.keys('keys.txt','keyusages.txt','keydates.txt',2500)

key = APIkeys.getKey()
APIkeys.updateKey(key,10)
APIkeys.saveKeys()

print('Given Key',key)

# Load Network from File
fh=open("OSMIntersections.gexf",'rb')
G = nx.read_gexf(fh)
fh.close

print('Number of Graph Nodes',len(G.nodes()))
print('Number of Graph Edges',len(G.edges()))

# Set Network Edge Weights

# for edgetuple in G.edges():
#     G[edgetuple[0]][edgetuple[1]]['weight'] = G[edgetuple[0]][edgetuple[1]]['basetime']

# Find k Unique Routes

k = 5
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


H = G   # Make copy of Network
subgraphnodes = []
paths = []
times = []

for i in range(0,k,1):
    path = nx.shortest_path(H,source = randomnodes[0],target = randomnodes[1],weight = 'weight')
    pathsubgraph = G.subgraph(path)
    time = nx.shortest_path_length(pathsubgraph,path[0],path[-1],weight = 'basetime')
    times.append(time)
    paths.append(path)
    subgraphnodes.extend(path)
    mid = int(math.floor(len(path)/2))
    delta = int(math.floor(len(path)/6))
    H.remove_nodes_from(path[mid-delta:mid+delta])

# Print Paths
for path,time in zip(paths,times):
    print(path)
    print('Path Time:',time,'(s)')

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


# Sample Waypoints from Paths (max 23 allowed)
numwaypoints = 3
sampledpaths = []

for path in paths:
    if len(path)>numwaypoints:
        newpath = []
        for i in range(1,len(path),len(path)/numwaypoints):
            string = ('via:'+'%.5f' % lats[path[i]]) + ',' + ('%.5f' % lons[path[i]])
            newpath.append(string)
        if ~(destination in newpath):
            string = ('%.5f' % lats[destination]) + ',' + ('%.5f' % lons[destination])
            newpath.append(string)
        string = ('%.5f' % lats[origin]) + ',' + ('%.5f' % lons[origin])
        newpath.insert(0,string)
        sampledpaths.append(newpath)


# Analyze Paths

# Find Congestion and Distances for Each Path

Pathbasetimes = []
Pathfulltimes = []
Pathtraffictimes = []
Pathlengths = []

gmaps = googlemaps.Client(key='AIzaSyAVf9cLmfR52ST0VZcFsf-L-HynMTCzZEM')

now = datetime.now()

for path in sampledpaths:
    origin = path[0]
    destination = path[-1]
    waypoints = path[1:-1]
    directions_result = gmaps.directions(origin,
                                         destination,
                                         mode="driving", waypoints = waypoints,
                                         departure_time=now, traffic_model = 'best_guess')
    # traveltime = directions_result[0]['legs'][0]['duration']['value']
    fulltime = directions_result[0]['legs'][0]['duration_in_traffic']['value']  #time in seconds
    # traffictime = fulltime-traveltime   #time in seconds
    totaldistance = directions_result[0]['legs'][0]['distance']['value']    #distance in meters
    # Pathbasetimes.append(traveltime)
    # Pathtraffictimes.append(traffictime)
    Pathfulltimes.append(fulltime)
    Pathlengths.append(totaldistance)

later = datetime(now.year,now.month,now.day+1,4,0)

for path in sampledpaths:
    origin = path[0]
    destination = path[-1]
    waypoints = path[1:-1]
    directions_result = gmaps.directions(origin,
                                         destination,
                                         mode="driving", waypoints = waypoints,
                                         departure_time=later, traffic_model = 'best_guess')
    basetime = directions_result[0]['legs'][0]['duration_in_traffic']['value']  #time in seconds
    Pathbasetimes.append(basetime)

for full,base in zip(Pathfulltimes,Pathbasetimes):
    traffictime = full-base
    Pathtraffictimes.append(traffictime)


print('Times:',Pathbasetimes)
print('Times due to traffic:', Pathtraffictimes)
print('Path Distance:',Pathlengths)
