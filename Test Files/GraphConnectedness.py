__author__ = 'Justin'

import googlemaps
from random import choice
import geojson
import networkx as nx
import math
from datetime import datetime

# Load Network from File
fh=open("Intersections.gexf",'rb')
G = nx.read_gexf(fh)
fh.close

# Generate Strongly Connected Graph

generator = nx.strongly_connected_component_subgraphs(G)

graphs = list(generator)

# Generate Weakly Conneted Graph

generator = nx.weakly_connected_component_subgraphs(G)

graphs = list(generator)

for graph in graphs:
    print(len(graph.edges()))

