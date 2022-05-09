# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 17:17:20 2022

@author: [t2]caiera
"""

import pathlib
import os
import numpy as np
import pandas as pd
import simplekml
from tkinter import Tk
from tkinter.filedialog import askdirectory

# log_name = "145"
# log_path = "C:\\Users\\T2\\"
# types = ("CURR", "ERR")
# csv_file = "C:\\Users\\T2\\CURR_145.csv"

#user prompt for main folder
root = Tk()
root.update()
path = askdirectory(title='Select the root folder:')
root.destroy()

types = ["CAM", "CURR", "ERR"] #EV, GPS (HDop), MSG, PARM, POWR, RCOU

def create_log_path (root_path):
    log_list = list(pathlib.Path(root_path).glob(r"**\**\*.BIN"))
    return log_list
log_list = create_log_path(path)    

def create_csv(log_path):
    log = log_path.as_posix()
    path = log_path.parent    
    for i in types:
        mycmd = "mavlogdump.py --planner --format csv --types " + i + " " + str(log) + " > " + str(path) + "/" + i + ".csv"
        os.system(mycmd)
    print("CSV files created in: " + str(path))
create_csv(log_list[0])

def create_cam_df(log_path):
    csv = str(log_path.parent) + "/CAM.csv"
    df = pd.read_csv(csv, index_col='timestamp')
    df.index = pd.to_datetime(df.index, unit='s', origin='unix')
    return df
    #os.remove(csv)
cam_df = create_cam_df(log_list[0])

def create_curr_df(log_path):
    csv = str(log_path.parent) + "/CURR.csv"
    df = pd.read_csv(csv, index_col='timestamp')
    df.index = pd.to_datetime(df.index, unit='s', origin='unix')
    return df
    #os.remove(csv) 
curr_df = create_curr_df(log_list[0])

def create_err_df(log_path):
    csv = str(log_path.parent) + "/ERR.csv"
    df = pd.read_csv(csv, index_col='timestamp')
    df.index = pd.to_datetime(df.index, unit='s', origin='unix')
    return df
    #os.remove(csv) 
err_df = create_err_df(log_list[0])

flights_kml = simplekml.Kml()
rgb = flights_kml.newfolder(name='RGB')
agr = flights_kml.newfolder(name='AGR')

def create_linestring(log_path, kml):
    ls = kml.newlinestring(name = log_path.name)
    coords_list = []
    for index, row in cam_df.iterrows():
        coords_list.append((row.Lng, row.Lat))
    ls.coords = coords_list

create_linestring(log_list[0], flights_kml)

flights_kml.save(path + '/flights.kml')



                  
                    
    
    
    



# with open(csv_file, mode = 'r') as f:
#     df = pd.read_csv(f)
#     f.close()

# def delete_csv(log_name, log_path):
#     os.remove(log_path + 'CURR_' + log_name + '.csv')
# delete_csv(log_name, log_path)





                     