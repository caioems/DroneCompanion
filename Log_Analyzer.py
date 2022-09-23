# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 17:17:20 2022

Script designed to take useful information from BIN dataflash logs and
present it on a KML file.

@author: [t2]caiera
"""

import pathlib
import os
import pandas as pd
import simplekml
from statistics import mean, median
from tkinter import Tk
from tkinter.filedialog import askdirectory
from tqdm import tqdm

##defining functions...
#user input for root folder & log list's WindowsPath object creation
def input_window():
    root = Tk()
    root.update()
    path = askdirectory(title='Select the root folder:')
    root.destroy()
    return path

def create_log_path (root_path):
    log_list = list(pathlib.Path(root_path).glob(r"**\**\*.BIN"))
    return log_list   

#data modeling
def create_csv(log_path):
    types = ["CAM", "EV", "BAT", "TERR", "RCOU"]
    log = log_path.as_posix()
    path = log_path.parent
    for t in types:    
        mycmd = "mavlogdump.py --planner --format csv --types " + t + " " + str(log) + " > " + str(path) + "/" + t + ".csv"
        os.system(mycmd)

def create_df(log_path, csv_name):
    global file, csv_file
    file = csv_name + ".csv"
    location = log_path.parent
    csv_file = os.path.join(location, file)
    df = pd.read_csv(csv_file, index_col='timestamp')
    df.index = pd.to_datetime(df.index, unit='s', origin='unix')
    os.remove(csv_file)
    return df

#creating kml
def create_kml(kml_name):
    kml_name = simplekml.Kml()
    kml_name.newfolder(name='RGB')
    kml_name.newfolder(name='AGR')
    return kml_name

def rgb_style(feature):
    rgb_style = simplekml.Style()
    rgb_style.linestyle.color = simplekml.Color.whitesmoke
    rgb_style.linestyle.width = 2.0
    feature.style = rgb_style
    
def agr_style(feature):
    agr_style = simplekml.Style()
    agr_style.linestyle.color = simplekml.Color.red
    agr_style.linestyle.width = 2.0
    feature.style = agr_style

def create_linestring(log_path, kml, container_index):
    ls = kml.containers[container_index].newlinestring(name = log_path.name)
    coords_list = []
    for index, row in cam_df.iterrows():
        coords_list.append((row.Lng, row.Lat))
    ls.coords = coords_list
    return ls

#health tests
class HealthTests:
    def __init__(self):
        self.motors_status = 'UNKNOWN'
        self.motors_feedback = ''
        
    def motor_test(self):
        pwm_df = pd.DataFrame({'A':[mean(rcou_df.C1), max(rcou_df.C1)],
                               'B':[mean(rcou_df.C2), max(rcou_df.C2)], 
                               'C':[mean(rcou_df.C3), max(rcou_df.C3)],
                               'D':[mean(rcou_df.C4), max(rcou_df.C4)]}).T
        pwm_df.columns = ["mean", "max"]
        
        if (max(pwm_df["mean"]) - min(pwm_df["mean"])) > 75:
            self.motors_status = 'WARNING'
            self.motors_feedback = ' - motor ' + pwm_df.index[pwm_df['max'] == max(pwm_df["max"])][0]
        elif (max(pwm_df["mean"]) - min(pwm_df["mean"])) > 150:
            self.motors_status = 'FAIL'
            self.motors_feedback = ''
        else:
            self.motors_status = 'OK'
            self.motors_feedback = ' - balanced'
        
def create_balloon_report(feature):
    flight_time = ev_df.index[-1] - ev_df.index[0]
    #errors = Errors()    
    feature.balloonstyle.text = "Flight time: " + str(flight_time.components.minutes) + "m " + str(flight_time.components.seconds) + "s \n" +\
                                "Bat. consumed: " + str(round(bat_df.CurrTot[-1])) + " mAh \n" +\
                                "\n" +\
                                "Motors: " + report.motors_status + report.motors_feedback #"\n" #+\
                                #"Radio FS: " + errors.gcs_count() + "\n" +\
                                #"EKF variance: " + errors.ekf_count() + "\n" +\
                                #"GPS glitch: " + errors.gps_glitch_count()
##main function                               
def day_checker():
    global path, log_list, flights_kml
    path = input_window()    
    log_list = create_log_path(path)     
    flights_kml = create_kml('flights_kml')    
    for i in tqdm(log_list):
        create_csv(i)
        global cam_df, ev_df, bat_df, terr_df, rcou_df, report
        cam_df = create_df(i, "CAM")
        ev_df = create_df(i, "EV")
        bat_df = create_df(i, "BAT")
        terr_df = create_df(i, "TERR")
        rcou_df = create_df(i, "RCOU")
        report = HealthTests()
        report.motor_test()
        if terr_df['CHeight'].median() < 105:
            rgb = create_linestring(i, flights_kml, 0)
            rgb_style(rgb)
            create_balloon_report(rgb)
        elif terr_df['CHeight'].median() > 105:
            agr = create_linestring(i, flights_kml, 1)
            agr_style(agr)
            create_balloon_report(agr)
        else:
            print("Invalid folder name.")
    flights_kml.save(path + '/flights.kml')

##running main function when not being imported
if __name__ == "__main__":
    day_checker()
    

