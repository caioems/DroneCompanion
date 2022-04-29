# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 17:17:20 2022

@author: [t2]caiera
"""

import pathlib
import os
import datetime as dt
import pandas as pd
import scipy.io
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

def create_curr_csv(log_path):
        mycmd = "mavlogdump.py --planner --format mat --types CURR,ERR  " + str(log_path) + " --mat_file C:\\Users\\T2\\curr.mat"
        os.system(mycmd)
        print("CURR csv created in: " + str(log_path))

create_curr_csv(log_list[0])

def create_err_csv(log_path):
        mycmd = "mavlogdump.py --planner --format csv --types ERR " + str(log_path) + " > err.csv"
        os.system(mycmd)
        print("ERR csv created in: " + str(log_path))

mat = scipy.io.loadmat(r'C:\Users\T2\145.BIN-490217.mat')
pqr = pd.Series(mat)
df = pd.DataFrame({'label':pqr.index, 'list':pqr.values})
#df = df.drop(index=[0,1,2])

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





                     