
import os
import matplotlib.pyplot as plt
import networkx as nx
import json
import numpy as np
import matplotlib.patches as mpatches
from scipy.stats import beta
import scipy.integrate as integrate
import scipy.special as special


result = np.random.binomial(n=1,p=1)
print(result)
print(type(result))


# Beta Distribution
alpha = 2.0
a = 3; b = 10;
beta_param = np.random.uniform(a,b,1)

randvals = beta.rvs(alpha, beta_param, size=10)
exp_mean = float(np.mean(randvals))
beta_param_hat = alpha/exp_mean-alpha

print(beta_param)
print(beta_param_hat)

def integrand(x,a,b):
    return 2.0/(2.0+x)/abs(b-a)

test = integrate.quad(integrand, a, b,args =(a,b))[0]
print(test)








# # Load Network
# cwd = os.getcwd()
# filename = "OSMNetworkReducedSet.gexf"
# filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
# fh=open(filepath,'rb')
# G = nx.read_gexf(fh)
#
# numweights = 20
# weights = np.linspace(0,1,numweights)
# numunique = 3
# rand_paretofront(G,weights,['Zenness','currenttime'],numunique,'Zenness')


# # Print Legend for Plot
#
# list = ['#ffff4d','#66ff66','#00cd00','#008b00']
# names = ['[0.00-0.42]','[0.47-0.79]','[0.84-1.00]']
#
# patches = []
# for color,name in zip(list,names):
#     patch = mpatches.Patch(color=color, label=name)
#     patches.append(patch)
# plt.legend(handles = patches)
# plt.show()
#
#
#
#
# # Print Graph of Gradient Optimization
#
# # Load Data
# cwd = os.getcwd()
# folder = filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','GradientOptimization','Justin'))
#
# filename = "ErrorDistribution.json"
# filepath = os.path.abspath(os.path.join(folder,filename))
# with open(filepath) as data:
#     errorProbs = json.load(data)
#
# filename = "zenweights.json"
# filepath = os.path.abspath(os.path.join(folder,filename))
# with open(filepath) as data:
#     zenweights = json.load(data)
#
# # Resort Data
#
# print(zenweights)
# print(errorProbs)
# indices = np.argsort(np.array(zenweights))
# zenweights.sort()
# errorProbs = [errorProbs[index] for index in indices]
#
# # Plot Data
#
# fig,ax = plt.subplots()
# ax.plot(zenweights,np.multiply(errorProbs,35.0/35.0))
# ax.set_xlim([0,1])
# plt.title('Probability of Error vs. Zenweight')
# plt.xlabel('Zenweight')
# plt.ylabel('Prob. of Error')
# plt.show()
#
#
#
#
#
# # Print Bar Graph of Gradient Optimization
#
# # Load Data
# cwd = os.getcwd()
# folder = filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','GradientOptimization'))
#
# filename = "ErrorDistribution3.json"
# filepath = os.path.abspath(os.path.join(folder,filename))
# with open(filepath) as data:
#     errorProbs = json.load(data)
#
# filename = "zenweights3.json"
# filepath = os.path.abspath(os.path.join(folder,filename))
# with open(filepath) as data:
#     zenweights = json.load(data)
#
# # Resort Data
#
# print(zenweights)
# print(errorProbs)
# indices = np.argsort(np.array(zenweights))
# zenweights.sort()
# errorProbs = [errorProbs[index] for index in indices]
#
# # Plot Data
#
# fig,ax = plt.subplots()
# ax.plot(zenweights,errorProbs)
# ax.set_xlim([0,1])
# plt.title('Probability of Error vs. Zenweight')
# plt.xlabel('Zenweight')
# plt.ylabel('Prob. of Error')
# plt.show()
#
#
#
#
# # Print Histogram of Zen Scores
#
# # Load Network
# cwd = os.getcwd()
# filename = "OSMNetworkReducedSet.gexf"
# filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','Networks',filename))
# fh=open(filepath,'rb')
# G = nx.read_gexf(fh)
#
#
# fig,ax = plt.subplots()
# zenscores = nx.get_edge_attributes(G,'Zenness').values()
# # hist = numpy.histogram(values)
# zenrange = [0,800]
# ax.hist(zenscores,range=zenrange,bins = 50)
# plt.title('Zenscore Histogram')
# plt.xlabel('Zenscore')
# plt.ylabel('Probability')
# plt.show()





