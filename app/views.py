from flask import render_template, Response
from app import app
from interop import *
from StaticObstacle import StaticObstacle

server = 'http://172.16.121.153'
username =  'testadmin'
password =  'testpass'

camera_height_meter = 100

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
        mo = ('%.5f' % m.longitude)  + ', ' + ('%.5f' % m.latitude) + ', ' + ('%.5f' % (m.altitude_msl * 0.3048))

    return Response(render_template('dynamic.kml',moving_obstacle_data=mo),
                        mimetype='text/xml')

@app.route('/telemetry.kml')
def telemetry_kml():
    return Response(render_template('telemetry.kml'),
                        mimetype='text/xml')
