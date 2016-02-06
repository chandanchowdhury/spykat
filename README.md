# SpyKat - Kansas State University AUVSI-SUAS Club
[http://spykat.org/](http://spykat.org)

---
## Background

***
## Architecture
The telemetry data is sent by the the drone to the Mission Planner application running in the Ground Control Station. The Mission Planner application has been modified to capture the telemetry data and store them on a MSSQL server.

This [Flask][1] application queries the MSSQL server and generates the KML data which is displayed on Google Earth.

***
## Running the application

To run the application
1. Clone the application in a directory
2. Update the database and AUVSI-SUAS Judges' server details
3. Run the command below
   python run.py
4. Double click on the main.kml file which should open Google Earth and start displaying the obstacle and flight data.

___
[1] https://en.wikipedia.org/wiki/Flask_(web_framework)
