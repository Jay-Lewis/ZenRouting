__author__ = 'Justin'

import geojson
import networkx as nx
import DefaultRoadSpeed as DRS
from geopy.distance import vincenty as latlondist

# DESCRIPTION:
# This script converts geojson road geometry file to a tractable networkx object (.gexf)
# Geojson map data such as node positions, edge connections, edge types, max speeds, and edge names are extracted
# The Geojson network is pruned to remove redundant network nodes. Roads of a restricted type are not included.
#
# INPUT:
# a) filepath to geojson file (string)
# b) restricted road types (list)
#
# OUTPUT:
# networkx object file (.gexf)



def mapload(filepath,restrictedTypes):

    # Load geoJSON strings into geojson objects
    with open(filepath, 'r') as myfile:
        geoJSONstring=myfile.read().replace('\n', '')
    roaddata = geojson.loads(geoJSONstring)

    # Extract nodes and edges
    meterconv = 1609.344 # miles to meters

    FullGraph = nx.DiGraph()

    for feature in roaddata.features:
        # Check if feature is a road
        if(feature.geometry['type'] == "LineString"):

            # get road edge properties
            edgename = feature.properties.get("name",'unknown')
            edgetype = feature.properties.get("highway",'unknown')
            oneway = feature.properties.get("oneway",'unknown')
            speedstr = feature.properties.get("maxspeed",'unknown')

            # obtain default speed (mph) if unknown
            if(speedstr == 'unknown'):
                speed = DRS.getdefaultspeed(speedstr)
            else:
                speednums = [int(s) for s in speedstr.split() if s.isdigit()]
                speed = speednums[0]

            # check for restricted road types or odd cases (road is restricted but important)
            if((edgetype not in restrictedTypes) or (speed >= 35 )):

                # check for oneway vs. twoway streets (twoway streets need two directed edges)
                if(oneway != 'yes'):
                    #add directed edges and associated nodes for feature element
                    for latlon in feature.geometry.coordinates:
                        FullGraph.add_node(str(latlon),lon =latlon[0] ,lat =latlon[1],usage = 0)
                    for counter in range(len(feature.geometry.coordinates)-1,0,-1):
                        #find distance between node pair
                        distance = meterconv*latlondist(feature.geometry.coordinates[counter],feature.geometry.coordinates[counter-1]).miles
                        #add edge with edge properties
                        basetime = distance/meterconv/speed*3600.0
                        edgedict = {'weight':0,'type':edgetype,'distance':distance,'basetime':basetime,'name':edgename,
                                    'Zenness':0,'currenttime':0}
                        FullGraph.add_edge(str(feature.geometry.coordinates[counter]),str(feature.geometry.coordinates[counter-1]),edgedict)

                #add directed edges and associated nodes for feature element (opposite direction of edges within if statement)
                for latlon in feature.geometry.coordinates:
                    FullGraph.add_node(str(latlon),lon =latlon[0] ,lat =latlon[1],usage = 0)
                for counter in range(0,len(feature.geometry.coordinates)-1):
                    #find distance between node pair
                    distance = meterconv*latlondist(feature.geometry.coordinates[counter],feature.geometry.coordinates[counter+1]).miles
                    #add edge with distance weight
                    basetime = distance/meterconv/speed*3600.0
                    edgedict = {'weight':0,'type':edgetype,'distance':distance,'basetime':basetime,'name':edgename,
                                'Zenness':0,'currenttime':0}
                    FullGraph.add_edge(str(feature.geometry.coordinates[counter]),str(feature.geometry.coordinates[counter+1]),edgedict)

    # Remove Unnecessary nodes (exactly two neighbors or one neighbor and two edges)

    Intersections = FullGraph

    for node in Intersections.nodes():
        neighbors = Intersections.neighbors(node)
        if(len(neighbors)==2):
            A = neighbors[0]
            B = neighbors[1]
            Aneighbors = Intersections.neighbors(A)
            Bneighbors = Intersections.neighbors(B)
            if((node in Aneighbors) and (node in Bneighbors)):
                basetimeA_node = Intersections[A][node]['basetime']
                basetimenode_A = Intersections[node][A]['basetime']
                basetimeB_node = Intersections[B][node]['basetime']
                basetimenode_B = Intersections[node][B]['basetime']

                distanceA_node = Intersections[A][node]['distance']
                distancenode_A = Intersections[node][A]['distance']
                distanceB_node = Intersections[B][node]['distance']
                distancenode_B = Intersections[node][B]['distance']

                edgedataAB = Intersections.get_edge_data(A,node)
                edgedataBA = Intersections.get_edge_data(B,node)

                edgedataAB['basetime'] = basetimeA_node+basetimenode_B
                edgedataBA['basetime'] = basetimeB_node+basetimenode_A

                edgedataAB['distance'] = distanceA_node+distancenode_B
                edgedataBA['distance'] = distanceB_node+distancenode_A

                Intersections.add_edge(A,B,attr_dict=edgedataAB)
                Intersections.add_edge(B,A,attr_dict=edgedataBA)
                Intersections.remove_node(node)

        elif(len(neighbors)== 1 and Intersections.degree(node)==2):
            end = neighbors[0]
            start = Intersections.in_edges(node)[0][0]

            basetimestart = Intersections[start][node]['basetime']
            basetimeend = Intersections[node][end]['basetime']
            distancestart = Intersections[start][node]['distance']
            distanceend = Intersections[node][end]['distance']

            edgedata = Intersections.get_edge_data(start,node)
            edgedata['basetime'] = basetimestart+basetimeend
            edgedata['distance'] = distancestart+distanceend

            Intersections.add_edge(start,end,edgedata)
            Intersections.remove_node(node)

    return Intersections
