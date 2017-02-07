__author__ = 'Justin'

import googlemaps
import networkx as nx
import gmapsKeys
import geojson
import matplotlib.pyplot as plt
from googlemaps import convert
from datetime import datetime
from random import choice
from distance import distance
from geopy.distance import vincenty as latlondist

# DESCRIPTION:
# This script aims to find a more minimalistic network for analysis
# This is done by calling GoogleMaps API services to find the shortest path between randomly selected nodes. The most
# utilized roadways are saved through thresholding. This is more useful than the same process using our network because
# the speed information is not complete and/or not very accurate.
#

# Load Networks from File
fh=open("OSMIntersections.gexf",'rb')
G = nx.read_gexf(fh)
fh.close

fh=open("OSMThreshold.gexf",'rb')
H = nx.read_gexf(fh)
fh.close


print('Num Graph Edges:',len(G.edges()))

nodes = G.nodes()
lons = nx.get_node_attributes(G,'lon')
lats = nx.get_node_attributes(G,'lat')

# Probe Network to find most commonly used roads

maxiter = 0
currentiter = 0
successfuliter = 0

while(currentiter < maxiter):

    # Reset Error Flag
    errorflag = False

    # Choose Random Nodes
    nodesdist = 0
    distancelimit = 3.0

    while(nodesdist < distancelimit):
        randomnodes = [choice(G.nodes()),choice(G.nodes())]
        origin = randomnodes[0]
        destination = randomnodes[1]
        nodesdist = latlondist([lats[origin],lons[origin]],[lats[destination],lons[destination]]).miles

    origin = [lats[randomnodes[0]],lons[randomnodes[0]]]
    destination = [lats[randomnodes[1]],lons[randomnodes[1]]]

    print('Origin',origin)
    print('Destination',destination)

    # Get Google Maps Directions results

    APIkeys = gmapsKeys.keys('keys.txt','keyusages.txt','keydates.txt',2000)
    keystring = APIkeys.getKey()
    APIkeys.updateKey(keystring,1)
    APIkeys.saveKeys()

    now = datetime.now()
    later = datetime(now.year,now.month+1,now.day+1,17,0)

    gmaps = googlemaps.Client(key=keystring)

    try:
        directions_result = gmaps.directions(origin,
                                             destination,
                                             mode="driving",
                                             departure_time=now,
                                             traffic_model = 'best_guess',
                                             alternatives = True)
    except:
        errorflag = True

    if(not errorflag):
        # Extract Path Taken from Results
            # Find midpoint of the path / find network point closest to midpoint / find shortest path from origin
            # to destination through midpoint

        encodedpolyline = directions_result[0]['overview_polyline']['points']
        polyline = convert.decode_polyline(encodedpolyline)

        midindex = (len(polyline)-len(polyline)%2)/2
        midpoint = [polyline[midindex]['lat'],polyline[midindex]['lng']]

        print('Midpoint:',midpoint)

        bestmidnode = []
        bestdist = 1000

        for node in nodes:
            currentnode = [lats[node],lons[node]]
            dist = distance(currentnode,midpoint)
            if(dist < bestdist):
                bestdist = dist
                bestmidnode = node

        print('Closest Node:',bestmidnode)

        try:
            subpath_a = nx.shortest_path(G,source = randomnodes[0],target = bestmidnode,weight = 'basetime')
            subpath_b = nx.shortest_path(G,source = bestmidnode,target = randomnodes[1],weight = 'basetime')
        except:
            errorflag = True

        if(not errorflag):
            usednodes = subpath_a[0:-1]+subpath_b

            # Add usage to all nodes in usednodes

            for somenode in usednodes:
                H.node[somenode]['usage'] = H.node[somenode]['usage'] +1

            successfuliter +=1

    currentiter += 1

# Display Iteration Results

print('Num of Successful Iterations:',successfuliter)
print('Num of Errors',maxiter-successfuliter)


# Generate Histogram of Usage

usagedict = nx.get_node_attributes(H,'usage')
usagevals = usagedict.values()

plt.hist(usagevals,bins = 20)
plt.title("Usage Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()

# Isolate Nodes with High usage

ThreshNodes = []
threshold = 100

for somenode in H.nodes():
    if(H.node[somenode]['usage']>=threshold):
        ThreshNodes.append(somenode)

# Save High Usage Intersections

Hreduced = H.subgraph(ThreshNodes)
nx.write_gexf(Hreduced,'OSMReducedIntersections.gexf')

print('Reduced Network: ',len(Hreduced.nodes()),' Nodes')

# Export Nodes with High usage

lons = nx.get_node_attributes(Hreduced,'lon')
lats = nx.get_node_attributes(Hreduced,'lat')

Features = []
for somenode in ThreshNodes:
    Features.append(geojson.Feature(geometry=geojson.Point((lons[somenode], lats[somenode]))))

Collection = geojson.FeatureCollection(Features)
dump = geojson.dumps(Collection)
string = 'OSMReducedIntersections.txt'
text_file = open(string, "w")
text_file.write(dump)
text_file.close()



