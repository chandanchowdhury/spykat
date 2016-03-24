import pyodbc, json
import logging
from interop import *


logger = logging.getLogger('telemetry_to_judge')

server = 'http://172.16.121.159'
username =  'testadmin'
password =  'testpass'
#username = 'spykat'
#password = 'spykat'

camera_height_meter = 100

#-------------
# DB Server parameters
dbserver_ip = "192.168.15.81"
#dbserver_ip = "172.16.121.148"

dbserver_user = "spykat"
dbserver_password = "spykat"

dbserver_db = "AUVSI"

odbc_conn_str = 'DRIVER={FreeTDS};SERVER=' + dbserver_ip + ';PORT=1433;DATABASE=' + dbserver_db + ';'
odbc_conn_str += 'UID=' + dbserver_user + ';PWD=' + dbserver_password


cnxn = None
client = None

def open_dbserver_connection():
    cnxn = pyodbc.connect(odbc_conn_str)
    if cnxn == None:
        raise Exception("Not able to connect to MSSQL: "+dbserver_ip)

    print "[+] Connection opened..."
    logger.info("Connection opened...")


'''
Telemetry data from MSSQL server
'''
def get_telemetry_data():
    live_query="SELECT TOP 1 Latitude, Longitude, Altitude, Heading FROM FlightTelemetry  ORDER BY ID DESC"

    # In case connection is broken, retry opening the connection
    if(cnxn == None):
        open_dbserver_connection

    cursor = cnxn.cursor()
    if cursor == None:
        raise Exception("Not able to get a cursor")

    cursor.execute(live_query)
    if cursor == None:
        raise Exception("Not able to execute SQL query")

    rows = cursor.fetchall()
    if cursor == None:
        raise Exception("Not able to execute SQL query")

    for row in rows:
        print row.Longitude, row.Latitude, row.Heading
        Telemetry(row.Longitude, row.Latitude, row.Altitude, row.Heading)

    cursor.close()
    #cnxn.close()

'''
Post telemetry data to judge's server
'''
def post_telemetry_to_judge(telem):

    client = AsyncClient(server, username, password)

    client.post_telem(telem)

if __name__ == '__main__':

    open_dbserver_connection()

    # to infinity and beyond
    while(1):
        # Get telemetry data from MSSQL
        t = get_telemetry_data

        # Post telemetry data to judge's server
        post_telemetry_to_judge(t)
