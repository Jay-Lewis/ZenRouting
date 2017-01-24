__author__ = 'Justin'

# DESCRIPTION:
# This function returns the euclidean distance between two points. Takes two numbers as input.

import math

def distance(a,b):
    return math.sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)