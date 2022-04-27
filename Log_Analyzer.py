# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 17:17:20 2022

@author: T2
"""

#import csv
import os
#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#from pymavlink.mavextra import *
#from pymavlink import mavutil

log_name = "145"
log_path = "C:\\Users\\T2\\"
types = "CURR"
csv_file = 'C:\\Users\\T2\\curr_145.csv'


def create_csv(log_name, log_path):
    mycmd='mavlogdump.py --planner --format csv --types ' + types + r' C:\Users\T2\145.BIN > C:\Users\T2\curr_145.csv'
    os.system(mycmd)    
create_csv(log_name, log_path)

with open(csv_file, mode = 'r') as f:
    df = pd.read_csv(f)
    f.close()




# def open_fileDB(log_name, log_path, types):
#     with open(log_path+log_name+'.csv', mode='r') as f:
#         myCmd='mavlogdump.py --planner --format csv --types'+types +log_path +log_name +'.BIN > '+log_path +log_name +'.csv'
#         os.system(myCmd)
#         csv = pd.read_csv(f)
#         df.concat(csv)
#         f.close()
        
# open_fileDB("145", "C:\\Users\\T2\\", "CURR")
#os.remove(log_path+'145.csv')





                     