__author__ = 'Justin'

from MapLoad import mapload
import os
import networkx as nx
import geojson


# I) Generate Full Network

# DESCRIPTION:
# This script converts geojson road geometry files to a tractable networkx object (.gexf)
# Geojson map data such as node positions, edge connections, edge types, max speeds, and edge names are extracted
# The Geojson network is pruned to remove redundant network nodes.
#
# This reduced load does not include residential sections as part of the core network.
#
# INPUT:
# converted Open Street Map extract (.geojson format)
#
# OUTPUT:
# networkx object file (.gexf)


# Create file path to geojson information
cwd = os.getcwd()
filename = 'cstat_map.geojson'
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Geojson',filename))

# Load Network
restrictedTypes = ['service','track','rail','footway','path','steps',
                   'raceway','unknown','pedestrian','construction','road']

RoadNetwork = mapload(filepath,restrictedTypes)

print("Number of edges:",len(RoadNetwork.edges()))
print("Number of nodes:",len(RoadNetwork.nodes()))

# Save Network Graph
cwd = os.getcwd()
filename = 'OSMNetwork.gexf'
string = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
nx.write_gexf(RoadNetwork,string)

# Export RoadNetwork Nodes (geoJSON format)
Features =[]
lons = nx.get_node_attributes(RoadNetwork,'lon')
lats = nx.get_node_attributes(RoadNetwork,'lat')

for point in RoadNetwork.nodes():
    Features.append(geojson.Feature(geometry=geojson.Point((lons[point], lats[point]))))

Collection = geojson.FeatureCollection(Features)
dump = geojson.dumps(Collection)

filename = 'OSMRoadNetwork.txt'
string = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Display',filename))
text_file = open(string, "w")
text_file.write(dump)
text_file.close()

# Export Edges (geoJSON format)
Features = []

for edge in RoadNetwork.edges():
    pointa = (lons[edge[0]], lats[edge[0]])
    pointb = (lons[edge[1]], lats[edge[1]])
    Features.append(geojson.Feature(geometry=geojson.LineString([pointa,pointb])))

Collection = geojson.FeatureCollection(Features)
dump = geojson.dumps(Collection)

filename = 'OSMEdges.txt'
string = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Display',filename))
text_file = open(string, "w")
text_file.write(dump)
text_file.close()




# II) Generate Reduced Network

# DESCRIPTION:
# This script converts geojson road geometry files to a tractable networkx object (.gexf)
# Geojson map data such as node positions, edge connections, edge types, max speeds, and edge names are extracted
# The Geojson network is pruned to remove redundant network nodes.
#
# This reduced load does not include residential sections as part of the core network.
#
# INPUT:
# converted Open Street Map extract (.geojson format)
#
# OUTPUT:
# networkx object file (.gexf)

# Create file path to geojson information
cwd = os.getcwd()
filename = 'cstat_map.geojson'
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Geojson',filename))

# Load Network
restrictedTypes = ['service','track','residential','living_street','rail','footway','path','steps','cycleway',
                   'raceway','unknown','pedestrian','construction','road']

RoadNetwork = mapload(filepath,restrictedTypes)


print("Number of reduced edges:",len(RoadNetwork.edges()))
print("Number of reduced nodes:",len(RoadNetwork.nodes()))

# Save Network Graph
cwd = os.getcwd()
filename = 'OSMNetworkReduced.gexf'
string = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
nx.write_gexf(RoadNetwork,string)

# Export RoadNetwork Nodes (geoJSON format)
Features =[]
lons = nx.get_node_attributes(RoadNetwork,'lon')
lats = nx.get_node_attributes(RoadNetwork,'lat')

for point in RoadNetwork.nodes():
    Features.append(geojson.Feature(geometry=geojson.Point((lons[point], lats[point]))))

Collection = geojson.FeatureCollection(Features)
dump = geojson.dumps(Collection)

filename = 'OSMRoadNetworkReduced.txt'
string = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Display',filename))
text_file = open(string, "w")
text_file.write(dump)
text_file.close()

# Export Edges (geoJSON format)
Features = []

for edge in RoadNetwork.edges():
    pointa = (lons[edge[0]], lats[edge[0]])
    pointb = (lons[edge[1]], lats[edge[1]])
    Features.append(geojson.Feature(geometry=geojson.LineString([pointa,pointb])))

Collection = geojson.FeatureCollection(Features)
dump = geojson.dumps(Collection)

filename = 'OSMEdgesReduced.txt'
string = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Display',filename))
text_file = open(string, "w")
text_file.write(dump)
text_file.close()
