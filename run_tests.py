# -*- coding: utf-8 -*-
# """
# Created on Thu Apr 21 17:17:20 2022

# Script designed to take useful information from ArduCopter dataflash logs and
# present it on a KML file.

# @author: [t2]caiera
# """

import simplekml
from multiprocessing import Pool
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
    
    #TODO: armazenar timestamps como numeric ou string
def run(flight_log):
    dc = DayChecker()
    dc.create_csv(flight_log)

    dc.cam_df = dc.create_df(flight_log, "CAM")
    dc.ev_df = dc.create_df(flight_log, "EV")
    dc.bat_df = dc.create_df(flight_log, "BAT")
    dc.rcou_df = dc.create_df(flight_log, "RCOU")
    dc.terr_df = dc.create_df(flight_log, "TERR")
    dc.vibe_df = dc.create_df(flight_log, "VIBE")

    dc.report = HealthTests(dc.rcou_df, dc.vibe_df)
    dc.report.run()

    #TODO: transferir dados do dc.report para tabela sql

    flight_alt = dc.terr_df['CHeight'].median()
    if flight_alt < 105:
        rgb = dc.create_linestring(flight_log, ppl._kml, 0)
        dc.rgb_style(rgb)
        dc.create_balloon_report(rgb)
    elif flight_alt > 105:
        agr = dc.create_linestring(flight_log, ppl._kml, 1)
        dc.agr_style(agr)
        dc.create_balloon_report(agr)
    else:
        print("Invalid folder name.")           
        

##running when not being imported
if __name__ == "__main__":
    ppl = PipeLine()        
    [run(log) for log in tqdm(ppl._log_list)]    
    #list(Pool().imap(run, ppl._root.log_list))
    ppl._kml.save(f'{ppl._root.root_folder}/flights.kml')
    print('Done.')
        
    

