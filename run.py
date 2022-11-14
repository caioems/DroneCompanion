# -*- coding: utf-8 -*-
# """
# Created on Thu Apr 21 17:17:20 2022

# Script designed to take useful information from ArduCopter dataflash logs and
# present it on a KML file.

# @author: [t2]caiera
# """

#TODO: create a package auto update function
#TODO: create new table with 'timestamps' and 'drone_uid' for motor data     
#TODO: create dashboard for local db
#TODO: create a windows service for syncing data with cloud db(API)

import simplekml
import concurrent.futures
import os
#from database.repository.report_repo import RpRepo
from internal.loglist import LogList
from internal.daychecker import DayChecker
from tests.healthtests import HealthTests
from tqdm import tqdm


class PipeLine:    
    def __init__(self):
        self._root = LogList()
        self._log_list = self._root.log_list
        self._kml = self.kml_container('flights_kml')
        self.dc = None
        
    def kml_container(self, kml_name):
        self._kml = simplekml.Kml(name=kml_name)
        self._kml.newfolder(name='RGB')
        self._kml.newfolder(name='AGR')
        return self._kml       
    
    #TODO: store timestamps as string
    def run(self, flight_log):
        self.dc = DayChecker()
        self.dc.create_csv(flight_log)    

        self.dc.cam_df = self.dc.create_df(flight_log, "CAM")
        self.dc.ev_df = self.dc.create_df(flight_log, "EV")
        self.dc.bat_df = self.dc.create_df(flight_log, "BAT")
        self.dc.rcou_df = self.dc.create_df(flight_log, "RCOU")
        self.dc.terr_df = self.dc.create_df(flight_log, "TERR")
        self.dc.vibe_df = self.dc.create_df(flight_log, "VIBE")

        self.flight_timestamp = str(self.dc.ev_df.index[0].timestamp())
        self.dc.report = HealthTests(self.dc.rcou_df, self.dc.vibe_df)
        self.dc.report.run()
        
        #Storing data into db
        #repo = RpRepo()
        #repo.insert(dc.report.motors_status, dc.report.motors_feedback, dc.report.imu_status, dc.report.imu_feedback)  

        flight_alt = self.dc.terr_df['CHeight'].median()
        if flight_alt < 105:
            rgb = self.dc.create_linestring(flight_log, ppl._kml, 0)
            self.dc.rgb_style(rgb)
            self.dc.create_balloon_report(rgb)
        elif flight_alt > 105:
            agr = self.dc.create_linestring(flight_log, ppl._kml, 1)
            self.dc.agr_style(agr)
            self.dc.create_balloon_report(agr)
        else:
            print("Invalid folder name.")          
        

##running when not being imported
if __name__ == "__main__":
    ppl = PipeLine()
    #max_workers alt formula = int(os.cpu_count()/3)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(tqdm(executor.map(ppl.run, ppl._log_list), total=len(ppl._log_list)))
        results
    
    kml_path = f'{ppl._root.root_folder}/flights.kml'     
    ppl._kml.save(kml_path)
    print('Done.')
    os.startfile(kml_path)