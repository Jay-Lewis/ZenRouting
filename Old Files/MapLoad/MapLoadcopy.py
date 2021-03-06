__author__ = 'Justin'

import geojson
import networkx as nx
from geopy.distance import vincenty as latlondist


# Load geoJSON strings from file

with open('road data.geojson', 'r') as myfile:
    geoJSONstring=myfile.read().replace('\n', '')
with open('roadspeeds.geojson', 'r') as myfile:
    geoJSONstring2=myfile.read().replace('\n', '')

# Load geoJSON strings into geojson objects
roaddata = geojson.loads(geoJSONstring)
speeddata = geojson.loads(geoJSONstring2)

# Extract Speeds

roadspeeds = {}

for feature in speeddata.features:
    if("maxspeed" in feature.properties and "name" in feature.properties ):
        speedstr = feature.properties["maxspeed"]
        speednum = [int(s) for s in speedstr.split() if s.isdigit()]
        roadspeeds[feature.properties["name"]] = speednum[0]

# Extract nodes and edges
meterconv = 1609.344 # miles to meters

FullGraph = nx.DiGraph()

for feature in roaddata.features:

    # get road edge properties
    if("name" in feature.properties):
        edgename = feature.properties["name"]
        if("name" in roadspeeds):
            speed = roadspeeds[edgename]
            basetime = distance/meterconv/speed*3600
        elif(feature.properties["type"] == 'residential'):
            speed = 20
        else:
            speed = 30
    else:
        edgename = 'unknown'

    # check for oneway vs. twoway streets (twoway streets need two directed edges)
    if(feature.properties["oneway"]== 0 ):
        #add directed edges and associated nodes for feature element
        for latlon in feature.geometry.coordinates:
            FullGraph.add_node(str(latlon),lon =latlon[0] ,lat =latlon[1])
        for counter in range(len(feature.geometry.coordinates)-1,0,-1):
            #find distance between node pair
            distance = meterconv*latlondist(feature.geometry.coordinates[counter],feature.geometry.coordinates[counter-1]).miles
            #add edge with edge properties
            edgedict = {'weight':0,'type':feature.properties["type"],'distance':distance,'basetime':0,'name':edgename}
            FullGraph.add_edge(str(feature.geometry.coordinates[counter]),str(feature.geometry.coordinates[counter-1]),edgedict)

    #add directed edges and associated nodes for feature element (opposite direction of edges within if statement)
    for latlon in feature.geometry.coordinates:
        FullGraph.add_node(str(latlon),lon =latlon[0] ,lat =latlon[1])
    for counter in range(0,len(feature.geometry.coordinates)-1):
        # #find distance between node pair
        # distance = meterconv*latlondist(feature.geometry.coordinates[counter],feature.geometry.coordinates[counter+1]).miles
        # #add edge with distance weight
        # edgedict = {'weight':0,'type':feature.properties["type"],'distance':distance,'basetime':0}
        FullGraph.add_edge(str(feature.geometry.coordinates[counter]),str(feature.geometry.coordinates[counter+1]),edgedict)


# Save FullGraph

nx.write_gexf(FullGraph,'FullGraph.gexf')

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
            edgetype = Intersections[A][node]['type']
            Intersections.add_edge(A,B,weight = weightA_node+weightnode_B, type = edgetype)
            Intersections.add_edge(B,A,weight = weightB_node+weightnode_A, type = edgetype)
            Intersections.remove_node(node)
        else:
            count += 1

    elif(len(neighbors)== 1 and Intersections.degree(node)==2):
        end = neighbors[0]
        start = Intersections.in_edges(node)[0][0]
        weightstart = Intersections[start][node]['weight']
        weightend = Intersections[node][end]['weight']
        edgetype = Intersections[start][node]['type']
        Intersections.add_edge(start,end,weight = weightstart+weightend, type = edgetype)
        Intersections.remove_node(node)


rescount = 0

for edge in Intersections.edges():
    edgedict = Intersections.get_edge_data(edge[0],edge[1])
    if(edgedict['type'] == 'residential'):
        rescount += 1

print('Number of Sections',len(Intersections.edges()))
print('Number of Residential Sections',rescount)


# Save Intersections

nx.write_gexf(Intersections,'Intersections.gexf')

# Export Intersections Nodes (geoJSON format)
Features =[]
lons = nx.get_node_attributes(Intersections,'lon')
lats = nx.get_node_attributes(Intersections,'lat')

for point in Intersections.nodes():
    Features.append(geojson.Feature(geometry=geojson.Point((lons[point], lats[point]))))

Collection = geojson.FeatureCollection(Features)
dump = geojson.dumps(Collection)

text_file = open("Intersections.txt", "w")
text_file.write(dump)
text_file.close()