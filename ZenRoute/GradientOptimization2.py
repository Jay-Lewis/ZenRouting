__author__ = 'Justin'

import os
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from collections import deque
import scipy.integrate as integrate
from scipy.stats import beta


# DESCRIPTION: this script will provide a simulation of the gradient ascent/descent method's performance
#


# I)------Fit Experimentally Determined Error vs. ZenWeight Curve-----------------------------------------------
#

# Load Characterization from file

# Load Data
cwd = os.getcwd()
folder = filepath = os.path.abspath(os.path.join(cwd, '..', 'Project Data','GradientOptimization','Justin'))

filename = "ErrorDistribution.json"
filepath = os.path.abspath(os.path.join(folder,filename))
with open(filepath) as data:
    errorProbs = json.load(data)
filename = "zenweights.json"
filepath = os.path.abspath(os.path.join(folder,filename))
with open(filepath) as data:
    zenweights = json.load(data)

MINweight = zenweights[errorProbs.index(min(errorProbs))]


# Fit to Gaussian
# gauss_mean = 0.32; std = 0.3     # Experimentally Determined
gauss_mean = 0.32; std = 0.01
x_range = np.linspace(0,1,100)
gauss_errorprobs = mlab.normpdf(x_range, gauss_mean, std)
MAXgauss_error = max(gauss_errorprobs)
scale = (1.0-min(errorProbs))/max(gauss_errorprobs)
gauss_errorprobs = np.add(np.multiply(gauss_errorprobs,-scale),1.0)


# Plot Fit
acceptanceProbs = [1-value for value in errorProbs]
fig,ax = plt.subplots()
ax.plot(zenweights,errorProbs)
ax.plot(x_range,gauss_errorprobs)
ax.set_xlim([0,1])
plt.title('Probability of Error vs. Zenweight')
plt.xlabel('Zenweight')
plt.ylabel('Prob. of Error')
plt.show()





# II)------Assume Form on User Characterization------------------------------------------------------------
#

# Assume Distribution on User Characterization as Beta Distribution
# alpha = 2; belta => [3,10]

alpha = 2.0
start = 3; end = 20;
beta_param = np.random.uniform(start,end,1)     # Choose beta for specific individual
lambda_true = alpha/(alpha+beta_param)

def integrand(x,a,b):
    return 2.0/(2.0+x)/abs(b-a)
average_weight = integrate.quad(integrand, start, end,args =(start,end))[0]    # Find expected mean


# Plot User Distribution
fig, ax = plt.subplots()
rv = beta(alpha, beta_param)
x = np.linspace(0,1,100)
ax.plot(x, rv.pdf(x), 'k-', lw=2)
text = 'Alpha: '+str(alpha)+'\n'+'Beta: '+str(beta_param[0])+'\n'+'Mean: '+str(lambda_true[0])
ax.text(0.5, 2,text, style='italic',
        bbox={'facecolor':'gray', 'alpha':0.5, 'pad':10})
plt.xlabel('Zen weight')
plt.ylabel('Prob. Density')
plt.title('User Characterization')
plt.show()




# III)------Infer User Characterization----------------------------------------------------------
#


# Initialize Test Metadata
weighthistory = [average_weight]
lambda_hat_hist = []
wzen = 0.0  # Start at Zero
scale = (1.0-min(errorProbs))/MAXgauss_error
maxiter = 2000
threshold = 0.05
MAlen = 100
delta = 0.3


# START: Gradient Ascent / Descent Loop
MAlist = deque([wzen for i in range(0,MAlen,1)])
iter = 0
converged = False

while(not converged and iter < maxiter):

        # Random Sample from User Characterization Distribution
        lambda_current = beta.rvs(alpha, beta_param, size=1)[0]

        # Determine if Route Accepted or Not (Based on Experimentally determined Error vs. Wzen curve)
        acceptance_prob = scale*mlab.normpdf(wzen, lambda_current, std)
        result = np.random.binomial(n=1,p=acceptance_prob)

        # Save Accepted Weights

        if(result == 1):
            weighthistory.append(wzen)

        # Determine New Wzen Through Ascent / Descent
        lambda_hat = float(np.mean(weighthistory))
        lambda_hat_hist.append(lambda_hat)
        beta_hat = alpha/lambda_hat-alpha
        rv = beta(alpha, beta_hat)      # New Estimate on User Characterization

        increment = 1e-6
        approx_gradient = ((rv.pdf(wzen+increment)-rv.pdf(wzen))/increment)
        wzen += delta*np.arctan(approx_gradient)    # Use gradient of expected distribution to move Wzen

        wzen = np.random.uniform(0.0,0.2,1)[0]

        if(wzen < 0.0):
            wzen = 0.0
        elif(wzen > 1.0):
            wzen = 1.0

        # Update Window of Recent Weights
        MAlist.appendleft(lambda_hat)
        MAlist.pop()


        # Check for Convergence
        converged = True
        for value in list(MAlist):
            test = abs(value-lambda_true)/lambda_true < threshold
            converged = converged and test
        iter += 1


# # Plot Wzen Changes
# gauss_errorprobs = mlab.normpdf(x_range, gauss_mean+shift, std)
# scale = (1.0-min(errorProbs))/MAXgauss_error
# gauss_errorprobs = np.add(np.multiply(gauss_errorprobs,-scale),1.0)
# fig,ax = plt.subplots()
# ax.plot(x_range,gauss_errorprobs)
# ax.plot(weighthistory,y)
# ax.set_xlim([0,1])
# plt.title('Zen Weight Changes')
# plt.xlabel('Zenweight')
# plt.ylabel('Prob. of Error')
# # plt.show()

# Plot Convergence of Average to Ideal

fig,ax = plt.subplots()
ax.plot(range(0,len(weighthistory)),weighthistory)
ax.plot(range(0,len(weighthistory)),[lambda_true for i in range(0,len(weighthistory))] )
plt.title('Weight History')

fig,ax = plt.subplots()
ax.plot(range(0,len(lambda_hat_hist)),lambda_hat_hist)
ax.plot(range(0,len(lambda_hat_hist)),[lambda_true for i in range(0,len(lambda_hat_hist))] )
plt.title('Lambda Hat History')
plt.show()

# Scatter Points
fig,ax = plt.subplots()
plt.hist(weighthistory)
plt.show()
