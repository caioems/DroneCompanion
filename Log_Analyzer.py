# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 17:17:20 2022

@author: [t2]caiera
"""

import pathlib
import os
import datetime as dt
import numpy as np
import pandas as pd
import scipy.io
import subprocess
from pprint import pprint
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

types = ["CURR", "ERR", "MSG"]

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

def convert_time(tst):
    time = dt.datetime.fromtimestamp(tst)
    return time

def create_curr_df(log_path):
    csv = str(log_path.parent) + "/CURR.csv"
    df = pd.read_csv(csv, index_col='timestamp')
    df.index = pd.to_datetime(df.index)
    return df
    #os.remove(csv) 
curr_df = create_curr_df(log_list[0])
    



# with open(csv_file, mode = 'r') as f:
#     df = pd.read_csv(f)
#     f.close()

# def delete_csv(log_name, log_path):
#     os.remove(log_path + 'CURR_' + log_name + '.csv')
# delete_csv(log_name, log_path)
    

curr_df.index = curr_df.index.apply(convert_time)





                     