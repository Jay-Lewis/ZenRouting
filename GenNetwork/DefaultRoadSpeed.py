__author__ = 'Justin'

# DESCRIPTION:
# This function returns a max speed based on Open Street Map (OSM) naming conventions
# Each OSM edgetype has a given max speed in mph by convention
#

def getdefaultspeed(string):

    unknownspeed = 30
    restrictedspeed = 0.01

    defaultspeeds = {
        'motorway':70,
        'trunk':60,
        'primary':55,
        'secondary':55,
        'tertiary':50,
        'unclassified':40,
        'residential':25,
        'living_street':15,
        'motorway_link': 40,
        'trunk_link': 35,
        'primary_link': 35,
        'secondary_link':25,
        'tertiary_link': 20,
        'service': 12,
        'track':restrictedspeed,
        'cycleway':restrictedspeed,
        'footway':restrictedspeed,
        'rail':restrictedspeed,
        'steps':restrictedspeed,
    }

    speed = defaultspeeds.get(string,unknownspeed)

    return speed

