__author__ = 'Justin'

import random
import geojson
import networkx as nx
import itertools

Graph = nx.DiGraph()

nodes = ['A','B','C','D','E','F','G']

Graph.add_edge('A','B',weight = 1,test = 1)
Graph.add_edge('A','C',weight = 2, test = 3)
Graph.add_edge('C','A',weight = 2, test = 3)
Graph.add_edge('B','A',weight = 2)

edges = Graph.edges()

print(Graph.get_edge_data(edges[1][0],edges[1][1]))

neighborsA = Graph.neighbors('A')
neighborsB = Graph.neighbors('B')
neighborsC = Graph.neighbors('C')
print('A Neighbors:',neighborsA)
print('B Neighbors:',neighborsB)
print('C Neighbors:',neighborsC)
print('Degree A:',Graph.degree('A'))
print('Degree B:',Graph.degree('B'))

print('A Edges',Graph.edges('A'))

print(type(Graph.in_edges('A')))
print(Graph.in_edges('A')[0][0])
print(Graph.out_edges('A'))

Graph.add_node('T',{'lat':1.2})
print(Graph.node['T']['lat'])

# remove unnecessary nodes
#
# for node in Graph.nodes():
#     neighbors = Graph.neighbors(node)
#     if(len(neighbors)==2):
#         A = neighbors[0]
#         B = neighbors[1]
#         weightA_node = Graph[A][node]['weight']
#         weightnode_A = Graph[node][A]['weight']
#         weightB_node = Graph[B][node]['weight']
#         weightnode_B = Graph[node][B]['weight']
#         Graph.add_edge(A,B,weight = weightA_node+weightnode_B)
#         Graph.add_edge(B,A,weight = weightB_node+weightnode_A)
#         Graph.remove_node(node)
#
#     elif(len(neighbors)== 1 and Graph.degree(node)==2):
#         end = neighbors[0]
#         start = Graph.in_edges(node)[0][0]
#         weightstart = Graph[start][node]['weight']
#         weightend = Graph[node][end]['weight']
#         Graph.add_edge(start,end,weight = weightstart+weightend)
#         Graph.remove_node(node)
#
#
# print('NewGraph',Graph.edges())
# print('BCweight',Graph['B']['C']['weight'])
# print('CBweight',Graph['C']['B']['weight'])

print('-----------------')

for edgetuple in Graph.edges():
    test = Graph[edgetuple[0]][edgetuple[1]]['weight']
    print(test)

# neighbors = Graph.neighbors('A')
# permutations = itertools.permutations(neighbors)
# for i in permutations:
#     print(i)
# for i in permutations:
#     print(i)
# for node in Graph.nodes():
#     neighbors = Graph.neighbors(node)
#     permutations = itertools.permutations(neighbors)
#     print(permutations)


# print('NewGraph',Graph.edges())
# print('BCweight',Graph['B']['C']['weight'])
# print('CBweight',Graph['C']['B']['weight'])






# from random import choice
#
# randomnodes = [choice(Graph.nodes()),choice(Graph.nodes())]
#
# path = nx.shortest_path(Graph,source = 'A',target = 'C',weight = 'weight')
#
# print(path)
#
#
# # Save and Load Network
#
# nx.write_gexf(Graph,'test.gexf')
#
# fh=open("test.gexf",'rb')
# H = nx.read_gexf(fh)
# fh.close
#
#
# weights = nx.get_edge_attributes(H,'weight')
# test = nx.get_edge_attributes(H,'test')
# print(weights)
# print(test)