import pyodbc

'''
Using PyODBC to connect to MS-SQL Server.

Ref:
http://mkleehammer.github.io/pyodbc/api.html

Error:
pyodbc.Error: ('01000', "[01000] [unixODBC][Driver Manager]Can't open lib 'SQL Server' : file not found (0) (SQLDriverConnect)")

Fix:
Confirm and install unixODBC



'''
#dbserver_ip = "localhost"
#dbserver_ip = "10.131.83.195"
dbserver_ip = "192.168.15.82"
dbserver_db = "AUVSI"
dbserver_user = "spykat"
dbserver_password = "spykat"


#dbserver_ip = "172.16.121.148"
#dbserver_db = "AUVSI"
#dbserver_user = "spykat"
#dbserver_password = "pasword"



#odbc_conn_str = 'driver={SQL Server};SERVER=' + dbserver_ip + ';DATABASE=' + dbserver_db + ';'
odbc_conn_str = 'DRIVER={FreeTDS};SERVER=' + dbserver_ip + ';PORT=1433;DATABASE=' + dbserver_db + ';'
#odbc_conn_str = 'mssql+pyodbc://' + dbserver_user + ':' + dbserver_password + '@' + dbserver_ip + ':1433/' + dbserver_db + '?driver=FreeTDS'

odbc_conn_str += 'UID=' + dbserver_user + ';PWD=' + dbserver_password

print "\n\n", odbc_conn_str

#cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=testdb;UID=me;PWD=pass')
cnxn = pyodbc.connect(odbc_conn_str)
cursor = cnxn.cursor()

#live_query = "SELECT * FROM FlightTelemetry"

live_query="SELECT TOP 1 Timestamp, Latitude, Longitude, Altitude, Azimuth, Pitch, Roll, CPUTimeStamp, Heading FROM FlightTelemetry  ORDER BY ID DESC"

    #WHERE ID = (SELECT MAX(Timestamp) FROM FlightTelemetry)
    #
    #"""

#cursor.execute("""SELECT
#	Timestamp, Latitude, Longitude, Altitude, Azimuth, Pitch, Roll, CPUTimeStamp, Heading
#	FROM
#    SpyKat_MSSQL_FlightTelemetry_Data_Export
#    WHERE convert(date, timestamp) = '2015-10-18'
#    #FlightTelemetry
#    """)
cursor.execute(live_query)

rows = cursor.fetchall()

for row in rows:
	print row.Timestamp, row.Longitude, row.Latitude, row.Heading, row.Pitch, row.Roll

cursor.close()
cnxn.close()
