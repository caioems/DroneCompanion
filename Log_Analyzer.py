# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 17:17:20 2022

Script designed to take useful information from ArduCopter dataflash logs and
present it on a KML file.

@author: [t2]caiera
"""

import pathlib
import os
import pandas as pd
import simplekml
from sqlalchemy import create_engine, Column, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from statistics import mean, median
from tkinter import Tk
from tkinter.filedialog import askdirectory
from tqdm import tqdm

##MAIN CLASS
class DayChecker:
    #user input for root folder & log list's WindowsPath object creation
    def input_window(self):
        root = Tk()
        root.update()
        path = askdirectory(title='Select the root folder:')
        root.destroy()
        return path
    
    def create_log_path (self, root_path):
        log_list = list(pathlib.Path(root_path).glob(r"**\**\*.BIN"))
        return log_list   
    
    #data modeling
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
    
    #creating kml
    def create_kml(self, kml_name):
        kml_name = simplekml.Kml()
        kml_name.newfolder(name='RGB')
        kml_name.newfolder(name='AGR')
        return kml_name
    
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
        global path, log_list, flights_kml
        path = self.input_window()
        log_list = self.create_log_path(path)
        flights_kml = self.create_kml('flights_kml')
        
        for i in tqdm(log_list):
            self.create_csv(i)
            global cam_df, ev_df, bat_df, terr_df, rcou_df, vibe_df, report
            cam_df = self.create_df(i, "CAM")
            ev_df = self.create_df(i, "EV")
            bat_df = self.create_df(i, "BAT")
            terr_df = self.create_df(i, "TERR")
            rcou_df = self.create_df(i, "RCOU")
            vibe_df = self.create_df(i, "VIBE")
            report = HealthTests()
            report.run()
            if terr_df['CHeight'].median() < 105:
                rgb = self.create_linestring(i, flights_kml, 0)
                self.rgb_style(rgb)
                self.create_balloon_report(rgb)
            elif terr_df['CHeight'].median() > 105:
                agr = self.create_linestring(i, flights_kml, 1)
                self.agr_style(agr)
                self.create_balloon_report(agr)
            else:
                print("Invalid folder name.")
                
        flights_kml.save(path + '/flights.kml')

##HEALTH TESTS OBJECT
class HealthTests:
    def __init__(self):
        self.motors_status = 'UNKNOWN'
        self.motors_feedback = ''
        self.imu_status = 'UNKNOWN'
        self.imu_feedback = ''
        self.gps_status = 'UNKNOWN'
        self.gps_feedback = ''
        
    def motor_test(self):
        self.motors_status = 'OK - '
        self.motors_feedback = 'balanced'
        
        pwm_df = pd.DataFrame({'1':[mean(rcou_df.C1), max(rcou_df.C1)],
                               '2':[mean(rcou_df.C2), max(rcou_df.C2)], 
                               '3':[mean(rcou_df.C3), max(rcou_df.C3)],
                               '4':[mean(rcou_df.C4), max(rcou_df.C4)]}).T
        pwm_df.columns = ["mean", "max"]        
        day_avg = str(int(mean(pwm_df["mean"])))
        avg_list = str([int(x) for x in pwm_df["mean"]])
        max_min = str(int(max(pwm_df["mean"]) - min(pwm_df["mean"])))              
        
        if int(max_min) > 75:
            self.motors_status = 'WARN - '
            self.motors_feedback = 'avg motors pwm: ' + day_avg + " " + avg_list + '. Difference between min and max motor averages: ' + max_min
        elif int(max_min) > 150:
            self.motors_status = 'FAIL - '
            self.motors_feedback = 'avg motors pwm: ' + day_avg + " " + avg_list + '. Difference between min and max motor averages: ' + max_min
            
            
    def vibe_test(self):
        self.imu_status = 'OK - '
        self.imu_feedback = 'no vibe issues'
        
        clips = (vibe_df.Clip0[-1], vibe_df.Clip1[-1], vibe_df.Clip2[-1])
        vibes = (mean(vibe_df.VibeX), mean(vibe_df.VibeY), mean(vibe_df.VibeZ))
        
        if any(v > 30 for v in vibes):
            max_vibes = str(round(max(vibes), 1))
            self.imu_status = 'WARN - '
            self.imu_feedback = 'several vibration (' + max_vibes + ' m/s/s)'
        elif any(c > 0 for c in clips):
            max_clips = str(max(clips))
            self.imu_status = 'FAIL - '
            self.imu_feedback = 'accel was clipped ' + max_clips + ' times'
    
    def run(self):
        self.motor_test()
        self.vibe_test()
        
class DataHandler():
    def __init__(self, db):
        self.engine = create_engine("sqlite:///./" + db)
        self.base = declarative_base()
        Session = sessionmaker(bind=self.engine)
        self.session = Session
    
    #TODO: declarative base
    #TODO: crud
    

##running when not being imported
if __name__ == "__main__":
    dc = DayChecker()
    dc.run()
    

