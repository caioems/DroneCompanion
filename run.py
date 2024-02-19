# -*- coding: utf-8 -*-
# """
# Created on Thu Apr 21 17:17:20 2022

# Also known as "day checker", it's a tool designed to extract useful data from ArduCopter dataflash logs, to model this data and
# to store it in a sqlite database. It also generates a KML file for easy tracking of the analyzed logs.

# @author: caioems
# """
import os
import simplekml
import concurrent.futures
from tqdm import tqdm

import tests.gps_test as gps_test
from database.repository.report_repo import RpRepo
from database.repository.motors_repo import MtRepo
from internal.loglist import LogList
from internal.daychecker import DayChecker



class Main:
    def __init__(self):
        """
         Initialize the object by creating the log list 
         and the KML object.
         
        """
        self._root = LogList()
        self._bin_list = self._root.bin_list
        self._gnss_list = self._root.gnss_list
        self._kml = self.create_kml()

    def create_kml(self, kml_name="flights"):
        """
         Create KML object which will hold geometries and reports.
         
         @param kml_name - The name of the KML object.
         
         @return The newly created KML object.
         
        """
        self._kml = simplekml.Kml(name=kml_name)
        return self._kml
    
    def linestring_dev(self):
        """
        Method to create a line string, change its style and create a balloon report.
        """
        flight_ls = self.dc.create_linestring(self._kml)
        self.dc.change_line_style(flight_ls)
        self.dc.create_balloon_report(flight_ls)

    def write_to_db(self):
        """
         Write data to sqlite database.
         
        """
        rp_repo = RpRepo()
        rp_repo.insert(
            self.dc.flight_timestamp,
            self.dc.drone_uid,
            self.dc.htests.motors_status,
            self.dc.htests.motors_feedback,
            self.dc.htests.imu_status,
            self.dc.htests.imu_feedback,
            self.dc.htests.vcc_status,
            self.dc.htests.vcc_mean,
            self.dc.htests.vcc_std,
        )

        m_repo = MtRepo()
        m_repo.insert(
            self.dc.flight_timestamp,
            self.dc.drone_uid,
            self.dc.htests.motors_pwm_list[0],
            self.dc.htests.motors_pwm_list[1],
            self.dc.htests.motors_pwm_list[2],
            self.dc.htests.motors_pwm_list[3],
        )

    def run_bin_analysis(self, flight_log, gnss_results):
        """
         Creates and runs the DayChecker. This is the main method.
         
         @param flight_log - flight log to be analyzed         
        """
        # Creating main class
        self.dc = DayChecker(flight_log, gnss_results)
        
        #TODO: add other output formats (csv, js)
        # Storing data into db
        self.write_to_db()

        # Creating the kml features
        self.linestring_dev()
        
        return self.dc
    
    def run_gnss_analysis(self, gnss_log):
        path = gnss_log.parent
        gnss_rinex = os.path.join(
            path,
            f"{gnss_log.stem}.obs"
            )
            
        gps_test.parse_rtcm_to_rinex(gnss_log)
        rinex_epochs = gps_test.get_rinex_epochs(gnss_rinex)
        
        gnss_test = {}
        gnss_test['md5'] = gps_test.calculate_md5(gnss_log)
        gnss_test['gps_freq'] = gps_test.check_gps_frequency(rinex_epochs)
        gnss_test['gps_date'] = gps_test.check_gps_date(rinex_epochs)
        return gnss_test
            
##running when not being imported
if __name__ == "__main__":
    flights = Main()
    kml_file = f"{flights._root.root_folder}/flights.kml"

    unique_gnss_list = gps_test.find_unique_gnss_logs(flights._gnss_list)
    print("Processing GNSS logs...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        gnss_results = list(
            tqdm(
                executor.map(flights.run_gnss_analysis, unique_gnss_list),
                total=len(unique_gnss_list)
            )
        )
    
    print("Processing BIN logs...")
    bin_results = [flights.run_bin_analysis(binlog, gnss_results) for binlog in tqdm(flights._bin_list)]
    
    flights._kml.save(kml_file)
    print("Done!")
    os.startfile(kml_file)



