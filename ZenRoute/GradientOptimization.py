__author__ = 'Justin'

import os
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from collections import deque


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

MINweight = zenweights[errorProbs.index(min(errorProbs))]


# Fit to Gaussian
mean = 0.32; std = 0.16     # Experimentally Determined
x_range = np.linspace(0,1,100)
gauss_errorprobs = mlab.normpdf(x_range, mean, std)
MAXgauss_error = max(gauss_errorprobs)
scale = (1.0-min(errorProbs))/max(gauss_errorprobs)
gauss_errorprobs = np.add(np.multiply(gauss_errorprobs,-scale),1.0)


# Plot Data
acceptanceProbs = [1-value for value in errorProbs]
fig,ax = plt.subplots()
ax.plot(zenweights,errorProbs)
ax.plot(x_range,gauss_errorprobs)
ax.set_xlim([0,1])
plt.title('Probability of Error vs. Zenweight')
plt.xlabel('Zenweight')
plt.ylabel('Prob. of Error')
# plt.show()


# Assume Distribution on Ideal Weight
a = 0.1; b = 0.4; average_weight = (b-a)/2.0
randval = np.random.uniform(a,b,1)
shift = randval-MINweight

# Generate Specific Pr(error|weight) Plot

gauss_errorprobs = mlab.normpdf(x_range, mean+shift, std)
scale = (1.0-min(errorProbs))/MAXgauss_error
gauss_errorprobs = np.add(np.multiply(gauss_errorprobs,-scale),1.0)


# Plot Data
fig,ax = plt.subplots()
ax.plot(x_range,gauss_errorprobs)
ax.set_xlim([0,1])
plt.title('Probability of Error vs. Zenweight')
plt.xlabel('Zenweight')
plt.ylabel('Prob. of Error')
# plt.show()



# Iterative Ascent/Descent Algorithm

delta = 0.1
# Initialize
weighthistory = []
wzen = average_weight
randval = np.random.uniform(a,b,1)
shift = randval-MINweight
scale = (1.0-min(errorProbs))/MAXgauss_error
best_weight = mean+shift
maxiter = 1000
threshold = 0.1
MAlen = 20

# Algorithm Loop START
y = []
MAlist = deque([wzen for i in range(0,MAlen,1)])
iter = 0
converged = False
while(not converged and iter < maxiter):
        weighthistory.append(wzen)

        feedback_prob = 1-scale*mlab.normpdf(wzen, mean+shift, std)
        y.append(feedback_prob[0])
        result = np.random.binomial(n=1,p=feedback_prob)

        diff = best_weight-wzen
        sign = np.sign(diff)

        if(wzen <= 0 or wzen >= 1):
            wzen += sign*delta
        else:
            if(result==1):
                wzen += sign*delta
            elif(result==0):
                wzen += sign*-delta
        wzen = wzen[0]

        MAlist.appendleft(np.mean(weighthistory))
        MAlist.pop()

        # Check for Convergence
        converged = True
        for value in list(MAlist):
            test = abs(value-best_weight)/best_weight < threshold
            converged = converged and test
        iter += 1



# Plot Wzen Changes
gauss_errorprobs = mlab.normpdf(x_range, mean+shift, std)
scale = (1.0-min(errorProbs))/MAXgauss_error
gauss_errorprobs = np.add(np.multiply(gauss_errorprobs,-scale),1.0)
fig,ax = plt.subplots()
ax.plot(x_range,gauss_errorprobs)
ax.plot(weighthistory,y)
ax.set_xlim([0,1])
plt.title('Zen Weight Changes')
plt.xlabel('Zenweight')
plt.ylabel('Prob. of Error')
# plt.show()

# Plot Convergence of Average to Ideal
averages = []
for index in range(0,len(weighthistory),1):
    average = np.mean(weighthistory[0:index+1])
    averages.append(average)

fig,ax = plt.subplots()
ax.plot(range(0,len(averages)),averages)
ax.plot(range(0,len(averages)),[best_weight for i in range(0,len(averages))] )
plt.title('Ascent / Descent Algorithm')
plt.xlabel('Iteration')
plt.ylabel('Lambda Estimation')
plt.show()







# Iterative Ascent/Descent Algorithm (Sweep Deltas)
if(False):
    AVGiters = []
    deltas = np.linspace(0.03,.22,20)
    for delta in deltas:

        numtrials = 50
        iters = []

        for _ in range(0,numtrials,1):

            # Initialize
            weighthistory = []
            wzen = average_weight
            randval = np.random.uniform(a,b,1)
            shift = randval-MINweight
            scale = (1.0-min(errorProbs))/MAXgauss_error
            best_weight = mean+shift
            maxiter = 1000
            threshold = 0.1
            MAlen = 5

            # Algorithm Loop START
            y = []
            MAlist = deque([wzen for i in range(0,MAlen,1)])
            iter = 0
            converged = False
            while(not converged and iter < maxiter):
                    weighthistory.append(wzen)

                    feedback_prob = 1-scale*mlab.normpdf(wzen, mean+shift, std)
                    y.append(feedback_prob[0])
                    result = np.random.binomial(n=1,p=feedback_prob)

                    diff = best_weight-wzen
                    sign = np.sign(diff)

                    if(wzen <= 0 or wzen >= 1):
                        wzen += sign*delta
                    else:
                        if(result==1):
                            wzen += sign*delta
                        elif(result==0):
                            wzen += sign*-delta
                    wzen = wzen[0]

                    MAlist.appendleft(np.mean(weighthistory))
                    MAlist.pop()

                    # Check for Convergence
                    converged = True
                    for value in list(MAlist):
                        test = abs(value-best_weight)/best_weight < threshold
                        converged = converged and test
                    iter += 1
            if(iter != 0 and iter != 1000 and iter != 1):
                iters.append(iter)
            # else:
            #     iters.append(maxiter)
        print('Delta',delta)
        print(iters)
        AVGiters.append(np.mean(iters))

    # Plot Iterations till Convergence vs. Step Size

    fig,ax = plt.subplots()
    ax.plot(deltas,AVGiters)
    plt.show()





















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
#
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
# gaussprobs = mlab.normpdf(np.array(zenweights), 0.32, 0.17)
# # gaussprobs = mlab.normpdf(np.array(zenweights), mu, sigma)
# plt.plot(zenweights,gaussprobs)
#
# norm = np.sum(np.multiply(gaussprobs,deltazen))
# print('Final Area: ',norm)
# mu = np.sum(np.multiply(np.multiply(gaussprobs,deltazen),zenweights))
# print('Approx mu: ',mu)
#
# plt.show()