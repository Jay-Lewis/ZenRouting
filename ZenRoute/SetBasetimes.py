__author__ = 'Justin'

import os
import networkx as nx
from SetNetworkTime import set_network_time
from datetime import datetime

# DESCRIPTION:
# This script generates the 'basetime' traffic time duration
# The 'basetime' is generated at a time during which traffic is minimal (3-4 am for example)


# Create file path to geojson information
cwd = os.getcwd()
filename = "OSMNetworkReduced.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))

fh=open(filepath,'rb')
G = nx.read_gexf(fh)
fh.close

now = datetime.now()
later = datetime(now.year,now.month,now.day+1,4,0)
H = set_network_time(G,'basetime',later,2000)

# Save Network Graph
filename = "OSMNetworkReduced.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
nx.write_gexf(H,filepath)


