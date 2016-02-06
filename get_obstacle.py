from interop import *

server = 'http://172.16.121.153'
username =  'spykat'
password =  'spykat'

client = AsyncClient(server, username, password)

server_info = client.get_server_info().result()

print "-- Server Info --"
print server_info.message
print server_info.message_timestamp
print server_info.server_time

stationary, moving = client.get_obstacles().result()

print "-- Stationary Obstacles --"
print "Count: ", len(stationary)
for i in stationary:
	print "Lat: ", i.latitude
	print "Lon: ", i.longitude
	print "Radius: ", i.cylinder_radius
	print "Height: ", i.cylinder_height

# The below details are of a moving obstacle at the time when request was made
# Next request would have a different Lat, Long as the obstacle has now moved
print "-- Moving Obstacles --"
print "Count: ", len(moving)
for i in moving:
	print "Lat: ", i.latitude
	print "Lon: ", i.longitude
	print "Radius: ", i.altitude_msl
	print "Height: ", i.sphere_radius


# For live flight data
# Fetch data from SQLServer and generate live KML link
'''
FlightTelemetry (
Timestamp,
Latitude,
Longitude,
Altitude,
Azimuth,
Pitch,
Roll,
CPUTimeStamp,
Heading
)


Waypoint (pk:1, order:1, pos:AerialPosition (pk:1, alt:200.0, gps:GpsPosition (pk:3, lat:38.142544, lon:-76.434088)))

Waypoint (pk:2, order:2, pos:AerialPosition (pk:2, alt:300.0, gps:GpsPosition (pk:4, lat:38.141833, lon:-76.425263)))

Waypoint (pk:3, order:3, pos:AerialPosition (pk:3, alt:100.0, gps:GpsPosition (pk:5, lat:38.144678, lon:-76.427995)))
'''
