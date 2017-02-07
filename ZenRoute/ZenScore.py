__author__ = 'Justin'

import math

# DESCRIPTION: This script will generate a Zenness metric which encapsulates driving factors which cause stress
#
# INPUT: edge dictionary
#
# OUTPUT: ZenScore


def zenscore(edge_dictionary):
    currenttime = edge_dictionary['currenttime']
    basetime = edge_dictionary['basetime']
    distance = edge_dictionary['distance']

    if basetime < 0.1:  # prevent divide by zeroish numbers
        basetime = 0.1

    zenness = distance*math.log(1+math.fabs(currenttime-basetime)/basetime)

    return zenness