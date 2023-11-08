# Drone Companion

Drone Companion is a phyton-based open source ETL tool that consolidates data from UAV flight logs. By pointing out a folder containing at least one log file, it will extract data related to the system and its sensors. This data will be used to check if the flight met some of the flight protocols, such as board temperature, camera parameters and GPS quality. In the end, it outputs a KML file containing flying paths, each one with a brief final report. The processed data may be stored in a sqlite database.

If working with Power BI, requires ODBC driver:
http://www.ch-werner.de/sqliteodbc/

 
