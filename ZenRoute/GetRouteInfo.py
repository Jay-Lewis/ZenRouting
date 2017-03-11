__author__ = 'Justin'

def routeinfo(G,route,keys):
    # initialize dictionary
    info = {}
    for key in keys:
        info[key] = 0

    # add up attribute along route
    for nodeA, nodeB in zip(route,route[1:]):
        for key in keys:
            info[key] += G[nodeA][nodeB][key]

    return info
