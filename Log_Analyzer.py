# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 17:17:20 2022

@author: [t2]caiera
"""

import pathlib
import os
#import numpy as np
import pandas as pd
import simplekml
from tkinter import Tk
from tkinter.filedialog import askdirectory
from tqdm import tqdm

# log_name = "145"
# log_path = "C:\\Users\\T2\\"
# types = ("CURR", "ERR")
# csv_file = "C:\\Users\\T2\\CURR_145.csv"

#user input & log's path creation
root = Tk()
root.update()
path = askdirectory(title='Select the root folder:')
root.destroy()

types = ["CAM", "CURR", "ERR"] #EV, GPS (HDop), MSG, PARM, POWR, RCOU

def create_log_path (root_path):
    log_list = list(pathlib.Path(root_path).glob(r"**\**\*.BIN"))
    return log_list
log_list = create_log_path(path)    

#importing data
def create_csv(log_path):
    log = log_path.as_posix()
    path = log_path.parent    
    for i in types:
        mycmd = "mavlogdump.py --planner --format csv --types " + i + " " + str(log) + " > " + str(path) + "/" + i + ".csv"
        os.system(mycmd)
#create_csv(log_list[0])

def create_cam_df(log_path):
    file = "CAM.csv"
    location = log_path.parent
    csv_file = os.path.join(location, file)
    df = pd.read_csv(csv_file, index_col='timestamp')
    df.index = pd.to_datetime(df.index, unit='s', origin='unix')
    os.remove(csv_file)
    return df
    
#cam_df = create_cam_df(log_list[0])

def create_curr_df(log_path):
    file = "CURR.csv"
    location = log_path.parent
    csv_file = os.path.join(location, file)
    df = pd.read_csv(csv_file, index_col='timestamp')
    df.index = pd.to_datetime(df.index, unit='s', origin='unix')
    os.remove(csv_file)
    return df 

#curr_df = create_curr_df(log_list[0])

def create_err_df(log_path):
    file = "ERR.csv"
    location = log_path.parent
    csv_file = os.path.join(location, file)
    df = pd.read_csv(csv_file, index_col='timestamp')
    df.index = pd.to_datetime(df.index, unit='s', origin='unix')
    os.remove(csv_file)
    return df
 
#err_df = create_err_df(log_list[0])

#creating kml
flights_kml = simplekml.Kml()
rgb = flights_kml.newfolder(name='RGB')
agr = flights_kml.newfolder(name='AGR')

def create_linestring(log_path, kml):
    ls = kml.containers[1].newlinestring(name = log_path.name)
    coords_list = []
    for index, row in cam_df.iterrows():
        coords_list.append((row.Lng, row.Lat))
    ls.coords = coords_list

for i in tqdm(log_list):
    create_csv(i)
    cam_df = create_cam_df(i)
    create_linestring(i, flights_kml)

flights_kml.save(path + '/flights.kml')



                  
                    
    
    
    



# with open(csv_file, mode = 'r') as f:
#     df = pd.read_csv(f)
#     f.close()
# def delete_csv(log_name, log_path):
#     os.remove(log_path + 'CURR_' + log_name + '.csv')
# delete_csv(log_name, log_path)





                     