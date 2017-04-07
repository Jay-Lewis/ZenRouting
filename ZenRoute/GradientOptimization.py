__author__ = 'Justin'

import os
import json
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.mlab as mlab


# DESCRIPTION: this script will provide a simulation of the gradient ascent/descent method's performance
#

# Load Characterization from file

# Load Data
cwd = os.getcwd()
folder = filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','GradientOptimization'))

filename = "ErrorDistribution3.json"
filepath = os.path.abspath(os.path.join(folder,filename))
with open(filepath) as data:
    errorProbs = json.load(data)

filename = "zenweights3.json"
filepath = os.path.abspath(os.path.join(folder,filename))
with open(filepath) as data:
    zenweights = json.load(data)

# Plot Data
acceptanceProbs = [1-value for value in errorProbs]
fig,ax = plt.subplots()
ax.plot(zenweights,errorProbs)
ax.set_xlim([0,1])
plt.title('Probability of Error vs. Zenweight')
plt.xlabel('Zenweight')
plt.ylabel('Prob. of Error')
plt.show()

# Assume Distribution on Ideal Weight

# Generate Specific Pr(error|weight) Plot

# Iterative Ascent/Descent Algorithm



# Plot Convergence of Average to Ideal

# Plot Iterations till Convergence vs. Step Size


















# # Normalize
# acceptanceProbs = [1-value for value in errorProbs]
# deltazen = zenweights[1]-zenweights[0]
# norm = np.sum(np.multiply(acceptanceProbs,deltazen))
# print('Initial Area: ',norm)
# areapresent = 0.9
# acceptanceProbs = np.multiply(acceptanceProbs,areapresent/norm)
#
#
# # Plot Data
# fig,ax = plt.subplots()
# ax.plot(zenweights,acceptanceProbs)
# ax.set_xlim([0,1])
# plt.title('Normalized Probability of Acceptance vs. Zenweight')
# plt.xlabel('Zenweight')
# plt.ylabel('Norm. Prob. of Acceptance')

# # Fit Data to Gaussian
# mu = np.sum(np.multiply(np.multiply(acceptanceProbs,deltazen),zenweights))
# print('Mu: ',mu)
# variance = np.sum(np.multiply(np.multiply(np.power(acceptanceProbs,2),deltazen),zenweights))-pow(mu,2)
# print('Var: ',variance)
# sigma = math.sqrt(variance)
# print('Sigma: ',sigma)
#
#
# # Plot Gaussian Fit
# gaussprobs = mlab.normpdf(np.array(zenweights), 0.35, 0.17)
# plt.plot(zenweights,gaussprobs)
#
# norm = np.sum(np.multiply(gaussprobs,deltazen))
# print('Final Area: ',norm)
# mu = np.sum(np.multiply(np.multiply(gaussprobs,deltazen),zenweights))
# print('Approx mu: ',mu)
#
# plt.show()



# # Plot Gaussian Fit
# zenweights = np.linspace(0,0.7,20)
# gaussprobs = mlab.normpdf(np.array(zenweights), 0.4, 0.01)
# plt.plot(zenweights,gaussprobs)
# plt.show()
#
# deltazen = zenweights[1]-zenweights[0]
# norm = np.sum(np.multiply(gaussprobs,deltazen))
# print(norm)
#
# mu = np.sum(np.multiply(np.multiply(gaussprobs,deltazen),zenweights))
# print(mu)
