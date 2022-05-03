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

#lista de logs criada, falta criar lista de subdir
def create_log_path (root_path):
    log_list = list(pathlib.Path(root_path).glob(r"**\**\*.BIN"))
    return log_list
log_list = create_log_path(path)    

def create_csv(log_path):
    log = log_path.as_posix()
    path = log_path.parent
    types = ["CURR", "ERR", "MSG"]
    for i in types:
        mycmd = "mavlogdump.py --planner --format csv --types " + i + " " + str(log) + " > " + str(path) + "/" + i + ".csv"
        os.system(mycmd)
    print("CURR csv created in: " + str(path))
create_csv(log_list[0])



# with open(csv_file, mode = 'r') as f:
#     df = pd.read_csv(f)
#     f.close()

# def delete_csv(log_name, log_path):
#     os.remove(log_path + 'CURR_' + log_name + '.csv')
# delete_csv(log_name, log_path)
    
# def convert_time(tst):
#     time = dt.datetime.fromtimestamp(tst)
#     return time
# df["timestamp"] = df["timestamp"].apply(convert_time)





                     