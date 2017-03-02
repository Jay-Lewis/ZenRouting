__author__ = 'Justin'

import os
cwd = os.getcwd()
kd_root= os.path.abspath(os.path.join(cwd, '..', 'Project Data','Keydata'))
import gmapsKeys
import networkx as nx
import googlemaps

# DESCRIPTION: This script will take a neworkx directed graph G and update
#
# INPUT: networkx graph
#
# Output: Updated networkx graph

def set_network_time(G,attr_key,time,usages):
 
    # Load API Keys
    keys_str = os.path.abspath(os.path.join(kd_root,'keys.txt'))
    keyusages_str = os.path.abspath(os.path.join(kd_root,'keyusages.txt'))
    keydates_str = os.path.abspath(os.path.join(kd_root,'keydates.txt'))
    APIkeys = gmapsKeys.keys(keys_str,keyusages_str,keydates_str,usages)
    
    lons = nx.get_node_attributes(G,'lon')
    lats = nx.get_node_attributes(G,'lat')

    # Iterate through all edges and generate travel duration for segment at current 'time'

    for segment in G.edges():

        key = APIkeys.getKey(1)
        gmaps = googlemaps.Client(key=key)
    
        nodeA = segment[0]
        nodeB = segment[1]
        origin = str(lats[nodeA])+','+str(lons[nodeA])
        destination = str(lats[nodeB])+','+str(lons[nodeB])
    
        directions_result = gmaps.directions(origin,
                                             destination,
                                             mode="driving",
                                             departure_time=time, traffic_model = 'best_guess')
        duration = directions_result[0]['legs'][0]['duration_in_traffic']['value']  # time in seconds
        print(duration)

        # avoid divide by 0 errors
        if duration < 0.1:
            duration = float(0.1)

        # save time duration to edge segment
        G[nodeA][nodeB][attr_key] = float(duration) # must be of type float
        print(duration)

    return G

# SetNetwork Example

# # Create file path to geojson information
# cwd = os.getcwd()
# filename = "OSMReducedIntersections.gexf"
# filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
#
# fh=open(filepath,'rb')
# G = nx.read_gexf(fh)
# fh.close
#
# set_network_time(G,'basetime',datetime.now())