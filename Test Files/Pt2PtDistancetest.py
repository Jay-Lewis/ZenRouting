__author__ = 'Justin'

from geopy.distance import vincenty as latlondist
from geopy.distance import great_circle as latlondist2

# Test distance between lat-lon pair

origin = '30.630637, -96.333554'
destination = '30.617907, -96.322968'
meterconv = 1609.344

distance = latlondist(origin,destination).miles
distance2 = latlondist2(origin,destination).miles

print(distance)
print(distance2)
