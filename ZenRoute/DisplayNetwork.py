__author__ = 'Justin'

import os
import matplotlib.pyplot as plt
from plotly.graph_objs import *
import networkx as nx
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import Scatter, Figure, Layout

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

def networkdisplay(G,routes,graphstyle,routestyles,weightstring,maxValue,title):

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
        zenness = G[edge[0]][edge[1]][weightstring]
        rgb = tuple([int(value*255) for value in colormap(zenness/maxValue)[0:3]])
        hexstring = rgb_to_hex(rgb)

        edge_trace = Scatter(
        x=(x0, x1),
        y=(y0, y1),
        line=Line(
            width=0.75,
            reversescale=True,
            color=hexstring,
            ),
        hoverinfo='none',
        text = str(zenness),
        mode='lines+text')
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
            color=[],
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

        # Zenness Information
        zenness = 0
        approx_zenness = 0
        neighbors = G.neighbors(node)
        if(len(neighbors)>0):
            for neighbor in neighbors:
                zenness += G[node][neighbor][weightstring]/maxValue
            approx_zenness = zenness/len(neighbors)
        node_trace['marker']['color'].append(approx_zenness)
        node_info = 'Approx. '+weightstring+':'+str(approx_zenness)
        node_trace['text'].append(node_info)


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
                    xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

    plot(fig, filename='networkx.html')








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
        color='#a9a9a9',
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
            width=0.5,
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
            color=[],
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
        node_trace['marker']['color'].append(approx_zenness)
        node_info = 'Approx. Zenness: '+str(approx_zenness)
        node_trace['text'].append(node_info)

    # Plot Network Graph

    fig = Figure(data=Data([city_trace,node_trace]+edge_traces),
                 layout=Layout(
                    title='<br>Zen Route Example',
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