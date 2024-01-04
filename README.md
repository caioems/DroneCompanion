
# Drone Companion

Drone Companion is a Python-based open source ETL tool that consolidates data from UAV flight logs. By pointing out a root folder, it will search within it for BIN logs and extract from them data related to the system and its sensors. This data will be used to check for flight compliance and UAV performance (e.g. Flight date and time, flight controller UID, battery usage, electronics issues, motors performance, GPS stats, etc). This way, drone operators get a compliance report on the missions carried out, guaranteeing the quality of the data collected, as well as an overview on the conditions of their UAV.

Right now it's only compatible with ArduPilot dataflash logs. It outputs a KML file containing a summarized report and it may also store the processed data in a sqlite database (experimental).