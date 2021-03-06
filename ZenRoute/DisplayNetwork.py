__author__ = 'Justin'

import os
import matplotlib.pyplot as plt
from plotly.graph_objs import *
import networkx as nx
from plotly.offline import  plot
from plotly.graph_objs import Scatter, Figure, Layout
import matplotlib.patches as mpatches

# Convert RGB tuple to hex
def rgb_to_hex(rgb):
    return '#'+str('%02x%02x%02x' % rgb)

# DESCRIPTION: This function will display a snapshot of a traffic network. Edges and nodes are plotted by extracting
# latitude and longitude data from the loaded networkx directed graphs.
#
# Edges and nodes are plotted with color in order to display the associated "zenness" metric associated with each. Edge
# color is directly related to the "zenness" on that edge. Node color is related to the average value of zenness of
# neighboring edges
#
# Inputs: Networkx graph objects G and H. The first graph, G, is
#
# Outpus:

def networkdisplay(G,routes,graphstyle,routestyles,weightstring,normValue,title):

    # I) -Generate Network 'G' Graphical Data--------------------

    # Get Color Map
    colormap = plt.get_cmap(graphstyle)

    # Get Node Positions
    pos=nx.get_node_attributes(G,'pos')
    dmin=1
    ncenter=0
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d

    # Generate Lines for Graph Edges
    edge_traces = []
    for edge in G.edges():
        x0 = G.node[edge[0]]['lon']
        y0 = G.node[edge[0]]['lat']
        x1 = G.node[edge[1]]['lon']
        y1 = G.node[edge[1]]['lat']
        weight = G[edge[0]][edge[1]][weightstring]/normValue
        if(weight > 1.0):
            weight = 1.0
        rgb = tuple([int(value*255) for value in colormap(weight)[0:3]])
        hexstring = rgb_to_hex(rgb)

        edge_trace = Scatter(
        x=(x0, x1),
        y=(y0, y1),
        line=Line(
            width=1.0,
            reversescale=True,
            color=hexstring,
            ),
        hoverinfo='none',
        # text = str(weight),
        # mode='lines+text')
        mode = 'lines')
        edge_traces.append(edge_trace)

    # Generate Markers for Graph Nodes
    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=Marker(
            showscale=True,
            colorscale=graphstyle,
            reversescale=False,
            color='#e8e8e8',
            size=10,
            colorbar=dict(
                thickness=15,
                title=weightstring+'Metric',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in G.nodes():

        # Positional Information
        x = G.node[node]['lon']
        y = G.node[node]['lat']
        node_trace['x'].append(x)
        node_trace['y'].append(y)

        # weight Information
        approx_weight = 0
        neighbors = G.neighbors(node)
        if(len(neighbors)>0):
            for neighbor in neighbors:
                subweight = G[node][neighbor][weightstring]/normValue
                if(subweight > 1.0):
                    subweight=1.0
                approx_weight += subweight
            approx_weight = approx_weight/len(neighbors)
        # node_trace['marker']['color'].append(approx_weight)
        node_info = 'Approx. '+weightstring+':'+str(approx_weight)
        # node_trace['text'].append(node_info)


    # II) -Generate Route Graphical Data--------------------
    route_traces = []

    for route,routestyle in zip(routes,routestyles):
        # Create graphical data for each route
        route_trace = Scatter(
        x=[],
        y=[],
        line=Line(
            width=routestyle['width'],
            color=routestyle['color'],
            ),
        hoverinfo='none',
        mode='lines')

        for nodeA, nodeB in zip(route,route[1:]):
            x0 = G.node[nodeA]['lon']
            y0 = G.node[nodeA]['lat']
            x1 = G.node[nodeB]['lon']
            y1 = G.node[nodeB]['lat']
            route_trace['x']+=([x0,x1,None])
            route_trace['y']+=([y0,y1,None])
        route_traces.append(route_trace)


    # zoom to routes
    lons = nx.get_node_attributes(G,'lon')
    lats = nx.get_node_attributes(G,'lat')
    sublons =[]
    sublats = []

    for route in routes:
        for node in route:
            sublons.append(lons[node])
            sublats.append(lats[node])

    if(len(routes)>0):
        xmin = min(sublons)-.005; xmax = max(sublons)+.005
        ymin = min(sublats)-.005; ymax = max(sublats)+.005
        x_range = [xmin,xmax]
        y_range = [ymin,ymax]
    else:
        x_range = []
        y_range = []


    # III) -Plot All Graphical Data--------------------
    graphicalData = route_traces+[node_trace]+edge_traces
    # graphicalData = route_traces+edge_traces
    fig = Figure(data=Data(graphicalData),
                 layout=Layout(
                    title='<br>'+title,
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code:",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False,range=x_range),
                    yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False,range=y_range)))

    # # Plot Legend
    # patches = []
    # for routestyle in routestyles:
    #     patch = mpatches.Patch(color=routestyle['color'], label=routestyle['name'])
    #     patches.append(patch)
    # plt.legend(handles = patches)

    plot(fig, filename='networkx.html')


#
# # Load Network
# cwd = os.getcwd()
# filename = "OSMNetworkReducedSet.gexf"
# filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
# fh=open(filepath,'rb')
# G = nx.read_gexf(fh)
# fh.close
# filename = "OSMNetwork.gexf"
# filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
# fh=open(filepath,'rb')
# H = nx.read_gexf(fh)
# fh.close
#
# from numpy import std
# Zen_std = std(nx.get_edge_attributes(G,'Zenness').values())
# networkdisplay(G,[],'RdYlBu_r',[],'Zenness',Zen_std,'Zen Score Validation')





# -----------------------------------------------------------------------------------------------------------
# DESCRIPTION: code below is left in order to use the display operation on a more complex example
set = 0

if set == 1:
    # Load Network
    cwd = os.getcwd()
    filename = "OSMNetworkReducedSet.gexf"
    filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
    fh=open(filepath,'rb')
    G = nx.read_gexf(fh)
    fh.close
    filename = "OSMNetwork.gexf"
    filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
    fh=open(filepath,'rb')
    H = nx.read_gexf(fh)
    fh.close

    # Plot Network

    # Get Node Positions
    pos=nx.get_node_attributes(G,'pos')

    dmin=1
    ncenter=0
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d


    # Create Edges

    # Color Map
    # good color options: ['YlOrRd','RdYlGn_r','RdYlBu_r','coolwarm','hist_heat_r','reds','greens','blues']
    colormaptype = 'RdYlBu_r'
    colormap = plt.get_cmap(colormaptype)

    # Normalize Zenness
    maxZenscore = 0
    for edge in G.edges():
        if(G[edge[0]][edge[1]]['Zenness'] > maxZenscore):
            maxZenscore = G[edge[0]][edge[1]]['Zenness']

    city_trace = Scatter(
    x=[],
    y=[],
    line=Line(
        width=0.5,
        reversescale=True,
        color='#a6a6a6',
        ),
    hoverinfo='none',
    mode='lines')

    for edge in H.edges():
        x0 = H.node[edge[0]]['lon']
        y0 = H.node[edge[0]]['lat']
        x1 = H.node[edge[1]]['lon']
        y1 = H.node[edge[1]]['lat']
        city_trace['x']+=([x0,x1,None])
        city_trace['y']+=([y0,y1,None])


    edge_traces = []

    for edge in G.edges():
        x0 = G.node[edge[0]]['lon']
        y0 = G.node[edge[0]]['lat']
        x1 = G.node[edge[1]]['lon']
        y1 = G.node[edge[1]]['lat']
        zenness = G[edge[0]][edge[1]]['Zenness']
        rgb = tuple([int(value*255) for value in colormap(zenness/maxZenscore)[0:3]])
        hexstring = rgb_to_hex(rgb)

        edge_trace = Scatter(
        x=(x0, x1),
        y=(y0, y1),
        line=Line(
            width=1.2,
            reversescale=True,
            color=hexstring,
            ),
        hoverinfo='none',
        mode='lines')
        edge_traces.append(edge_trace)


    node_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=Marker(
            showscale=True,
            # colorscale options
            # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
            # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
            colorscale=colormaptype,
            reversescale=False,
            color='#e8e8e8',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Normalized Zenness Metric',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in G.nodes():
        x = G.node[node]['lon']
        y = G.node[node]['lat']
        node_trace['x'].append(x)
        node_trace['y'].append(y)

    # Color Node Points

    for node in G.nodes():
        zenness = 0
        approx_zenness = 0
        neighbors = G.neighbors(node)
        if(len(neighbors)>0):
            for neighbor in neighbors:
                zenness += G[node][neighbor]['Zenness']/maxZenscore
            approx_zenness = zenness/len(neighbors)
        # node_trace['marker']['color'].append(approx_zenness)
        node_info = 'Approx. Zenness: '+str(approx_zenness)
        node_trace['text'].append(node_info)

    # from numpy import multiply
    # MAXvalue = max(node_trace['marker']['color'])
    # node_trace['marker']['color'] = multiply(node_trace['marker']['color'],1.0/MAXvalue)

    # Plot Network Graph

    fig = Figure(data=Data([city_trace,node_trace]+edge_traces),
                 layout=Layout(
                    title='<br>Zen Score Validation',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="Python code:",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

    plot(fig, filename='networkx.html')

