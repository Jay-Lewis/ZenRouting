__author__ = 'Justin'


from sklearn.linear_model import LogisticRegression
import os
import json
import networkx as nx
import numpy as np
from GetRouteInfo import routeinfo

persons = ['Justin','Justin2','Pablo']
for person in persons:

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


    # Logistic Regression
    model = LogisticRegression()
    model = model.fit(np.array(X),np.array(y))

    print('Model Accuracy: '+str(model.score(X,y)))
    print('Average Rate: '+str(np.mean(y)))


    # Plot Logistic Regression
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    xx, yy = np.mgrid[0:1:0.1, 0:1:0.1]
    grid = np.c_[xx.ravel(), yy.ravel()]
    probs = model.predict_proba(grid)[:, 1].reshape(xx.shape)

    surf = ax.plot_surface(xx, yy, probs, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    # ax.plot_wireframe(xx, yy, probs, rstride=10, cstride=10)

    plt.xlabel('Percentage Zen Decrease')
    plt.ylabel('Percentage Time Decrease')
    plt.title(person)
    ax.set_zlabel('Probability of ZenRoute')

# Show All Graphs at Once
plt.show()