
import os
from os.path import isfile, join
cwd = os.getcwd()
kd_root= os.path.abspath(os.path.join(cwd, '..', 'Project Data','Keydata'))
import gmapsKeys
import networkx as nx
import googlemaps
from datetime import datetime
from datetime import timedelta
from DisplayNetwork import networkdisplay



cwd = os.getcwd()
folderpath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks','CstatHistory'))
files = [f for f in os.listdir(folderpath) if isfile(join(folderpath, f))]
print(files)
for filename in files:
    filepath = os.path.abspath(os.path.join(cwd,folderpath,filename))
    fh2=open(filepath,'rb')
    H = nx.read_gexf(fh2)
    networkdisplay(H,[],'RdYlBu_r',[])
    fh2.close













# start = datetime.now()+timedelta(seconds=15)
# hours = 1
# iterations = 1
# end = start+timedelta(hours=hours*iterations+hours/2.0)
# print(float(hours*iterations)+hours/2.0)
# print(str(start))
# print(str(end))
#
# filename = "OSMNetworkReducedSet.gexf"
# filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
# fh2=open(filepath,'rb')
# H = nx.read_gexf(fh2)
# edge = H.edges()[3]
# print(H[edge[0]][edge[1]]['currenttime'])
#
# cwd = os.getcwd()
# folderpath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks','CstatHistory'))
# files = [f for f in os.listdir(folderpath) if isfile(join(folderpath, f))]
# print(files)
# for filename in files:
#     filepath = os.path.abspath(os.path.join(cwd,folderpath,filename))
#     fh2=open(filepath,'rb')
#     H = nx.read_gexf(fh2)
#     edge = H.edges()[3]
#     print(H[edge[0]][edge[1]]['currenttime'])
#     fh2.close











# Way in which to grab the time from filename
# datestring = "0-27(8-3-2017)"
# myDate = datetime.strptime(datestring,"%H-%M(%d-%m-%Y)")
# print(myDate)

# maxusages = 10
#
# # Load API Keys
# keys_str = os.path.abspath(os.path.join(kd_root,'keys.txt'))
# keyusages_str = os.path.abspath(os.path.join(kd_root,'keyusages.txt'))
# keydates_str = os.path.abspath(os.path.join(kd_root,'keydates.txt'))
# APIkeys = gmapsKeys.keys(keys_str,keyusages_str,keydates_str,maxusages)
#
# for i in range(0,5):
#     newkey = APIkeys.getKey(1)
#     print(newkey)
#
# APIkeys.setDefective(newkey,5)
# print('defective key',newkey)
#
# for i in range(0,10):
#     newkey = APIkeys.getKey(1)
#     print(newkey)









# __author__ = 'Justin'
#
# import os
# import networkx as nx
#
# # Load Network
# cwd = os.getcwd()
# filename = "OSMNetworkReduced.gexf"
# filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
# print(filepath)
#
# fh=open(filepath,'rb')
# G = nx.read_gexf(fh)
# fh.close
#
# cwd = os.getcwd()
# filename = "OSMNetwork.gexf"
# filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
# print(filepath)
#
# fh=open(filepath,'rb')
# H = nx.read_gexf(fh)
# fh.close
#
#
# print(len(G.nodes()))
#
# print(len(H.nodes()))







import matplotlib.lines as lines
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
# fig, ax = plt.subplots()
#
# fig.set_size_inches(6,6)          # Make graph square
# plt.scatter([-0.1],[-0.1],s=0.01)     # Move graph window a little left and down
#
# line1 = [(0,0), (1,0)]
# line2 = [(0,0), (0,1)]
#
# # Note that the Line2D takes a list of x values and a list of y values,
# # not 2 points as one might expect.  So we have to convert our points
# # an x-list and a y-list.
# (line1_xs, line1_ys) = zip(*line1)
# (line2_xs, line2_ys) = zip(*line2)
#
# ax.add_line(Line2D(line1_xs, line1_ys, linewidth=2, color='blue'))
# ax.add_line(Line2D(line2_xs, line2_ys, linewidth=2, color='red'))
#
# print(line1_xs)
# print(line1_ys)
# plt.plot()
# plt.show()

