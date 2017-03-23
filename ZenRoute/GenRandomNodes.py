__author__ = 'Justin'

import networkx as nx
from random import choice
from geopy.distance import vincenty as latlondist

def randomnodes(G,distancelimit,print_=False):
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

        if(print_):
            print('Source:',[lats[origin],lons[origin]])
            print('Destination',[lats[destination],lons[destination]])

        return origin,destination