__author__ = 'Justin'


import networkx as nx
import geojson


# Load Networks from File
fh=open("OSMIntersections.gexf",'rb')
G = nx.read_gexf(fh)
fh.close

fh=open("IntersectionsReduced.gexf",'rb')
G2 = nx.read_gexf(fh)
fh.close

fh=open("OSMReducedIntersections.gexf",'rb')
G3 = nx.read_gexf(fh)
fh.close


# Find corresponding node in G from node in G2 (node naming difference due to different sources)

lons = nx.get_node_attributes(G,'lon')
lats = nx.get_node_attributes(G,'lat')

lons2 = nx.get_node_attributes(G2,'lon')
lats2 = nx.get_node_attributes(G2,'lat')



print(type(lons))

# Combine All Reduced Graphs


N1 = G2.nodes()
N2 = G3.nodes()
N3 = N1+N2

print(N1[0],N2[0])

print('N3 Length:',len(N3))

print('Total Num Nodes:',len(G.nodes()))
print('N1 Length:',len(N1))
print('N2 Length:',len(N2))

FinalReducedGraph = G.subgraph(N3)

count = 0
print('Number of Graph Nodes',len(FinalReducedGraph.nodes()))

for node in FinalReducedGraph.nodes():
    neighbors = FinalReducedGraph.neighbors(node)
    if(len(neighbors)==2):
        A = neighbors[0]
        B = neighbors[1]
        Aneighbors = FinalReducedGraph.neighbors(A)
        Bneighbors = FinalReducedGraph.neighbors(B)
        if((node in Aneighbors) and (node in Bneighbors)):
            weightA_node = FinalReducedGraph[A][node]['weight']
            weightnode_A = FinalReducedGraph[node][A]['weight']
            weightB_node = FinalReducedGraph[B][node]['weight']
            weightnode_B = FinalReducedGraph[node][B]['weight']
            FinalReducedGraph.add_edge(A,B,weight = weightA_node+weightnode_B)
            FinalReducedGraph.add_edge(B,A,weight = weightB_node+weightnode_A)
            FinalReducedGraph.remove_node(node)
        else:
            count += 1

    elif(len(neighbors)== 1 and FinalReducedGraph.degree(node)==2):
        end = neighbors[0]
        start = FinalReducedGraph.in_edges(node)[0][0]
        weightstart = FinalReducedGraph[start][node]['weight']
        weightend = FinalReducedGraph[node][end]['weight']
        FinalReducedGraph.add_edge(start,end,weight = weightstart+weightend)
        FinalReducedGraph.remove_node(node)

print('Number of Reduced Nodes:',len(FinalReducedGraph.nodes()))

# Export Final Nodes

lons = nx.get_node_attributes(FinalReducedGraph,'lon')
lats = nx.get_node_attributes(FinalReducedGraph,'lat')

Features = []
for somenode in FinalReducedGraph.nodes():
    # if(FinalReducedGraph.node[somenode]['usage']>=threshold):
    Features.append(geojson.Feature(geometry=geojson.Point((lons[somenode], lats[somenode]))))

Collection = geojson.FeatureCollection(Features)
dump = geojson.dumps(Collection)
string = 'FinalReducedIntersections.txt'
text_file = open(string, "w")
text_file.write(dump)
text_file.close()

