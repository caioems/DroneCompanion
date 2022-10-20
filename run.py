# -*- coding: utf-8 -*-
# """
# Created on Thu Apr 21 17:17:20 2022

# Script designed to take useful information from ArduCopter dataflash logs and
# present it on a KML file.

# @author: [t2]caiera
# """

import os
import pandas as pd
import simplekml
from internal.loglist import LogList
from statistics import mean, median
from tests.healthtests import HealthTests
from tqdm import tqdm

##MAIN CLASS
class DayChecker:
    #user input for root folder & log list's WindowsPath object creation
    # def input_window(self):
    #     root = Tk()
    #     root.update()
    #     path = askdirectory(title='Select the root folder:')
    #     root.destroy()
    #     return path
    
    # def create_log_path (self, root_path):
    #     log_list = list(pathlib.Path(root_path).glob(r"**\**\*.BIN"))
    #     return log_list   
    def __init__(self):
        self.__root_folder = LogList.root_folder
        self.__log_list = LogList.create_log_path()
        self.__kml = self.create_kml('flights_kml')
        self.__kml = self.kml_containers(self.__kml)
        
    def kml_containers(self):
        self.__kml.newfolder(name='RGB')
        self.__kml.newfolder(name='AGR')
        return self.__kml
    
    #TODO: ARRUMAR ARGUMENTOS DAS FUNÇOES ABAIXO      
    
    def create_csv(self, log_path):
        types = ["CAM", "EV", "BAT", "TERR", "RCOU", "VIBE"]
        log = log_path.as_posix()
        path = log_path.parent
        for t in types:    
            mycmd = "mavlogdump.py --planner --format csv --types " + t + " " + str(log) + " > " + str(path) + "/" + t + ".csv"
            os.system(mycmd)
    
    def create_df(self, log_path, csv_name):
        global file, csv_file
        file = csv_name + ".csv"
        csv_file = os.path.join(log_path.parent, file)
        df = pd.read_csv(csv_file, index_col='timestamp')
        df.index = pd.to_datetime(df.index, unit='s', origin='unix')
        os.remove(csv_file)
        return df
    
    #creating kml containers
    
    def rgb_style(self, feature):
        rgb_style = simplekml.Style()
        rgb_style.linestyle.color = simplekml.Color.whitesmoke
        rgb_style.linestyle.width = 2.0
        feature.style = rgb_style
        
    def agr_style(self, feature):
        agr_style = simplekml.Style()
        agr_style.linestyle.color = simplekml.Color.red
        agr_style.linestyle.width = 2.0
        feature.style = agr_style
    
    def create_linestring(self, log_path, kml, container_index):
        ls = kml.containers[container_index].newlinestring(name = log_path.name)
        coords_list = []
        for index, row in cam_df.iterrows():
            coords_list.append((row.Lng, row.Lat))
        ls.coords = coords_list
        return ls
    
    def create_balloon_report(self, feature):
        flight_time = ev_df.index[-1] - ev_df.index[0]  
        feature.balloonstyle.text = "Flight time: " + str(flight_time.components.minutes) + "m " + str(flight_time.components.seconds) + "s \n" +\
                                    "Bat. consumed: " + str(round(bat_df.CurrTot[-1])) + " mAh \n" +\
                                    "\n" +\
                                    "Motors: " + report.motors_status + report.motors_feedback + "\n" +\
                                    "Vibration: " + report.imu_status + report.imu_feedback #"\n" +\
                                    #"EKF variance: " + errors.ekf_count() + "\n" +\
                                    #"GPS glitch: " + errors.gps_glitch_count() 
    #running                                
    def run(self):
        # global path, log_list, self.__kml
        # path = self.input_window()
        # log_list = self.create_log_path(path)
        # self.__kml = self.create_kml('self.__kml')
        
        #TODO: INCLUIR DFS NO OBJETO
        for i in tqdm(self.__log_list):
            self.create_csv(i)
            global cam_df, ev_df, bat_df, terr_df, rcou_df, vibe_df, report
            cam_df = self.create_df(i, "CAM")
            ev_df = self.create_df(i, "EV")
            bat_df = self.create_df(i, "BAT")
            terr_df = self.create_df(i, "TERR")
            rcou_df = self.create_df(i, "RCOU")
            vibe_df = self.create_df(i, "VIBE")
            report = HealthTests(rcou_df, vibe_df)
            report.run()
            if terr_df['CHeight'].median() < 105:
                rgb = self.create_linestring(i, self.__kml, 0)
                self.rgb_style(rgb)
                self.create_balloon_report(rgb)
            elif terr_df['CHeight'].median() > 105:
                agr = self.create_linestring(i, self.__kml, 1)
                self.agr_style(agr)
                self.create_balloon_report(agr)
            else:
                print("Invalid folder name.")
                
        self.__kml.save(self.__root_folder + '/flights.kml')

##running when not being imported
if __name__ == "__main__":
    dc = DayChecker()
    dc.run()
    

