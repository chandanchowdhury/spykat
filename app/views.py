from flask import render_template, Response
from app import app
from interop import *
import pyodbc

from StaticObstacle import StaticObstacle

server = 'http://172.16.121.154'
#username =  'testadmin'
#password =  'testpass'
username = 'spykat'
password = 'spykat'

camera_height_meter = 100

#-------------
# DB Server parameters
dbserver_ip = "192.168.15.82"
#dbserver_ip = "172.16.121.148"

dbserver_user = "spykat"
dbserver_password = "spykat"

dbserver_db = "AUVSI"

odbc_conn_str = 'DRIVER={FreeTDS};SERVER=' + dbserver_ip + ';PORT=1433;DATABASE=' + dbserver_db + ';'
odbc_conn_str += 'UID=' + dbserver_user + ';PWD=' + dbserver_password

#--------------

@app.route('/')
@app.route('/index')
def index():

    return Response(render_template('main.kml'),
                        mimetype='application/vnd.google-earth.kml+xml');

@app.route('/fence.kml')
def fence_kml():
    return Response(render_template('fence.kml'),
                        mimetype='text/xml')


@app.route('/static.kml')
def static_kml():

    client = AsyncClient(server, username, password)

    stationary, moving = client.get_obstacles().result()

    static_page_data = {}
    static_obstacles_data = []

    if len(stationary) > 0:
        static_page_data['camera_view_longitude'] = stationary[0].longitude
        static_page_data['camera_view_latitude'] = stationary[0].latitude
        #static_page_data['camera_view_altitude'] = (stationary[0].cylinder_height + camera_height_meter)
        static_page_data['camera_view_altitude'] =  2000

    for s in stationary:
    #s = stationary[1]
        so = StaticObstacle(s.latitude, s.longitude, s.cylinder_radius, s.cylinder_height)
        static_obstacles_data.append({'kml_data': so.get_kml()})

    #print static_page_data

    return Response(render_template('static.kml',
        static_page_data=static_page_data,
        static_obstacles_data=static_obstacles_data),
        mimetype='text/xml')

@app.route('/dynamic.kml')
def dynamic_kml():
    client = AsyncClient(server, username, password)

    stationary, moving = client.get_obstacles().result()

    for m in moving:
        mo = ('%.6f' % m.longitude)  + ', ' + ('%.6f' % m.latitude) + ', ' + ('%.6f' % (m.altitude_msl * 0.3048Spy  ))

    return Response(render_template('dynamic.kml',moving_obstacle_data=mo),
                        mimetype='text/xml')


@app.route('/telemetry.kml')
def telemetry_kml():
    ###
    #test_query = """SELECT
    #	Timestamp, Latitude, Longitude, Altitude, Azimuth, Pitch, Roll, CPUTimeStamp, Heading
    #	FROM
    #    SpyKat_MSSQL_FlightTelemetry_Data_Export
    #    WHERE convert(date, timestamp) = '2015-10-18'
    #    #FlightTelemetry
    #    """


    live_query = """SELECT
        TOP 1
    	Timestamp, Latitude, Longitude, Altitude, Azimuth, Pitch, Roll, CPUTimeStamp, Heading
    	FROM FlightTelemetry
        #WHERE ID = (SELECT MAX(Timestamp) FROM FlightTelemetry)
        ORDER BY ID DESC
        """

    live_query="SELECT TOP 1 Timestamp, Latitude, Longitude, Altitude, Azimuth, Pitch, Roll, CPUTimeStamp, Heading FROM FlightTelemetry  ORDER BY ID DESC"

    cnxn = pyodbc.connect(odbc_conn_str)
    cursor = cnxn.cursor()

    cursor.execute(live_query)

    rows = cursor.fetchall()

    for row in rows:
    	print row.Timestamp, row.Longitude, row.Latitude, row.Heading
        uav_telemetry_data = ('%.6f' %row.Longitude) + ", " + ('%.6f' % row.Latitude) + ", " + ('%.1f' % (row.Altitude * 0.3048))
    cursor.close()
    #cnxn.close()

    return Response(render_template('telemetry.kml',uav_current_telemetry=uav_telemetry_data),
    #return Response(render_template('telemetry.kml'),
                        mimetype='text/xml')
