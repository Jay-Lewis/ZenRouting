
import os
cwd = os.getcwd()
kd_root= os.path.abspath(os.path.join(cwd, '..', 'Project Data','Keydata'))
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from numpy import mean
import networkx as nx


# Print Histogram of Zen Scores

# Load Network
cwd = os.getcwd()
filename = "OSMNetworkReducedSet.gexf"
filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
fh=open(filepath,'rb')
G = nx.read_gexf(fh)


fig,ax = plt.subplots()
zenscores = nx.get_edge_attributes(G,'Zenness').values()
# hist = numpy.histogram(values)
zenrange = [0,800]
ax.hist(zenscores,range=zenrange,bins = 50)
plt.title('Zenscore Histogram')
plt.xlabel('Zenscore')
plt.ylabel('Probability')
plt.show()




# Print Justin and Pablo's User Weights

weights = [0.55, 0.5, 0.55, 0.6000000000000001, 0.55, 0.55, 0.5, 0.45, 0.4, 0.4, 0.45, 0.45, 0.45, 0.5, 0.5, 0.45, 0.45, 0.5, 0.55, 0.55, 0.5, 0.55, 0.5, 0.5, 0.45, 0.45, 0.4, 0.4, 0.45, 0.5, 0.5, 0.5, 0.55, 0.55]
plt.plot(range(1,len(weights)+1,1),weights)
plt.xlabel('Iteration')
plt.ylabel('Zen Weight')
pablo_avg = mean(weights[5:-1])


weights = [0.55, 0.55, 0.6000000000000001, 0.55, 0.6000000000000001, 0.6500000000000001, 0.7000000000000002, 0.6500000000000001, 0.6000000000000001, 0.6500000000000001, 0.7000000000000002, 0.6500000000000001, 0.6500000000000001, 0.6000000000000001, 0.6000000000000001, 0.6500000000000001, 0.7000000000000002, 0.6500000000000001, 0.6000000000000001, 0.6000000000000001, 0.6500000000000001, 0.6000000000000001, 0.6500000000000001, 0.6500000000000001, 0.6000000000000001, 0.6000000000000001, 0.6500000000000001, 0.7000000000000002, 0.6500000000000001, 0.6500000000000001, 0.7000000000000002, 0.6500000000000001, 0.6000000000000001, 0.6000000000000001, 0.6500000000000001]
plt.plot(range(1,len(weights)+1,1),weights)
plt.xlabel('Iteration')
plt.ylabel('Zen Weight')
plt.title("Weight Regression")
justin_avg = mean(weights[5:-1])

pablo_patch = mpatches.Patch(color='blue', label="Pablo")
justin_patch = mpatches.Patch(color='green', label='Justin')
plt.legend(handles = [pablo_patch,justin_patch])

plt.plot(range(1,len(weights)+1,1),[pablo_avg for x in range(1,len(weights)+1,1)],'--',color='#737373')
plt.plot(range(1,len(weights)+1,1),[justin_avg for x in range(1,len(weights)+1,1)],'--',color='#737373')

plt.show()

