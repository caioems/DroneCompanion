# -*- coding: utf-8 -*-
# """
# Created on Thu Apr 21 17:17:20 2022

# Script designed to take useful information from ArduCopter dataflash logs and
# present it on a KML file.

# @author: [t2]caiera
# """

import simplekml
from internal.loglist import LogList
from internal.daychecker import DayChecker
from tests.healthtests import HealthTests
from tqdm import tqdm

class PipeLine:    
    def __init__(self):
        self.__root = LogList()
        self.__log_list = self.__root.log_list
        self.__kml = self.kml_container('flights_kml')
        
    def kml_container(self, kml_name):
        self.__kml = simplekml.Kml(name=kml_name)
        self.__kml.newfolder(name='RGB')
        self.__kml.newfolder(name='AGR')
        return self.__kml       
     
    def run(self):
        for i in tqdm(self.__log_list):
            dc = DayChecker()
            dc.create_csv(i)
            dc.cam_df = dc.create_df(i, "CAM")
            dc.ev_df = dc.create_df(i, "EV")
            dc.bat_df = dc.create_df(i, "BAT")
            dc.terr_df = dc.create_df(i, "TERR")
            dc.rcou_df = dc.create_df(i, "RCOU")
            dc.vibe_df = dc.create_df(i, "VIBE")
            dc.report = HealthTests(dc.rcou_df, dc.vibe_df)
            dc.report.run()
            self.dc = dc
            
            if dc.terr_df['CHeight'].median() < 105:
                rgb = dc.create_linestring(i, self.__kml, 0)
                dc.rgb_style(rgb)
                dc.create_balloon_report(rgb)
            elif dc.terr_df['CHeight'].median() > 105:
                agr = dc.create_linestring(i, self.__kml, 1)
                dc.agr_style(agr)
                dc.create_balloon_report(agr)
            else:
                print("Invalid folder name.")
                
        self.__kml.save(f'{self.__root.root_folder}/flights.kml')

##running when not being imported
if __name__ == "__main__":
    pl = PipeLine()
    pl.run()
    

