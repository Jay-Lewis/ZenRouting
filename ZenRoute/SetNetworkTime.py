__author__ = 'Justin'

import os
cwd = os.getcwd()
kd_root= os.path.abspath(os.path.join(cwd, '..', 'Project Data','Keydata'))
import gmapsKeys
import networkx as nx
import googlemaps
from datetime import datetime

# DESCRIPTION: This script will take a neworkx directed graph G and update the given time related attr_key
#
# INPUT: networkx graph
#
# Output: Updated networkx graph

def set_network_time(G,attr_key,time,maxusages):
 
    # Load API Keys
    keys_str = os.path.abspath(os.path.join(kd_root,'keys.txt'))
    keyusages_str = os.path.abspath(os.path.join(kd_root,'keyusages.txt'))
    keydates_str = os.path.abspath(os.path.join(kd_root,'keydates.txt'))
    APIkeys = gmapsKeys.keys(keys_str,keyusages_str,keydates_str,maxusages)
    
    lons = nx.get_node_attributes(G,'lon')
    lats = nx.get_node_attributes(G,'lat')

    # Iterate through all edges and generate travel duration for segment at current 'time'

    for segment in G.edges():

        nodeA = segment[0]
        nodeB = segment[1]
        origin = str(lats[nodeA])+','+str(lons[nodeA])
        destination = str(lats[nodeB])+','+str(lons[nodeB])

        # Create try/exception block to pass over exceptions due to GoogleMaps API server issues
        while True:
            keyname = APIkeys.getKey(usage=1)             #get new key and add one unit of usage
            gmaps = googlemaps.Client(key=keyname)
            try:
                directions_result = gmaps.directions(origin,
                                                     destination,
                                                     mode="driving",
                                                     departure_time=time, traffic_model = 'best_guess')
                duration = directions_result[0]['legs'][0]['duration_in_traffic']['value']  # time in seconds
                break

            except:
                print('------Directions Result Error-------')
                print('Current Key:',keyname)
                print('Current Key Usage:',str(APIkeys.keysdict[keyname].usage))
                print('Current Time and Date:',str(datetime.now()))
                print('Other Keys:')
                APIkeys.printKeys()
                APIkeys.setDefective(keyname,10)
                print('Retrying GoogleMaps API request....')


        # avoid divide by 0 errors
        if duration < 0.1:
            duration = float(0.1)

        # save time duration to edge segment
        G[nodeA][nodeB][attr_key] = float(duration) # must be of type float

    APIkeys.printKeys()
    APIkeys.saveKeys()
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