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
from tkinter import Tk
from tkinter.filedialog import askdirectory
from tqdm import tqdm

#user input & WindowsPath object creation
root = Tk()
root.update()
path = askdirectory(title='Select the root folder:')
root.destroy()

def create_log_path (root_path):
    log_list = list(pathlib.Path(root_path).glob(r"**\**\*.BIN"))
    return log_list   

#importing data
def create_csv(log_path):
    types = ["CAM", "EV", "BAT"] #ERR, GPS (HDop), MSG, PARM, POWR, RCOU
    log = log_path.as_posix()
    path = log_path.parent    
    for t in types:
        mycmd = "mavlogdump.py --planner --format csv --types " + t + " " + str(log) + " > " + str(path) + "/" + t + ".csv"
        os.system(mycmd)

def create_df(log_path, csv_name):
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

def create_balloon_report(feature):
    flight_time = ev_df.index[-1] - ev_df.index[0]
    feature.balloonstyle.text = "Flight time: " + str(flight_time.components.minutes) + "m " + str(flight_time.components.seconds) + "s \n" + "Battery consumed: " + str(round(bat_df.CurrTot[-1])) + " mAh"
    #feature.balloonstyle.bgcolor = simplekml.Color.lightgreen
    #feature.balloonstyle.textcolor = simplekml.Color.rgb(0, 0, 255)
    
# def create_logbook(log_path):
#     lb_dict = {"log":[], "bat_bto":[], "bat_ato":[], "bat_amp":[], "bat_res":[], "bat_ald":[], "to_time":[], "ld_time":[]}
#     lb_dict["log"].append(log_path.name)
#     lb_dict["bat_bto"].append(bat_df.columns)

#running functions...
log_list = create_log_path(path) 

flights_kml = create_kml('flights_kml')

for i in tqdm(log_list):
    create_csv(i)    
    cam_df = create_df(i, "CAM")
    ev_df = create_df(i, "EV")
    bat_df = create_df(i, "BAT")
    if any("90_rgb" in s for s in i.parts):
        rgb = create_linestring(i, flights_kml, 0)
        rgb_style(rgb) 
        create_balloon_report(rgb)
    elif any("120_agr" in s for s in i.parts):
        agr = create_linestring(i, flights_kml, 1)
        agr_style(agr)
        create_balloon_report(agr)
    else:
        print("Invalid folder name.")

flights_kml.save(path + '/flights.kml')





                     