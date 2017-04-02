__author__ = 'Justin'

from datetime import timedelta
from SetNetworkTime import set_network_time
from WeightFunction import weightfunction
from ZenScore import zenscore
from apscheduler.schedulers.blocking import BlockingScheduler
import os
cwd = os.getcwd()
kd_root= os.path.abspath(os.path.join(cwd, '..', 'Project Data','Keydata'))
import networkx as nx
from datetime import datetime

import logging
logging.basicConfig()

def updatenetwork(G,setTime,setZen,setWeight,weights,folderpath,maxusages):
    print('---------------Beginning Iteration------------------------ ')
    print(str(datetime.now()))
    # Update Time Segments
    if setTime:
        now = datetime.now()
        G = set_network_time(G,'currenttime',now,maxusages)

    # Update "Zenness"
    if setZen:
        for edge in G.edges():
            nodeA = edge[0]
            nodeB = edge[1]

            G[nodeA][nodeB]['Zenness'] = zenscore(G[nodeA][nodeB])

    if setWeight:
        # Update Total Edge Weights
        keys = ['Zenness','distance','currenttime']
        for edge in G.edges():
            nodeA = edge[0]
            nodeB = edge[1]
            dict = G[nodeA][nodeB]
            G[nodeA][nodeB]['weight'] = weightfunction(weights,dict,keys)

    # Save Network Graph
    now = datetime.now()
    filename = str(now.hour)+'-'+str(now.minute)+'('+str(now.day)+'-'+str(now.month)+'-'+str(now.year)+').gexf'
    filepath = os.path.abspath(os.path.join(folderpath,filename))
    # G.graph['datetime']=now   #for some reason datetime is lost in writing
    nx.write_gexf(G,filepath)
    print('---------------Successful Iteration------------------------ ')
    print(str(datetime.now()))



def periodicupdate(period,start,end,G,weights,folderpath,maxusages):
    scheduler = BlockingScheduler()
    scheduler.add_job(updatenetwork, 'interval', seconds=period,start_date=start, end_date=end,
                      args = [G,True,True,True,weights,folderpath,maxusages])
    scheduler.start()



# Load Network
cwd = os.getcwd()
filename = "OSMNetworkReducedSet.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
fh=open(filepath,'rb')
G = nx.read_gexf(fh)
fh.close


# Periodic Network Load
folderpath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks','CstatHistory'))
weights = [1,1,1]
maxusages = 1000
hours = 1
period = hours*3600     # time in seconds
start = datetime.now()+timedelta(seconds = 40)
print('Scheduled Start Time:',str(start))
iterations = 1
end = start+timedelta(hours=hours*iterations+hours/2.0)
print('--------Beginning Periodic Update------------')
periodicupdate(period,start,end,G,weights,folderpath,maxusages)


