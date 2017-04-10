__author__ = 'Justin'

import os
import sys
import json
import networkx as nx
from numpy import std,linspace,argsort,array,linspace,unique
from DisplayNetwork import networkdisplay
from ParetoFrontier import rand_paretofront
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from os.path import isfile, join
from datetime import datetime
import random

# DESCRIPTION: Generate Estimate of Factor Weight Error Distribution
#

# Initialize data
numweights = 30
weights = linspace(0,1,numweights)
weightchosen = {weight:0 for weight in weights}
uniquerange = [3,5]
numiter = 35

print('Enter your first name: ')
person = sys.stdin.readline()[0:-1]

# Load Networks

Graphs = []
cwd = os.getcwd()
folderpath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks','CstatHistory'))
files = [f for f in os.listdir(folderpath) if isfile(join(folderpath, f))]
for filename in files:
    filepath = os.path.abspath(os.path.join(cwd,folderpath,filename))
    fh=open(filepath,'rb')
    G = nx.read_gexf(fh)
    fh.close

    myDate = datetime.strptime(filename,"%H-%M(%d-%m-%Y).gexf")
    G.graph['datetime']=myDate
    Graphs.append(G)

for _ in range(0,numiter,1):

    # Generate Pareto Frontier
    Gchosen = random.choice(Graphs)
    cluster_weights, paths, pathsinfo = rand_paretofront(Gchosen,weights,['Zenness','currenttime'],
                                                         uniquerange[0],uniquerange[1],'Zenness')


    # Print Route Information
    print('------------------------------------------------------------------------------')
    print('/////////////////////////////////////////////////////////////////////////////')
    Zenscore_pts = []
    time_pts = []
    for index,path in enumerate(paths):
        print('---------------------------------------')
        print('Route '+str(index)+':')
        print('-time(min):',pathsinfo[index]['currenttime']/60)
        print('-zenness:',pathsinfo[index]['Zenness'])
        print('----------------')
        print('-zen diff:',pathsinfo[0]['Zenness']-pathsinfo[index]['Zenness'])
        print('-time diff:',(pathsinfo[index]['currenttime']-pathsinfo[0]['currenttime'])/60)
        print('---------------------------------------')
        Zenscore_pts.append(pathsinfo[index]['Zenness'])
        time_pts.append(pathsinfo[index]['currenttime']/60)


    # Plot All Route Options
    routestyles=[]
    listcolors = ['#cc9999','#ccff99','#999933','#ffcc99','#996633','#767777']
    # listcolors = ['#ffff4d','#66ff66','#00cd00','#008b00','#006400','#cc9999','#ccff99','#999933']

    patches = []
    for index,color in enumerate(listcolors):
        patch = mpatches.Patch(color=color, label='Route '+str(index))
        patches.append(patch)
    # plt.legend(handles = patches)
    # plt.show()

    for index in range(0,len(paths),1):
        dict = {'color': listcolors[index],'width': 10,'name': 'Route '+str(index)+':'}
        routestyles.append(dict)

    Zen_std = std(nx.get_edge_attributes(Gchosen,'Zenness').values())
    networkdisplay(Gchosen,routes=paths,graphstyle='RdYlBu_r',routestyles = routestyles,
                   weightstring='Zenness',normValue=6.0*Zen_std, title='Pareto Optimal Routes')

    # # Plot Pareto Frontier
    # fig,ax = plt.subplots()
    # MIN = min(time_pts)
    # time_pts[:]=[value/MIN for value in time_pts]   # Normalize time to minimum value
    # ax.scatter(Zenscore_pts,time_pts,s=10)
    # plt.title('Pareto Frontier Example')
    # plt.xlabel('Zenscores')
    # plt.ylabel('Time Normalized to Fastest Route')
    # plt.show()
    #
    # for index,weightgroup in enumerate(cluster_weights):
    #     if(len(weightgroup)==1):
    #         a = "%.2f" % weightgroup[0]
    #         ax.annotate('['+a+']',(Zenscore_pts[index],time_pts[index]))
    #     else:
    #         a = "%.2f" % weightgroup[0]
    #         b = "%.2f" % weightgroup[-1]
    #         ax.annotate('['+a+'-'+b+']',(Zenscore_pts[index],time_pts[index]))





    # Get User Feedback:
    print('Options:')
    print('Enter list of acceptable routes separated by commas')
    print('Route indicated by number 0-'+str(len(paths)-1)+'')
    print('Example => 1,2,3')
    print('OR')
    print("'s' for skip  and  'r' for refine:")
    string = sys.stdin.readline()
    if(string[0] != 'r' and string[0] != 's'):
        chosenindices = [int(element) for index,element in enumerate(string) if(index % 2 == 0) ]



    if(string[0] == 'r'):
        # Prune Options:
        print('Options:')
        print('Enter list separated by commas of choices to view')
        print('Example => 1,2,3')
        string = sys.stdin.readline()
        chosenindices = [int(element) for index,element in enumerate(string) if(index % 2 == 0) ]
        print('Chosen:',chosenindices)


        # Plot All Chosen Options
        routestyles=[]
        for index in chosenindices:
            dict = {'color': listcolors[index],'width': 10,'name': 'Route '+str(index)+':'}
            routestyles.append(dict)

        chosenpaths = [paths[i] for i in chosenindices]
        chosenpathinfos = [paths[i] for i in chosenindices]

        Zen_std = std(nx.get_edge_attributes(Gchosen,'Zenness').values())
        networkdisplay(Gchosen,routes=chosenpaths,graphstyle='RdYlBu_r',routestyles = routestyles,
                       weightstring='Zenness',normValue=6.0*Zen_std, title='Pareto Optimal Routes')

        # Get Refined User Feedback:
        print('Options:')
        print('Enter list of acceptable routes separated by commas')
        print('Route indicated by number 0-'+str(len(paths)-1)+'')
        print('Example => 1,2,3')
        print('OR')
        print("'s' for skip  and  'r' for refine:")
        string = sys.stdin.readline()
        if(string[0] != 'r' and string[0] != 's'):
            chosenindices = [int(element) for index,element in enumerate(string) if(index % 2 == 0) ]



    if(string[0] != 's'):
        # Save contribution to weight error distribution
        for chosenindex in chosenindices:
            for weight in cluster_weights[chosenindex]:
                weightchosen[weight] += 1

print(chosenindices)

# Print Estimate of Factor Weight Error Distribution

fig,ax = plt.subplots()
x = sorted(weightchosen.keys())
y = [1.0-float(weightchosen[key])/float(numiter) for key in x]
ax.bar(x,y)
ax.set_xlim([0,1])
plt.title('Probability of Error vs. Zenweight')
plt.xlabel('Zenweight')
plt.ylabel('Prob. of Error')
plt.show()

# Save Information

folder = filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','GradientOptimization',person))

filename = "ErrorDistribution.json"
filepath = os.path.abspath(os.path.join(folder,filename))
with open(filepath, 'w') as outfile:
    json.dump(y, outfile)

filename = "zenweights.json"
filepath = os.path.abspath(os.path.join(folder,filename))
with open(filepath, 'w') as outfile:
    json.dump(x, outfile)

