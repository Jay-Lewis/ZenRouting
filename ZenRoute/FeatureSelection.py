__author__ = 'Justin'


import os
import json
import networkx as nx
import numpy as np
from GetRouteInfo import routeinfo
import matplotlib.pyplot as plt

person = 'Justin2'

# Load Data
cwd = os.getcwd()
folder = os.path.abspath(os.path.join(cwd, '..', 'Project Data','UserWeights',person))

filename = 'PathOptions'
filepath = os.path.abspath(os.path.join(folder,filename))
with open(filepath) as json_data:
    PathOptions = json.load(json_data)

filename = 'Choices'
filepath = os.path.abspath(os.path.join(folder,filename))
with open(filepath) as json_data:
    Choices = json.load(json_data)

filename = "OSMNetworkReducedSet.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))

fh=open(filepath,'rb')
G = nx.read_gexf(fh)
fh.close

# Format Data
y = []
X = []

for index,choice in enumerate(Choices):
    if(choice == '1'):      # Zen Chosen
        y.append(1)
    elif(choice == '2'):    # Fastest Chosen
        y.append(0)

    if(choice == '1' or choice == '2'):
        zenRoute = PathOptions[index]['Zen']
        fastestRoute = PathOptions[index]['Fast']

        zenRouteInfo = routeinfo(G,zenRoute,['currenttime','Zenness'])
        fastestRouteInfo = routeinfo(G,fastestRoute,['currenttime','Zenness'])

        ZenDiff = (fastestRouteInfo['Zenness']-zenRouteInfo['Zenness'])/fastestRouteInfo['Zenness']
        TimeDiff = (zenRouteInfo['currenttime']-fastestRouteInfo['currenttime'])/zenRouteInfo['currenttime']
        X.append([ZenDiff,TimeDiff])

# Plot Data
fig,ax = plt.subplots()

for pt,choice in zip(X,y):

    if(choice == 1):
        ax.scatter(pt[0],pt[1],color='r')
    elif(choice == 0):
        ax.scatter(pt[0],pt[1],color='b')
plt.xlabel('Normalized ZenDiff')
plt.ylabel('Normalized TimeDiff')

fig,ax = plt.subplots()

for pt,choice in zip(X,y):

    if(choice == 1):
        ax.scatter(pow(pt[0],2),pt[1],color='r')
    elif(choice == 0):
        ax.scatter(pow(pt[0],2),pt[1],color='b')

plt.xlabel('Normalized ZenDiff')
plt.ylabel('Normalized TimeDiff')

fig,ax = plt.subplots()

for pt,choice in zip(X,y):

    if(choice == 1):
        ax.scatter(pt[0]/pt[1],0,color='r')
    elif(choice == 0):
        ax.scatter(pt[0]/pt[1],0,color='b')

plt.xlabel('Normalized ZenDiff / TimeDiff')
plt.ylabel('Unused')

# Plot all at once
plt.show()
