__author__ = 'Justin'

import googlemaps
from googlemaps import convert
from datetime import datetime
from datetime import timedelta
gmaps = googlemaps.Client(key='AIzaSyAVf9cLmfR52ST0VZcFsf-L-HynMTCzZEM')

# Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
# print(geocode_result)
# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
# print(reverse_geocode_result)

# Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions("Sydney Town Hall",
#                                      "Parramatta, NSW",
#                                      mode="transit",
#                                      departure_time=now)

# Distance Matrix / Directions

origin = '29.584769, -98.617857'
destination = '29.599569, -98.385984'

origin = '30.630637, -96.333554'
waypoints = ['via:30.629712, -96.325264']
destination = '30.617907, -96.322968'

print(origin)
print(destination)


now = datetime.now()
later = datetime(now.year,now.month,now.day+1,17,0)

'''------------------------------------------------------------------------------'''

directions_result = gmaps.directions(origin,
                                     destination,
                                     mode="driving",
                                     departure_time=now,
                                     traffic_model = 'best_guess',
                                     alternatives = True)

print(directions_result)

encodedpolyline = directions_result[0]['overview_polyline']['points']
print(encodedpolyline)
print(type(encodedpolyline))
polyline = convert.decode_polyline(encodedpolyline)
print(polyline)

traveltime = directions_result[0]['legs'][0]['duration']['value']
fulltime = directions_result[0]['legs'][0]['duration_in_traffic']['value']
traffictime = fulltime-traveltime

print('TravelTime:',traveltime)
print('FullTime:',fulltime)
print('Traffictime:',traffictime)


'''------------------------------------------------------------------------------'''

# directions_result = gmaps.directions(origin,
#                                      destination,
#                                      mode="driving", waypoints = waypoints,
#                                      departure_time=later, traffic_model = 'best_guess')
#
# print(directions_result)
#
# traveltime = 0
# legs = directions_result[0]['legs']
# for leg in legs:
#     seconds = leg['duration']['value']
#     traveltime = traveltime + seconds
#
# print(traveltime)
# print(traveltime/60)
'''------------------------------------------------------------------------------'''

# distance_matrix_result = gmaps.distance_matrix(origin,
#                                     destination,
#                                      mode="driving",
#                                      departure_time=now,
#                                      traffic_model ='best_guess')
# print(distance_matrix_result)

'''------------------------------------------------------------------------------'''

distance_matrix_result2 = gmaps.distance_matrix(origin,
                                    destination,
                                     mode="driving",
                                     departure_time=later,
                                     traffic_model ='best_guess')
print('Best Guess:',distance_matrix_result2)
#
# distance_matrix_result2 = gmaps.distance_matrix(origin,
#                                     destination,
#                                      mode="driving",
#                                      departure_time=later,
#                                      traffic_model ='optimistic')
# print('Optimistic:',distance_matrix_result2)
#
# distance_matrix_result2 = gmaps.distance_matrix(origin,
#                                     destination,
#                                      mode="driving",
#                                      departure_time=later,
#                                      traffic_model ='pessimistic')
# print('Pessimistic',distance_matrix_result2)

'''------------------------------------------------------------------------------'''

print(now)
print(later)