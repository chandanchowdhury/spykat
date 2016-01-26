from decimal import Decimal

class StaticObstacle:

    def __init__(self, latitude, longitude, radius, height):

        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius/1000000
        self.height = height*0.3048 #convert the height to meter for Google Earth

    def get_kml(self):
        self.a_lat = self.latitude + self.radius
        self.a_lon = self.longitude - self.radius

        self.b_lat = self.latitude + self.radius
        self.b_lon = self.longitude + self.radius

        self.c_lat = self.latitude - self.radius
        self.c_lon = self.longitude + self.radius

        self.d_lat = self.latitude - self.radius
        self.d_lon = self.longitude - self.radius

        '''
        Google Earth Coorinate Format
        <coordinates> <Longitude>,<Latitude>,<Altitude> </coordinates>
        '''


        static_obstacle_data  = str(self.a_lon) + ',' + str(self.a_lat) + ', ' + str(self.height) + ' \n '
        static_obstacle_data += str(self.b_lon) + ',' + str(self.b_lat) + ', ' + str(self.height) + ' \n '
        static_obstacle_data += str(self.c_lon) + ',' + str(self.c_lat) + ', ' + str(self.height) + ' \n '
        static_obstacle_data += str(self.d_lon) + ',' + str(self.d_lat) + ', ' + str(self.height) + ' \n '


        '''
        static_obstacle_data  = str(self.a_lat) + ',' + str(self.a_lon) + ', ' + str(self.height) + ' \n '
        static_obstacle_data += str(self.b_lat) + ',' + str(self.b_lon) + ', ' + str(self.height) + ' \n '
        static_obstacle_data += str(self.c_lat) + ',' + str(self.c_lon) + ', ' + str(self.height) + ' \n '
        static_obstacle_data += str(self.d_lat) + ',' + str(self.d_lon) + ', ' + str(self.height) + ' \n '
        '''

        return static_obstacle_data
