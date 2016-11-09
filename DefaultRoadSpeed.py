__author__ = 'Justin'

def getdefaultspeed(string):

    unknownspeed = 30

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
        'service': 12
    }

    speed = defaultspeeds.get(string,unknownspeed)

    return speed

